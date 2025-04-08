import os
import sys
import importlib.util
import json
import time
from typing import Type, List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError
from crewai.tools import BaseTool


class SingleRequest(BaseModel):
    route: str
    method: str
    json_data: Optional[Dict[str, Any]] = None


class BulkTestClientInput(BaseModel):
    requests: List[SingleRequest]


class FlaskTestClientTool(BaseTool):
    name: str = "flask_test_client"
    description: str = "Test Flask app routes using test_client with passed request definitions."
    args_schema: Type[BaseModel] = BulkTestClientInput

    def _load_app_module(self):
        app_path = os.path.join("Output", "app.py")
        if not os.path.exists(app_path):
            raise FileNotFoundError("Output/app.py not found.")

        if "Output" not in sys.path:
            sys.path.insert(0, "Output")

        spec = importlib.util.spec_from_file_location("app_module", app_path)
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)

        if not hasattr(app_module, "app") or not hasattr(app_module, "db"):
            raise AttributeError("app.py must have 'app' and 'db'")

        with app_module.app.app_context():
            app_module.db.create_all()

        return app_module.app

    def _run(self, requests: List[dict]) -> str:
        # Validate all requests using Pydantic
        try:
            validated_requests = [SingleRequest(**r) if isinstance(r, dict) else r for r in requests]
        except ValidationError as ve:
            return f"❌ Validation failed: {ve}"

        app = self._load_app_module()
        client = app.test_client()
        results = []

        for req in validated_requests:
            method = req.method.upper()
            try:
                if method == "GET":
                    resp = client.get(req.route)
                elif method == "POST":
                    resp = client.post(req.route, json=req.json_data)
                elif method == "PUT":
                    resp = client.put(req.route, json=req.json_data)
                elif method == "DELETE":
                    resp = client.delete(req.route)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                results.append({
                    "method": method,
                    "route": req.route,
                    "status_code": resp.status_code,
                    "response": resp.data.decode("utf-8")
                })
            
                time.sleep(0.2)

            except Exception as e:
                results.append({
                    "method": method,
                    "route": req.route,
                    "error": str(e)
                })

        return json.dumps(results, indent=2)
