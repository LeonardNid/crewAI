#!/usr/bin/env python
import json, yaml

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router, or_

from backend5.crews.backend_crew.backend_crew import DesignCrew
from backend5.crews.test_crew.test_crew import TestCrew
from backend5.crews.bug_fix_crew.bug_fix_crew import BugFixCrew
from backend5.tools.Utils import read_file, cleanup_quotes_in_file

import weave
import shutil
from pathlib import Path

SCENARIO_KEY = "football"

class BackendState(BaseModel):
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
            else:
                dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Cleared folder: {folder}")

    @listen(clean_directories)
    def generate_Design(self):
        print("Design crew started")

        # inputs vorbereiten
        with open("src/backend5/prompts.yaml", "r", encoding="utf-8") as f:
            scenarios = yaml.safe_load(f)
        # Templates laden
        app_tpl = read_file("files/templates/app_template.py")
        models_tpl = read_file("files/templates/models_template.py")

        inputs = scenarios[SCENARIO_KEY] | {
            "app_template":    app_tpl,
            "models_template": models_tpl,
        }

        result = (
            DesignCrew()
            .crew()
            .kickoff(inputs=inputs)
        )

        print("Design crew finished")

    @listen(or_(generate_Design, "fix_bug"))
    def test_Backend(self):
        input("Pause")

        # Cleanup quotes in the generated files before running tests
        for target_file in ["Output/app.py", "Output/models.py"]:
            cleanup_quotes_in_file(target_file) 

        input("Pause") # Temporary pause for debugging


        print("Test crew started")
        app_plan_md = read_file("Output/app_plan.md")
        app_py = read_file("Output/app.py")
        inputs = {
            "app_py": app_py,
            "app_plan_md": app_plan_md,
        }
        result = (
            TestCrew()
            .crew()
            .kickoff(inputs=inputs)
        )
        self.state.test_count += 1
        print("Test crew finished")
        self.state.test_result = result.raw

    @router(test_Backend)
    def check_results(self):
        """
        Parses the JSON test_result to check for any failed requests.
        Returns 'failed' if any request has a status code >= 400.
        """

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
            return "error"
        
    @listen("failed")
    def fix_bug(self):
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
        
    @listen("success")
    def final(self):
        print("All tests passed successfully!")
        print("Test attempts:", self.state.test_count)
    

def kickoff():
    backendFlow = BackendFlow()
    backendFlow.kickoff()


def plot():
    backendFlow = BackendFlow()
    backendFlow.plot()


if __name__ == "__main__":
    kickoff()
