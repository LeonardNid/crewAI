from typing import Any, Tuple, Union
from crewai import Agent, Crew, Process, Task, TaskOutput
from crewai.project import CrewBase, agent, crew, task
from pydantic import ValidationError

from backend5.tools.test_tool import FlaskTestClientTool, BulkTestClientInput

@CrewBase
class TestCrew:
    """Test Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def code_tester(self) -> Agent:
        return Agent(
            config=self.agents_config["code_tester"],
            verbose=True,
        )
    
    # Tasks
    @task
    def backend_endpoint_summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_endpoint_summary_task"],
        )
    
    # def callback_function(self, output: TaskOutput):
    #     if not output.json_dict:
    #         print("Output JSON is empty. Skipping tool execution.")
    #         return
    #     result = FlaskTestClientTool().run(**output.json_dict)
    #     print(result)

    def guardrail_function(self, output: TaskOutput) -> tuple[bool, str]:
        try:
            BulkTestClientInput(**(payload := output.json_dict))
            res = FlaskTestClientTool().run(**payload)
            if isinstance(res, str) and res.startswith("Validation failed"):
                raise ValueError(res)
            return True, res
        except (AttributeError, ValidationError, ValueError) as err:
            return False, str(err)
    
    @task
    def backend_test_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_test_task"],
            # tools=[FlaskTestClientTool(result_as_answer=True)],
            output_json=BulkTestClientInput,
            # callback=self.callback_function,
            guardrail=self.guardrail_function,
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
