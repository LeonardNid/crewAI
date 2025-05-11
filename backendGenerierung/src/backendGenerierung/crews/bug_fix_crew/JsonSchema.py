from typing import Optional
from pydantic import BaseModel

from backendGenerierung.tools.json_patch_tool import JsonPatchToolInput

class fix_code_task_output(BaseModel):
    models: Optional[JsonPatchToolInput]
    routes: Optional[JsonPatchToolInput]
