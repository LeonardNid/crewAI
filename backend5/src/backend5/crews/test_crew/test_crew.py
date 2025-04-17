from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from backend5.tools.test_tool import FlaskTestClientTool
from backend5.tools.custom_tool import FileReaderTool, FileWriterTool

@CrewBase
class TestCrew:
    """Test Crew"""

    tasks_config = "config/tasks.yaml"

    @agent
    def code_tester(self) -> Agent:
        return Agent(
            config=self.agents_config["code_tester"],
            verbose=True,
            tools=[FlaskTestClientTool(result_as_answer=True), FileReaderTool()],
        )
    
    # Tasks
    @task
    def backend_endpoint_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_endpoint_summary_task"],
        )
    
    @task
    def backend_test_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_test_task"],
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
