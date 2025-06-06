from typing import Any, Tuple
from crewai import Agent, Crew, Process, Task, TaskOutput
from crewai.project import CrewBase, agent, crew, task

from backendGenerierung.crews.bug_fix_crew.JsonSchema import fix_code_task_output
from backendGenerierung.tools.json_patch_tool import JsonPatchTool, JsonPatchToolInput

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
    

    def guardrail_function(self, output: TaskOutput) -> tuple[bool, str]:
        try:
            for section in ("models", "routes"):
                payload = output.json_dict.get(section)
                if payload:                           # nur wenn der Agent etwas liefert
                    res = JsonPatchTool().run(**payload)
                    print(f"{section} → {res}")
            return True, output.json_dict
        except Exception as err:
            print(f"Patch failed: {err}")
            return False, str(err)


    @task
    def fix_code_task(self) -> Task:
        return Task(
            config=self.tasks_config["fix_code_task"],
            # tools=[JsonPatchTool()],
            output_json=fix_code_task_output,
            guardrail=self.guardrail_function,
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
