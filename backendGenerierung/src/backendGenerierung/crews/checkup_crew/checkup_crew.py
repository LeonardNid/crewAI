import json
from typing import Any, Tuple
from crewai import Agent, Crew, Process, Task, TaskOutput
from crewai.project import CrewBase, agent, crew, task

from backendGenerierung.tools.json_patch_tool import JsonPatchTool, JsonPatchToolInput
from backendGenerierung.crews.checkup_crew.JsonSchema import Verification
import os

@CrewBase
class CheckupCrew:
    """Checkup Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def branch_verifier(self) -> Agent:
        return Agent(
            config=self.agents_config["branch_verifier"],
            verbose=True,
        )

    @agent
    def verification_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["verification_agent"],
            verbose=True,
        )
    
    # ──────────────────────────────────────────────────────────────────────────────
    #  BRANCH VERIFIER TASK
    # ──────────────────────────────────────────────────────────────────────────────

    # def callback_function(self, output: TaskOutput):
    #     if not output.json_dict:
    #         print("Output JSON is empty. Skipping tool execution.")
    #         return
    #     result = JsonPatchTool().run(**output.json_dict)
    #     print(result)

    def guardrail_function(self, output: TaskOutput) -> Tuple[bool, Any]:
        try:
            os.makedirs("Output/checkupCrew", exist_ok=True)
            with open("Output/checkupCrew/old_changes.json", "w") as f:
                json.dump(output.json_dict, f, indent=2)
            if output.json_dict:
                print(JsonPatchTool().run(**output.json_dict))
            else:
                print("Output JSON is empty. Skipping tool execution, no changes needed")
            with open("Output/backendCrew/routes.json", "r") as file:
                return (True, json.dumps(json.load(file), indent=2))
        except Exception as err:
            print(f"Patch failed: {err}")
            return False, str(err)

    @task
    def branch_verification_task(self) -> Task:
        return Task(
            config=self.tasks_config["branch_verification_task"],
            # tools=[JsonPatchTool()],
            # tools=[JsonBranchUpdateTool()],
            output_json=JsonPatchToolInput,
            guardrail=self.guardrail_function,
        )
    
    # ──────────────────────────────────────────────────────────────────────────────
    #  VERIFICATION AGENT TASK
    # ──────────────────────────────────────────────────────────────────────────────
    
    @task
    def verification_task(self) -> Task:
        return Task(
            config=self.tasks_config["verification_task"],
            output_json=Verification,
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
