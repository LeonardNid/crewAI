import os
import sys
import importlib.util
import json
import time
import traceback
from typing import Type, List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from crewai.tools import BaseTool


# -------------------- Pydantic request schemas --------------------

class SingleRequest(BaseModel):
    route: str = Field(..., description="Full URL path to call, e.g. '/teams' or '/players/1'.")
    method: str = Field(..., description="HTTP verb for this call (GET, POST, PUT, DELETE …).")
    json_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional JSON payload to send with POST/PUT; "
                    "omit or use `null` for GET/DELETE."
    )


class BulkTestClientInput(BaseModel):
    requests: List[SingleRequest] = Field(..., description="Ordered list of SingleRequest objects to execute.")



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
        

        try:
            spec.loader.exec_module(app_module)
        except SyntaxError as e:
                error_type = type(e).__name__
                error_msg = str(e)
                return (
                    "Python code is not executable!\n"
                    f"{error_type}: {error_msg}\n"
                    "Please fix the Output/app.py or Output/models.py file so that it contains clean, valid Python code."
                )

        app_module.app.testing = True
        with app_module.app.app_context():
            app_module.db.create_all()

        return app_module.app

    def _run(self, requests: List[dict]) -> str:
        print("Using Tool: flask_test_client")
        # Validate all requests using Pydantic
        try:
            validated_requests = [SingleRequest(**r) if isinstance(r, dict) else r for r in requests]
        except ValidationError as ve:
            example = {
                "requests": [
                    {
                        "method": "POST",
                        "route": "/teams",
                        "json_data": {
                            "name": "FC Test",
                            "city": "Berlin",
                            "country": "Germany",
                            "stadium": "Olympiastadion"
                        }
                    }
                ]
            }
            return (
                f"Validation failed: {ve}\n\n"
                "🔧 Make sure each request contains at least:\n"
                "- 'method': one of GET, POST, PUT, DELETE\n"
                "- 'route': the URL path (e.g., '/teams')\n"
                "- Optional: 'json_data' as a JSON object for POST/PUT\n\n"
                f"Example input:\n{json.dumps(example, indent=2)}"
            )


        app = self._load_app_module()
        if isinstance(app, str):
            return app
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
                    "json_data": req.json_data,
                    "status_code": resp.status_code,
                    "response": resp.data.decode("utf-8")
                })
            
                time.sleep(0.2)

            except Exception as e:
                short_err = traceback.format_exception_only(type(e), e)[-1].strip()

                results.append({
                    "method": method,
                    "route": req.route,
                    "json_data": req.json_data,
                    "status_code": 500,
                    "error":  short_err
                })

        return json.dumps(results, indent=2)
