{
  "models": {
    "file_path": "Output/backendCrew/models.json",
    "patch": [
      {
        "op": "replace",
        "path": "/models/0/relationship_lines/4",
        "value": "theses = db.relationship(\n    'Thesis',\n    back_populates='user',\n    lazy='select',\n    foreign_keys=[Thesis.user_id]\n)",
        "from_path": null
      }
    ]
  },
  "routes": null
}