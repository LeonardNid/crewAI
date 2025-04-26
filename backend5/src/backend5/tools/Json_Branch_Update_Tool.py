import json
import os
import re
from typing import Any, ClassVar, Dict, List, Type

from pydantic import BaseModel, Field, field_validator
from crewai.tools import BaseTool

"""
JsonBranchUpdateTool - fixed-path variant (Pydantic v2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This lightweight tool **exclusively** replaces the code strings inside
`branches` entries (e.g. `endpoints[2].branches.GET`) of the single file
``Output/backendCrew/routes.json``.

* It **cannot** add or remove endpoints - only update existing branch code.
* The file path is hard-wired; the agent supplies **only** the edits.
* Multiple replacements can be performed in one call.

Updated to **Pydantic v2**: `@validator` ➔ `@field_validator`.
"""

# ────────────────────────────────────────────────────────────────────────────────
#  Constants
# ────────────────────────────────────────────────────────────────────────────────

_FILE_PATH = "Output/backendCrew/routes.json"

# ────────────────────────────────────────────────────────────────────────────────
#  Pydantic input schema
# ────────────────────────────────────────────────────────────────────────────────

class BranchEdit(BaseModel):
    """Describe a single branch-code replacement."""

    path: str = Field(
        ...,
        description=(
            "Path in the form `endpoints[<index>].branches.<METHOD>`, e.g. "
            "`endpoints[3].branches.PUT`. <METHOD> must be uppercase."
            "The first enpoint index is 0."
        ),
    )
    new_code: str = Field(
        ..., description="The *complete* multiline code string to store in that branch."
    )

    _PATH_RE: ClassVar[re.Pattern[str]] = re.compile(
        r"^endpoints\[(\d+)\]\.branches\.([A-Z]+)$"
    )

    @field_validator("path")  # Pydantic v2 style
    def validate_path(cls, v: str):  # noqa: N805 - pydantic naming
        if not cls._PATH_RE.fullmatch(v):
            raise ValueError(
                "Path must match 'endpoints[<int>].branches.<METHOD>' with METHOD uppercase"
            )
        return v


class JsonBranchUpdateInput(BaseModel):
    edits: List[BranchEdit] = Field(
        ..., description="List of branch replacements to apply sequentially."
    )


# ────────────────────────────────────────────────────────────────────────────────
#  Tool implementation
# ────────────────────────────────────────────────────────────────────────────────

class JsonBranchUpdateTool(BaseTool):
    """Replace branch code in routes.json with minimal overhead."""

    name: str = "json_branch_update"
    description: str = (
        "Replace the code inside existing GET/POST/PUT/DELETE branches in the fixed "
        "file 'Output/backendCrew/routes.json'. The tool takes a list of "
        "{path, new_code} edit objects and performs all replacements in a single call."
    )
    args_schema: Type[BaseModel] = JsonBranchUpdateInput

    # process-wide cache to avoid re-reading when called repeatedly in one run
    _cache: Dict[str, Any] = {}

    _INDEX_METHOD_RE: ClassVar[re.Pattern[str]] = re.compile(
        r"^endpoints\[(\d+)\]\.branches\.([A-Z]+)$"
    )

    # ────────────────────────────────────────────────────────────────────────────
    #  File helpers
    # ────────────────────────────────────────────────────────────────────────────

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

    # ────────────────────────────────────────────────────────────────────────────
    #  Core logic
    # ────────────────────────────────────────────────────────────────────────────

    def _run(self, edits: List[Dict[str, str]]):  # noqa: N802 - BaseTool API expects snake case
        print("Using Tool: json_branch_update")
        input_obj = JsonBranchUpdateInput(edits=edits)

        try:
            data = self._load_json()
        except Exception as exc:
            return f"❌ Error loading JSON file: {exc}"

        modified: List[str] = []
        for edit in input_obj.edits:
            match = self._INDEX_METHOD_RE.fullmatch(edit.path)
            if not match:
                return f"❌ Invalid path (should never happen after validation): {edit.path}"
            idx, method = int(match.group(1)), match.group(2)

            # Ensure endpoint index exists
            if idx >= len(data.get("endpoints", [])):
                return f"❌ No endpoint at index {idx}"
            endpoint = data["endpoints"][idx]
            branches = endpoint.get("branches")
            if branches is None or method not in branches:
                return f"❌ Branch '{method}' not found in endpoint[{idx}]"

            endpoint["branches"][method] = edit.new_code
            modified.append(f"endpoint[{idx}].{method}")

        try:
            self._save_json(data)
        except Exception as exc:
            return f"❌ Error saving JSON: {exc}"

        return (
            "✅ Branch code updated successfully.\n" +
            "Modified: " + ", ".join(modified)
        )
