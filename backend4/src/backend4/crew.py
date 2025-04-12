from pathlib import Path
import shutil

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task as task_decorator

from backend4.tools.custom_tool import FileReaderTool, FileWriterTool
from backend4.tools.test_tool import FlaskTestClientTool
from backend4.tools.lookup_tool import DataObjectLookupTool


# 🔧 Tool-Mapping für YAML-Tasks
tool_functions = {
    "file_reader": FileReaderTool,
    "file_writer": FileWriterTool,
    "flask_test_client": FlaskTestClientTool,
}


@CrewBase
class Backend4():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # 🧠 AGENTS ---------------------------------------------------------------
    @agent
    def structure_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["structure_designer"],
            verbose=True,
            tools=[DataObjectLookupTool()],
        )

    @agent
    def code_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["code_creator"],
            verbose=True,
            tools=[FileReaderTool()],
        )

    @agent
    def code_tester(self) -> Agent:
        return Agent(
            config=self.agents_config["code_tester"],
            verbose=True,
            tools=[FlaskTestClientTool(), FileReaderTool()],
        )

    @agent
    def bug_fixer(self) -> Agent:
        return Agent(
            config=self.agents_config["bug_fixer"],
            verbose=True,
            tools=[FileReaderTool(), FileWriterTool()],
        )

    # 🧠 TASKS FÜR DEN CREW-ABLAUF -------------------------------------------
    @task_decorator
    def models_planning_task(self) -> Task:
        return Task(config=self.tasks_config["models_planning_task"])

    @task_decorator
    def routes_planning_task(self) -> Task:
        return Task(config=self.tasks_config["routes_planning_task"])

    @task_decorator
    def backend_models_task(self) -> Task:
        return Task(config=self.tasks_config["backend_models_task"])

    @task_decorator
    def backend_app_task(self) -> Task:
        return Task(config=self.tasks_config["backend_app_task"])

    @task_decorator
    def pause_task(self) -> Task:
        return Task(config=self.tasks_config["pause_task"])

    @task_decorator
    def backend_endpoint_summary_task(self) -> Task:
        return Task(config=self.tasks_config["backend_endpoint_summary_task"])

    @task_decorator
    def backend_test_task(self) -> Task:
        return Task(config=self.tasks_config["backend_test_task"])

    # ✅ NICHT als @task: Diese werden manuell mit .build_task() erstellt!
    def build_task(self, name: str, agent, output_file=None) -> Task:
        config = self.tasks_config[name]
        return Task(
            description=config["description"],
            expected_output=config["expected_output"],
            agent=agent,
            tools=config.get("tools", []),
            context=config.get("context", []),
            output_file=output_file or config.get("output_file", None),
        )

    # 🧠 CREW-ZUSAMMENSTELLUNG ----------------------------------------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=[
                self.models_planning_task(),
                self.routes_planning_task(),
                self.backend_models_task(),
                self.backend_app_task(),
                self.pause_task(),
                self.backend_endpoint_summary_task(),
                self.backend_test_task(),
            ],
            process=Process.sequential,
            verbose=True,
        )

    # 🔁 FEHLERBEHEBUNGS-LOOP -----------------------------------------------
    def retry_fixing_errors(self, inputs: dict, max_attempts: int = 3):
        attempt = 0
        test_report = Path("Output/test_report.md")

        while attempt < max_attempts:
            attempt += 1
            print(f"\n🔁 Bugfix Attempt #{attempt}")

            if not test_report.exists():
                print("⚠️ Test report not found. Skipping fix.")
                break

            report_content = test_report.read_text(encoding="utf-8")

            if "❌" not in report_content:
                print("✅ All tests passed. No more fixes required.")
                break

            # 🛠 Bugfix-Tasks ausführen
            analyze_task = self.build_task("analyze_failed_requests_task", self.bug_fixer())
            analyze_task.kickoff(inputs=inputs)

            fix_task = self.build_task("fix_code_task", self.bug_fixer())
            fix_task.kickoff(inputs=inputs)

            # 🔁 Test erneut laufen lassen
            summary_task = self.build_task("backend_endpoint_summary_task", self.code_tester())
            summary_task.kickoff(inputs=inputs)

            test_task = self.build_task("backend_test_task", self.code_tester())
            test_task.kickoff(inputs=inputs)

        # 📁 Bericht sichern
        if test_report.exists():
            final_path = Path("Output/test_report_final.md")
            shutil.copy(test_report, final_path)
            print(f"📁 Final test report saved as {final_path}")
