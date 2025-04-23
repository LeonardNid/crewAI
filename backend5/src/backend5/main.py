#!/usr/bin/env python
import json, yaml, shutil
from pathlib import Path

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router, or_

from backend5.crews.backend_crew.backend_crew import BackendCrew
from backend5.crews.checkup_crew.checkup_crew import CheckupCrew
from backend5.crews.test_crew.test_crew import TestCrew
from backend5.crews.bug_fix_crew.bug_fix_crew import BugFixCrew

from backend5.Utils import read_file, renderTemplate

import weave

SCENARIO_KEY = "football"

class BackendState(BaseModel):
    skip: bool = False
    backend_crew_count: int = 0
    backend_crew_defects: list = []
    test_count: int = 0
    test_result: str = ""
    test_result_type: str = ""


class BackendFlow(Flow[BackendState]):

    weave.init(project_name="backend5")

    @start()
    def clean_directories(self):
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

    @listen(or_(clean_directories, "retryBackendCrew"))
    def generate_Backend(self):
        # inputs vorbereiten
        with open("src/backend5/prompts.yaml", "r", encoding="utf-8") as f:
            scenarios = yaml.safe_load(f)

        feature_checklist = ""
        entity_overview = ""
        models_json = ""
        routes_json = ""

        if (self.state.backend_crew_count > 0):
            feature_checklist = read_file("Output/backendCrew/feature_checklist.md")
            entity_overview = read_file("Output/backendCrew/entity_overview.md")
            models_json = read_file("Output/backendCrew/models.json")
            routes_json = read_file("Output/backendCrew/routes.json")

        inputs = scenarios[SCENARIO_KEY] | {
            "defects": self.state.backend_crew_defects,
            "feature_checklist": feature_checklist,
            "entity_overview": entity_overview,
            "models_json": models_json,
            "routes_json": routes_json,
        }

        print("Backend crew started")
        result = (
            BackendCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        print("Backend crew finished")
        self.state.backend_crew_count += 1


        print("Backend crew attempts: ", self.state.backend_crew_count)
        if (input("py's erstellt, continue? (y/n): ") == "n"):
            self.state.skip = True
        
    @router(generate_Backend)
    def checkup(self):
        

        inputs = {

        }

        print("Checkup crew started")
        result = (
            CheckupCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        print("Checkup crew finished")

        verification_Json = result.tasks_output[2].to_dict()
        if (verification_Json["retry"]):
            self.state.backend_crew_defects = verification_Json["defects"]
            print("verification_Json: ", verification_Json)
            input("retryBackendCrew")
            return "retryBackendCrew"
        
        renderTemplate("models.j2", "Output/backendCrew/models.json", "Output/models.py")
        renderTemplate("app.j2", "Output/backendCrew/routes.json", "Output/app.py")
        return "firstTest"

    @listen(or_("firstTest", "fix_bug"))
    def test_Backend(self):
        if self.state.skip:
            print("Skipping test crew due to previous failure.")
            return "skipped"

        print("Test crew started")
        routes_json = read_file("Output/backendCrew/routes.json")
        app_py = read_file("Output/app.py")
        inputs = {
            "app_py": app_py,
            "routes_json": routes_json,
        }
        result = (
            TestCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        self.state.test_count += 1
        self.state.test_result = result.raw
        print("Test crew finished")
        if (input("after TestCrew, continue? (y/n): ") == "n"):
            self.state.skip = True

    @router(test_Backend)
    def check_results(self):
        """
        Parses the JSON test_result to check for any failed requests.
        Returns 'failed' if any request has a status code >= 400.
        """
        if self.state.skip:
            print("Skipping result check due to previous failure.")
            return "skipped"


        try:
            first_line = self.state.test_result.strip().splitlines()[0]
            if first_line.startswith("Python code is not executable!"):
                self.state.test_result_type = "startup_failure"
                return "failed"

            results = json.loads(self.state.test_result)
            for entry in results:
                code = entry.get("status_code", "")
                if code >= 400:
                    self.state.test_result_type = "requests_failure"
                    return "failed"

            print("Test passed ✅")
            return "success"

        except Exception as e:
            print("⚠️ Error parsing test_result:", e)
            return "failed"
        
    @listen("failed")
    def fix_bug(self):
        if self.state.skip:
            print("Skipping bug fix crew due to previous failure.")
            return "skipped"
        
        print("Bug fix crew started")
        app_py = read_file("Output/app.py")
        models_py = read_file("Output/models.py")
        inputs = {
            "test_result_type": self.state.test_result_type,
            "test_result": self.state.test_result,
            "app_py": app_py,
            "models_py": models_py,
        }
        result = (
            BugFixCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        print("Bug fix crew finished")
        
    @listen(or_("success", "skipped"))
    def final(self):
        if self.state.skip:
            print("Flow stopped due to user input.")
        else:
            print("All tests passed successfully!")
        print("Test attempts:", self.state.test_count)
        print("Backend crew attempts:", self.state.backend_crew_count)

def kickoff():
    backendFlow = BackendFlow()
    backendFlow.kickoff()


def plot():
    backendFlow = BackendFlow()
    backendFlow.plot()


if __name__ == "__main__":
    kickoff()
