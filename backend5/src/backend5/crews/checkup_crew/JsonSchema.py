from typing import List, Optional
from pydantic import BaseModel

# verification

class Verification(BaseModel):
    retry: bool
    defects: List[str]