# pip install jsonpatch
import json
import os
from typing import Any, Dict, List, Optional, Type, Literal

import jsonpatch  # RFC-6902 engine
from pydantic import BaseModel, Field, field_validator
from crewai.tools import BaseTool

from backend5.Utils import renderTemplate

"""JsonPatchTool - strict RFC 6902 editor (file path passed per call)

Applies an **RFC 6902 JSON Patch** to an arbitrary JSON file. The *agent* must
provide two parameters:

```jsonc
{
  "file_path": "Output/backendCrew/routes.json",
  "patch": [ { "op": "replace", "path": "/topic", "value": "Soccer" } ]
}
```

* `file_path` **must** end with **`.json`** - the tool rejects other
  extensions.
* `patch` is an array of operations (validated below).
"""

# ---------------------------------------------------------------------------
#  Pydantic models
# ---------------------------------------------------------------------------

class Operation(BaseModel):
    op: Literal["add", "remove", "replace", "move", "copy", "test"]
    path: str = Field(..., description="JSON Pointer location, e.g. /a/b/0")
    value: Optional[Any] = Field(None)
    from_path: Optional[str] = Field(None, alias="from")

    @field_validator("value", mode="after")
    def _validate_value(cls, v, info):
        op = info.data["op"]
        if op in {"add", "replace", "test"} and v is None:
            raise ValueError("'value' required for op add|replace|test")
        if op in {"remove", "move", "copy"} and v is not None:
            raise ValueError("'value' not allowed for op remove|move|copy")
        return v

    @field_validator("from_path", mode="after")
    def _validate_from(cls, v, info):
        op = info.data["op"]
        if op in {"move", "copy"} and v is None:
            raise ValueError("'from' required for op move|copy")
        if op not in {"move", "copy"} and v is not None:
            raise ValueError("'from' only allowed for op move|copy")
        return v

class PatchRequest(BaseModel):
    file_path: str = Field(..., description="Target JSON file path ending with .json")
    patch: List[Operation] = Field(..., description="List of RFC 6902 operations (see docstring table)." 
            "Operation:" 
            f"""    op: Literal["add", "remove", "replace", "move", "copy", "test"]
            path: str = Field(..., description="JSON Pointer to target location")
            value: Optional[Any] = Field(
                None,
                description="The value to add / replace / test against (required for certain ops)",
            )
            from_path: Optional[str] = Field(
                None,
                alias="from",
                description="Source path for move / copy operations",
            )""",
    )

    @field_validator("file_path")
    def _must_be_json(cls, v: str):
        if not v.lower().endswith(".json"):
            raise ValueError("file_path must point to a .json file")
        return v

# ---------------------------------------------------------------------------
#  Tool implementation
# ---------------------------------------------------------------------------

class JsonPatchTool(BaseTool):
    """Apply an RFC-6902 patch to a JSON file specified in the call."""

    name: str = "json_patch_update"
    description: str = (
        "Modify any JSON file by passing `file_path` and a RFC-6902 `patch` array. "
        "`file_path` must end with '.json'."
    )
    args_schema: Type[BaseModel] = PatchRequest

    # helpers ---------------------------------------------------------------
    @staticmethod
    def _load_doc(path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_doc(path: str, doc: Dict[str, Any]):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=4, ensure_ascii=False)

    # core ------------------------------------------------------------------
    def _run(self, file_path: str, patch: List[Dict[str, Any]]):  # noqa: N802
        # loader
        try:
            doc = self._load_doc(file_path)
        except Exception as exc:
            return f"❌ Error loading JSON file: {exc}"

        # apply patch
        try:
            new_doc = jsonpatch.apply_patch(doc, patch, in_place=False)
        except (jsonpatch.JsonPatchConflict, jsonpatch.JsonPointerException) as err:
            return f"❌ Patch failed: {err}"

        # save
        try:
            self._save_doc(file_path, new_doc)
        except Exception as exc:
            return f"❌ Error saving JSON: {exc}"
        
        return f"✅ Patch applied successfully to {file_path}."
