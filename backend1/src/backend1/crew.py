from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import FileWriterTool, FileReaderTool
from dotenv import load_dotenv
load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Backend1():
	"""Backend1 crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# ollama_llm = LLM(
	# 	model='ollama/llama3.2:3b',
	# 	base_url='http://localhost:11434'
	# )

	ollama_llm = LLM(
		model='ollama/deepseek-r1:14b',
		base_url='http://localhost:11434'
	)

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def code_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['code_creator'],
			verbose=True,
			tools=[FileWriterTool(), FileReaderTool()],
			llm=self.ollama_llm
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
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
	
	# @task
	# def backend_refactor_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['backend_refactor_task']
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the Backend1 crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
