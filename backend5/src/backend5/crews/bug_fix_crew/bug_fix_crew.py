from crewai import Agent, Crew, Process, Task, TaskOutput
from crewai.project import CrewBase, agent, crew, task

from backend5.crews.bug_fix_crew.JsonSchema import fix_code_task_output
from backend5.tools.json_patch_tool import JsonPatchTool, JsonPatchToolInput

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
    
    # Tasks

    @task
    def analyze_python_code_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_python_code_task"],
        )
    

    def callback_function(self, output: TaskOutput):
        if not output.json_dict:
            print("Output JSON is empty. Skipping tool execution.")
            return
        
        if output.json_dict.get("models"):
            print("Processing models...")
            result_models = JsonPatchTool().run(**output.json_dict["models"])
            print("Models result:", result_models)
        
        if output.json_dict.get("routes"):
            print("Processing routes...")
            result_routes = JsonPatchTool().run(**output.json_dict["routes"])
            print("Routes result:", result_routes)

    @task
    def fix_code_task(self) -> Task:
        return Task(
            config=self.tasks_config["fix_code_task"],
            # tools=[JsonPatchTool()],
            output_json=fix_code_task_output,
            callback=self.callback_function,
        )
    
    
    
    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        
        # Define a custom manager agent (Manager agent should not be included in agents list.)
        # manager = Agent(
        #     role="Bug Fix Task Manager",
        #     goal="The application got a {test_result_type}. Decide how to proceed with the fix attempt based on test results: {test_result}", 
        #     backstory="You're in charge of managing the bug fix process. Based on the test result, you decide if the problem lies in code execution or in specific failed requests and assign the right team.",
        #     allow_delegation=True,
        # )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            # manager_agent=manager,
            verbose=True,
        )
