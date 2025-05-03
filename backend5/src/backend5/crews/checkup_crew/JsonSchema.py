from typing import Any, Dict, List, Optional, Type, Literal
from pydantic import BaseModel, Field

# verification

class Verification(BaseModel):
    retry: bool
    defects: List[str]