from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from backend5.tools.Json_Branch_Update_Tool import JsonBranchUpdateTool
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
    
    @task
    def branch_verification_task(self) -> Task:
        return Task(
            config=self.tasks_config["branch_verification_task"],
            tools=[JsonBranchUpdateTool()],
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
