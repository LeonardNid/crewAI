#!/usr/bin/env python
import json, yaml, shutil
from pathlib import Path

from typing import Any, Dict, List
from pydantic import BaseModel, Field

from crewai.flow import Flow, listen, start, router, or_

from backendGenerierung.crews.backend_crew.backend_crew import BackendCrew
from backendGenerierung.crews.checkup_crew.checkup_crew import CheckupCrew
from backendGenerierung.crews.test_crew.test_crew import TestCrew
from backendGenerierung.crews.bug_fix_crew.bug_fix_crew import BugFixCrew

from backendGenerierung.Utils import read_file, renderTemplate, enrich_Endpoints, enrich_Models

import weave

SCENARIO_KEY = "library"
BACKEND_MAX_RETRY = 5
TEST_MAX_RETRY = 10

class BackendLoop(BaseModel):
    count: int = 0
    feature_checklist: str = ""
    entity_overview: str = ""
    retry: bool = False
    defects: List[str] = Field(default_factory=list)
    models_json: Dict[str, Any] = Field(default_factory=dict)
    routes_json: Dict[str, Any] = Field(default_factory=dict)

class TestLoop(BaseModel):
    count: int = 0
    result: str = ""
    result_type: str = ""

class BackendState(BaseModel):
    breakFlow: bool = False
    bL: BackendLoop = BackendLoop()
    tL: TestLoop = TestLoop()


