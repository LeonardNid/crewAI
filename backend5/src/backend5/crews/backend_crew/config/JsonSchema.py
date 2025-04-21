# common_models.py  (nur einmal definieren)

from typing import List, Optional
from pydantic import BaseModel

class Column(BaseModel):
    name: str                 # z. B. "id"
    type: str                 # z. B. "Integer, primary_key=True"
    description: Optional[str]

class Relationship(BaseModel):
    target_model: str         # z. B. "Team"
    rel_type: str             # "one_to_many", "many_to_one", ...
    fk_column: str            # z. B. "team_id"
    backref: Optional[str]    # optionales backref‑Feld

class ModelSchema(BaseModel):
    name: str                 # "Player"
    table: str                # "players"
    columns: List[Column]
    relationships: List[Relationship] = []

class ModelsPlan(BaseModel):
    topic: str                # "Football"
    models: List[ModelSchema]

# RoutesPlan

class Endpoint(BaseModel):
    path: str                     # "/players/<int:id>"
    methods: List[str]            # ["GET", "PUT", "DELETE"]
    model: str                    # "Player"
    json_body: Optional[dict]     # erwartete Felder bei POST/PUT
    description: Optional[str]

class RoutesPlan(BaseModel):
    topic: str
    endpoints: List[Endpoint]
