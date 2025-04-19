from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from backend5.tools.custom_tool import FileReaderTool, FileWriterTool

@CrewBase
class BugFixCrew:
    """Bug fix Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def bug_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["bug_analyzer"],
            verbose=True,
        )
    
    @agent
    def code_modifier(self) -> Agent:
        return Agent(
            config=self.agents_config["code_modifier"],
            verbose=True,
            tools=[FileWriterTool()],
        )
    
    # Tasks

    @task
    def analyze_startup_failure_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_startup_failure_task"],
        )
    
    @task
    def analyze_failed_requests_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_failed_requests_task"],
        )

    @task
    def fix_code_task(self) -> Task:
        return Task(
            config=self.tasks_config["fix_code_task"],
        )
    
    
    
    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        
        # Define a custom manager agent (Manager agent should not be included in agents list.)
        manager = Agent(
            role="Bug Fix Task Manager",
            goal="The application got a {test_result_type}. Decide how to proceed with the fix attempt based on test results: {test_result}", 
            backstory="You're in charge of managing the bug fix process. Based on the test result, you decide if the problem lies in code execution or in specific failed requests and assign the right team.",
            allow_delegation=True,
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=manager,
            verbose=True,
        )
