from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from backend4.tools.custom_tool import FileReaderTool, FileWriterTool
from backend4.tools.test_tool import FlaskTestClientTool
from backend4.tools.lookup_tool import DataObjectLoopupTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Backend4():
    """Backend4 crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def structure_designer(self) -> Agent:
        return Agent(
			config=self.agents_config['structure_designer'],
			verbose=True,
			tools=[DataObjectLoopupTool()],
			# llm=self.ollama_llm
		)
    
    @agent
    def code_creator(self) -> Agent:
        return Agent(
			config=self.agents_config['code_creator'],
			verbose=True,
			tools=[FileReaderTool()],
			# llm=self.ollama_llm
		)
    
    @agent
    def code_tester(self) -> Agent:
        return Agent(
			config=self.agents_config['code_tester'],
			verbose=True,
			tools=[FlaskTestClientTool()],
			# llm=self.ollama_llm
		)
    
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    # structure_designer
    @task
    def models_planning_task(self) -> Task:
        return Task(
			config=self.tasks_config['models_planning_task'],
		)
	
    @task
    def routes_planning_task(self) -> Task:
        return Task(
			config=self.tasks_config['routes_planning_task'],
		)

    # code_creator

    @task
    def backend_models_task(self) -> Task:
        return Task(
			config=self.tasks_config['backend_models_task']
		)
	
    @task
    def backend_app_task(self) -> Task:
        return Task(
			config=self.tasks_config['backend_app_task']
		)
    
    # code_tester

    @task
    def backend_endpoint_summary_task(self) -> Task:
        return Task(
			config=self.tasks_config['backend_endpoint_summary_task']
		)
    
    @task
    def backend_test_task(self) -> Task:
        return Task(
			config=self.tasks_config['backend_test_task']
		)
    
    

    @crew
    def crew(self) -> Crew:
        """Creates the Backend4 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
