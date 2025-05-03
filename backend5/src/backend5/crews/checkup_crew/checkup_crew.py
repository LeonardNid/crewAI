from crewai import Agent, Crew, Process, Task, TaskOutput
from crewai.project import CrewBase, agent, crew, task

from backend5.tools.json_patch_tool import JsonPatchTool, JsonPatchToolInput
from backend5.crews.checkup_crew.JsonSchema import Verification

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

    def callback_function(self, output: TaskOutput):
        if not output.json_dict:
            print("Output JSON is empty. Skipping tool execution.")
            return
        result = JsonPatchTool().run(**output.json_dict)
        print(result)
    
    @task
    def branch_verification_task(self) -> Task:
        return Task(
            config=self.tasks_config["branch_verification_task"],
            # tools=[JsonPatchTool()],
            # tools=[JsonBranchUpdateTool()],
            output_json=JsonPatchToolInput,
            callback=self.callback_function,
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
