from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from backend5.tools.lookup_tool import DataObjectLookupTool

@CrewBase
class BackendCrew:
    """Backend Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def structure_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["structure_designer"],
            verbose=True,
        )
    
    @agent
    def code_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["code_creator"],
            verbose=True,
        )
    
    # Tasks

    # structure_designer tasks
    @task
    def models_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["models_planning_task"],
            tools=[DataObjectLookupTool()]
        )
    
    @task
    def routes_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["routes_planning_task"],
        )
    
    # code_creator tasks
    @task
    def backend_models_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_models_task"],
    )

    @task
    def backend_app_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_app_task"],
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
