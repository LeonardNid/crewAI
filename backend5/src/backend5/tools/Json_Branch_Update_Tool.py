import json
import os
import textwrap
from typing import Any, Dict, List, Type, ClassVar, Set

from pydantic import BaseModel, Field, field_validator
from crewai.tools import BaseTool

"""JsonBranchUpdateTool v4 — *clean* route-only API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Updates branch code in **Output/backendCrew/routes.json**.

The legacy dot-notation is **removed**.  Each edit must now specify:
* `path`     - the exact route string as it appears in routes.json
* `method`   - required HTTP verb (uppercase)
* `new_code` - full multiline replacement string

Example input:
```jsonc
{
  "edits": [
    {
      "path": "/players/team/<int:team_id>",
      "method": "GET",
      "reason": "..."
      "new_code": "..."
    }
  ]
}
```
"""

# ---------------------------------------------------------------------------
#  Constants
# ---------------------------------------------------------------------------

_FILE_PATH: str = "Output/backendCrew/routes.json"
_ALLOWED_METHODS: Set[str] = {"GET", "POST", "PUT", "DELETE", "PATCH"}

# ---------------------------------------------------------------------------
#  Pydantic schema
# ---------------------------------------------------------------------------

class BranchEdit(BaseModel):
    path: str = Field(..., description="Exact route path from routes.json")
    method: str = Field(..., description="HTTP method, e.g. GET, POST … (uppercase)")
    reason: str = Field(..., description="Reason for the edit")
    new_code: str = Field(..., description="Replacement code for the branch")

    @field_validator("path")
    def non_empty_path(cls, v: str):
        if not v:
            raise ValueError("path cannot be empty")
        return v

    @field_validator("method")
    def valid_method(cls, v: str):
        vv = v.upper()
        if vv not in _ALLOWED_METHODS:
            raise ValueError(f"Unsupported HTTP method '{v}'.")
        return vv

class JsonBranchUpdateInput(BaseModel):
    edits: List[BranchEdit]

# ---------------------------------------------------------------------------
#  Tool implementation
# ---------------------------------------------------------------------------

class JsonBranchUpdateTool(BaseTool):
    name: str = "json_branch_update"
    description: str = (
        "Replace code inside existing GET/POST/PUT/DELETE branches in the fixed."
        "file 'Output/backendCrew/routes.json'." \
        "BranchEdit:"
        "path: str = Field(..., description=\"Exact route path from routes.json\")"
        "method: str = Field(..., description=\"HTTP method, e.g. GET, POST … (uppercase)\")"
        "reason: str = Field(..., description=\"Reason for the edit\")"
        "new_code: str = Field(..., description=\"Replacement code for the branch\")"
    )
    args_schema: Type[BaseModel] = JsonBranchUpdateInput

    _cache: Dict[str, Any] = {}

    # ----------------------------------------------------------------------
    #  Helpers
    # ----------------------------------------------------------------------

    def _load_json(self) -> Any:
        if _FILE_PATH in self._cache:
            return self._cache[_FILE_PATH]
        if not os.path.exists(_FILE_PATH):
            raise FileNotFoundError(_FILE_PATH)
        with open(_FILE_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self._cache[_FILE_PATH] = data
        return data

    def _save_json(self, data: Any):
        os.makedirs(os.path.dirname(_FILE_PATH) or ".", exist_ok=True)
        with open(_FILE_PATH, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=4, ensure_ascii=False)
        self._cache[_FILE_PATH] = data

    # ----------------------------------------------------------------------
    #  Core
    # ----------------------------------------------------------------------

    def _run(self, edits: List[Dict[str, str]]):
        print("Using Tool: json_branch_update (route-only)")
        input_obj = JsonBranchUpdateInput(edits=edits)

        try:
            data = self._load_json()
        except Exception as exc:
            return f"❌ Error loading JSON file: {exc}"

        endpoints = data.get("endpoints", [])
        modified: List[str] = []

        for edit in input_obj.edits:
            # locate endpoint by path
            idx = next((i for i, ep in enumerate(endpoints) if ep.get("path") == edit.path), -1)
            if idx == -1:
                return f"❌ No endpoint with path '{edit.path}' found"

            endpoint = endpoints[idx]
            if edit.method not in endpoint.get("methods", []):
                return f"❌ Endpoint '{edit.path}' does not define method {edit.method}"
            if edit.method not in endpoint.get("branches", {}):
                return f"❌ Branch '{edit.method}' not found for endpoint '{edit.path}'"

            endpoint["branches"][edit.method] = edit.new_code
            modified.append(f"{edit.path}#{edit.method}:\n{edit.reason}:\n{edit.new_code}\n")

        try:
            self._save_json(data)
        except Exception as exc:
            return f"❌ Error saving JSON: {exc}"

        return textwrap.dedent(
            f"""
            ✅ Branch code updated successfully.
            {modified}
            """
        )
