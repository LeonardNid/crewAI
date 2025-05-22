{
  "models": {
    "file_path": "Output/backendCrew/models.json",
    "patch": [
      {
        "op": "add",
        "path": "/models/1/relationships/-",
        "value": {
          "target_model": "Rental",
          "rel_type": "one_to_many",
          "cascade": null
        },
        "from_path": null
      },
      {
        "op": "add",
        "path": "/models/1/relationship_lines/-",
        "value": "rentals = db.relationship(\n    'Rental',\n    primaryjoin=\"or_(Location.id==Rental.pickup_location_id, Location.id==Rental.dropoff_location_id)\",\n    foreign_keys=[Rental.pickup_location_id, Rental.dropoff_location_id],\n    lazy=True\n)",
        "from_path": null
      }
    ]
  },
  "routes": null
}