class BackendFlow(Flow[BackendState]):

    weave.init(project_name="backendGenerierung")

    @start()
    def start(self):
        """
        Cleans the Output and instance directories before running the crews.
        """
        for folder in ["Output", "instance"]:
            dir_path = Path(folder)
            if dir_path.exists() and dir_path.is_dir():
                for item in dir_path.iterdir():
                    try:
                        if item.is_file() or item.is_symlink():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                    except Exception as e:
                        print(f"⚠️ Could not delete {item}: {e}")
                        raise e
            else:
                dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Cleared folder: {folder}")

    @listen(or_(start, "retryBackendCrew"))
    def generate_Backend(self):
        # inputs vorbereiten
        with open("src/backendGenerierung/prompts.yaml", "r", encoding="utf-8") as f:
            scenarios = yaml.safe_load(f)

        inputs = scenarios[SCENARIO_KEY] | {
            "defects": self.state.bL.defects,
            "feature_checklist": self.state.bL.feature_checklist,
            "entity_overview": self.state.bL.entity_overview,
            "models_json": self.state.bL.models_json,
            "routes_json": self.state.bL.routes_json,
        }

        print("Backend crew started")
        result = (
            BackendCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        print("Backend crew finished")

        self.state.bL.count += 1
        self.state.bL.feature_checklist = result.tasks_output[0].raw
        self.state.bL.entity_overview = result.tasks_output[1].raw
        self.state.bL.models_json = result.tasks_output[2].to_dict()
        self.state.bL.routes_json = result.tasks_output[3].to_dict()

        # if (input("End of 'generate_Backend' | 'n' to break the Flow: ") == "n"): # user input to break the flow
        #     self.state.breakFlow = True
        
    @listen(generate_Backend)
    def enrich_JSON(self):
        self.state.bL.routes_json = enrich_Endpoints(self.state.bL.routes_json)
        self.state.bL.models_json = enrich_Models(self.state.bL.models_json)

        # if (input("JSON Enriched | 'n' to break the Flow: ") == "n"): # user input to break the flow
        #     self.state.breakFlow = True

    @listen(enrich_JSON)
    def checkup_backend(self):
        if self.state.breakFlow: # break the flow 
            return "breakFlow"

        inputs = {
            "feature_checklist": self.state.bL.feature_checklist,
            "models_json": self.state.bL.models_json,
            "routes_json": self.state.bL.routes_json,
        }

        print("Checkup crew started")
        result = (
            CheckupCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        print("Checkup crew finished")

        # Aktualisiere die routes_json im State
        self.state.bL.routes_json = read_file("Output/backendCrew/routes.json", as_json=True)

        self.state.bL.retry = result.tasks_output[1].json_dict["retry"]
        self.state.bL.defects = result.tasks_output[1].json_dict["defects"]
    
    @router(checkup_backend)
    def check_Backend_Results(self):
        if (self.state.bL.retry):
            print("attempts: ", self.state.bL.count)
            print("verification_Json: ", self.state.bL.defects)
            # if not (input("retryBackendCrew | 'n' to skip retry: ") == "n"): # user input to stop retry of BackendCrew
            if self.state.bL.count < BACKEND_MAX_RETRY:
                return "retryBackendCrew"
        return "renderTemplate"
    
    @listen(or_("renderTemplate", "fix_bug"))
    def render_Templates(self):
        renderTemplate("models.j2", self.state.bL.models_json, "Output/models.py")
        renderTemplate("app.j2", self.state.bL.routes_json, "Output/app.py")

        # print("Backend crew attempts: ", self.state.bL.count)
        # if (input("py's erstellt | 'n' to break the Flow: ") == "n"): # user input to break the flow
        #     self.state.breakFlow = True

    
    @listen(render_Templates)
    def test_Backend(self):
        if self.state.breakFlow: # break the flow 
            return "breakFlow"

        print("Test crew started")
        inputs = {
            "models_json": self.state.bL.models_json,
            "routes_json": self.state.bL.routes_json,
        }
        result = (
            TestCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        self.state.tL.count += 1
        self.state.tL.result = result.raw

        print("Test crew finished")
        # if (input("after TestCrew, continue? (y/n): ") == "n"):
        #     self.state.breakFlow = True

    @router(test_Backend)
    def check_test_results(self):
        """
        Parses the JSON test_result to check for any failed requests.
        Returns 'failed' if any request has a status code >= 400.
        """
        if self.state.breakFlow: # break the flow 
            return "breakFlow"
        if self.state.tL.count >= TEST_MAX_RETRY:
            return "breakFlow"

        try:
            first_line = self.state.tL.result.strip().splitlines()[0]
            if first_line.startswith("Python code is not executable!"):
                self.state.tL.result_type = "startup_failure"
                return "failed"

            results = json.loads(self.state.tL.result)
            for entry in results:
                code = entry.get("status_code", "")
                if code >= 400:
                    self.state.tL.result_type = "requests_failure"
                    return "failed"

            print("Test passed ✅")
            return "success"

        except Exception as e:
            print("⚠️ Error parsing test_result:", e)
            return "failed"
        
    @listen("failed")
    def fix_bug(self):
        # if (input("fix_bug, continue? (y/n): ") == "n"):
        #     self.state.breakFlow = True
        #     return


        if self.state.breakFlow: # break the flow 
            return "breakFlow"
        
        print("Bug fix crew started")
        app_py = read_file("Output/app.py")
        models_py = read_file("Output/models.py")
        inputs = {
            "test_result_type": self.state.tL.result_type,
            "test_result": self.state.tL.result,
            "app_py": app_py,
            "models_py": models_py,
            "routes_json": self.state.bL.routes_json,
            "models_json": self.state.bL.models_json,
        }
        result = (
            BugFixCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        # JSON aktualisieren
        self.state.bL.models_json = read_file("Output/backendCrew/models.json", as_json=True)
        self.state.bL.routes_json = read_file("Output/backendCrew/routes.json", as_json=True)
        print("Bug fix crew finished")
        
    @listen(or_("success", "breakFlow"))
    def finish(self):
        if self.state.breakFlow:
            print("Flow stopped due to \"breakFlow\".")
        else:
            print("All tests passed successfully!")
        print("Test attempts:", self.state.tL.count)
        print("Backend crew attempts:", self.state.bL.count)

def kickoff():
    backendFlow = BackendFlow()
    backendFlow.kickoff()


def plot():
    backendFlow = BackendFlow()
    backendFlow.plot()


if __name__ == "__main__":
    kickoff()
