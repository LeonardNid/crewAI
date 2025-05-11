from typing import List, Optional
from pydantic import BaseModel, model_validator

class Column(BaseModel):
    name: str                 # z. B. "id"
    type: str                 # z. B. "Integer, primary_key=True"
    description: Optional[str]

class Relationship(BaseModel):
    target_model: str         # z. B. "Team"
    rel_type: str             # "one_to_many", "many_to_one", "many_to_many"
    cascade: Optional[str]              # z. B. "all, delete-orphan"

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
    get_List: bool                # True, False
    json_body: Optional[dict]     # erwartete Felder bei POST/PUT
    description: Optional[str]

class RoutesPlan(BaseModel):
    """Top-level container returned by *routes_json_task*."""
    topic: str
    endpoints: List[Endpoint]

    @model_validator(mode="after")
    def _unique_paths(cls, model):  # noqa: N805  (classmethod name)
        paths_seen: set[str] = set()
        duplicates: list[str] = []
        for ep in model.endpoints:
            if ep.path in paths_seen:
                duplicates.append(ep.path)
            else:
                paths_seen.add(ep.path)
        if duplicates:
            dup_list = ", ".join(sorted(set(duplicates)))
            raise ValueError(
                f"Duplicate path detected in routes.json: {dup_list}. "
                "Merge all HTTP verbs for the same URL into one endpoint object."
            )
        return model

