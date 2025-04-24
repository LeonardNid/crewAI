from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from backend5.tools.lookup_tool import DataObjectLookupTool
from backend5.crews.backend_crew.JsonSchema import ModelsPlan, RoutesPlan

@CrewBase
class BackendCrew:
    """Backend Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def requirements_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["requirements_analyst"],
            verbose=True,
        )
    
    @agent
    def api_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["api_planner"],
            verbose=True,
        )
    
    # ──────────────────────────────────────────────────────────────────────────────
    #  REQUIREMENTS ANALYST TASKS
    # ──────────────────────────────────────────────────────────────────────────────
    @task
    def features_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["features_extraction_task"],
        )
    
    @task
    def entities_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["entities_extraction_task"],
        )
    
    # ──────────────────────────────────────────────────────────────────────────────
    #  API PLANNER TASKS
    # ──────────────────────────────────────────────────────────────────────────────
    @task
    def models_json_task(self) -> Task:
        return Task(
            config=self.tasks_config["models_json_task"],
            tools=[DataObjectLookupTool()],
            output_json=ModelsPlan,
        )
    
    @task
    def routes_json_task(self) -> Task:
        return Task(
            config=self.tasks_config["routes_json_task"],
            output_json=RoutesPlan,
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""

        # manager agent (NOT part of the agents list)
        manager = Agent(
            role="Backend Manager",
            goal=(
                "Efficiently manage the crew and ensure high-quality task completion."
                "The Verification Agent has to confirm the models and routes JSON files"
                "and don't detect any defects."
            ),
            backstory=(
                "You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard."
                "You coordinate the pipeline until the verification agent "
                "confirms full coverage."
            ),
            allow_delegation=True,
        )


        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            manager_agent=manager,
            verbose=True,
        )
