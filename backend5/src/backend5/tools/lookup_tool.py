import os
import json
from difflib import SequenceMatcher
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class DataObjectLookupInput(BaseModel):
    query: str = Field(..., description="Keyword or phrase to look up (e.g., 'home', 'residence', 'contact', 'role').")

class DataObjectLookupTool(BaseTool):
    name: str = "data_object_lookup"
    description: str = "Returns the fields of the most commonly used data objects based on a given keyword."
    args_schema: Type[BaseModel] = DataObjectLookupInput

    # wir halten die JSON-Daten im Speicher, damit wir nicht jedes Mal neu laden müssen
    _cached_data: List[Dict[str, Any]] = []

    def _load_data(self):
        """Load the JSON file once, store in _cached_data."""
        if self._cached_data:
            return self._cached_data  # already loaded

        file_path = os.path.join("files", "common_Data_Objects.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found at {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._cached_data = data
        return self._cached_data
    
    def similarity(self, a: str, b: str) -> float:
        """Returns a float ratio between 0 and 1 indicating how similar 'a' and 'b' are."""
        return SequenceMatcher(None, a, b).ratio()

    def _run(self, query: str):
        print("Using Tool: data_object_lookup")
        # 1) load Data
        try:
            data = self._load_data()
        except Exception as e:
            return f"Error loading JSON data: {str(e)}"

        # 2) Search in Data for fuzzy match
        query_lower = query.lower()
        threshold = 0.6

        matches = []
        for obj in data:
            # Check the 'name' field
            obj_name = obj.get("name", "").lower()
            name_score = self.similarity(obj_name, query_lower)

            # Check synonyms
            synonyms = obj.get("synonyms", [])
            best_syn_score = 0.0
            for syn in synonyms:
                syn_score = self.similarity(syn.lower(), query_lower)
                if syn_score > best_syn_score:
                    best_syn_score = syn_score

            # If either 'name' or any 'synonym' crosses the threshold, consider it a match
            if name_score >= threshold or best_syn_score >= threshold:
                matches.append(obj)


        # 3) Result
        if matches:
            return json.dumps(matches, indent=2)
        else:
            return f"No data objects found matching query '{query}'"
