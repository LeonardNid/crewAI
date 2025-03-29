# test_tool.py
import os
import sys
import importlib.util
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class TestClientInput(BaseModel):
    route: str = Field(..., description="e.g. '/teams'")
    method: str = Field("GET", description="HTTP method: GET, POST, PUT, DELETE")
    json_data: dict = Field(None, description="Request body if needed for POST/PUT")


class FlaskTestClientTool(BaseTool):
    name: str = "flask_test_client"
    description: str = (
        "Allows sending requests to the dynamically loaded Flask app (app.py) "
        "without starting an external server. Caches the loaded app module for reuse."
    )
    args_schema: Type[BaseModel] = TestClientInput

    # Class-level cache so we only load the app module once
    _loaded_app_module = None

    def _load_app_module(self):
        """
        Loads Output/app.py with importlib, caches the result in _loaded_app_module.
        Also updates sys.path so 'models.py' in Output can be found.
        """
        if self._loaded_app_module is not None:
            return self._loaded_app_module  # Already loaded

        app_path = os.path.join("Output", "app.py")
        if not os.path.exists(app_path):
            raise FileNotFoundError("Output/app.py not found, cannot run tests.")

        # 1) Output in sys.path, damit "from models import ..." funktioniert
        if "Output" not in sys.path:
            sys.path.insert(0, "Output")

        # 2) Dynamisch "app.py" laden
        spec = importlib.util.spec_from_file_location("app_module", app_path)
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)

        # 3) Check if we have app and db in that module
        if not hasattr(app_module, "app") or not hasattr(app_module, "db"):
            raise AttributeError("app_module does not contain 'app' or 'db' attributes.")

        # Optional: create tables once
        with app_module.app.app_context():
            app_module.db.create_all()

        # 4) Cache the module so next time we skip the import
        self._loaded_app_module = app_module
        return app_module

    def _make_request(self, app, db, route: str, method: str, json_data: dict):
        """
        Helper method to perform the actual request using Flask test_client().
        """
        client = app.test_client()

        method = method.upper()
        if method == "GET":
            resp = client.get(route)
        elif method == "POST":
            resp = client.post(route, json=json_data)
        elif method == "PUT":
            resp = client.put(route, json=json_data)
        elif method == "DELETE":
            resp = client.delete(route)
        else:
            return f"Error: HTTP method {method} not supported."

        return f"Status: {resp.status_code}, Body: {resp.data.decode('utf-8')}"

    def _run(self, route: str, method: str = "GET", json_data: dict = None) -> str:
        """
        Main entry point for the tool. Uses the cached app module, or loads it if needed.
        Then calls _make_request() to do the actual test request.
        """
        try:
            app_module = self._load_app_module()
        except (FileNotFoundError, AttributeError) as e:
            return f"Error loading app.py: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

        app = app_module.app
        db = app_module.db

        # Actually perform the request
        result = self._make_request(app, db, route, method, json_data)
        return result
