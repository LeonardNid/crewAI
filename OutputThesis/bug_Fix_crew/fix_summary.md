{
  "models": {
    "file_path": "Output/backendCrew/models.json",
    "patch": [
      {
        "op": "replace",
        "path": "/topic",
        "value": "Thesis Management",
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/models/8/columns",
        "value": [
          {
            "name": "id",
            "type": "db.Integer, primary_key=True, autoincrement=True",
            "description": "Unique identifier for the reminder period"
          },
          {
            "name": "user_id",
            "type": "db.Integer, db.ForeignKey('users.id'), nullable=True",
            "description": "User ID for user-specific reminder period (nullable for global)"
          },
          {
            "name": "thesis_id",
            "type": "db.Integer, db.ForeignKey('theses.id'), nullable=True",
            "description": "Thesis ID for thesis-specific override reminder period (optional)"
          },
          {
            "name": "days_before_deadline",
            "type": "db.Integer, nullable=False",
            "description": "Number of days before deadline when reminder should trigger"
          },
          {
            "name": "deadline_id",
            "type": "db.Integer, db.ForeignKey('deadlines.id'), nullable=True",
            "description": "Foreign key to deadlines table to establish relationship with Deadline"
          }
        ],
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/models/8/relationship_lines",
        "value": [
          "user = db.relationship(",
          "    'User',",
          "    back_populates='reminderperiods',",
          "    lazy=True",
          ")",
          "thesis = db.relationship(",
          "    'Thesis',",
          "    back_populates='reminderperiods',",
          "    lazy=True",
          ")",
          "deadline = db.relationship(",
          "    'Deadline',",
          "    back_populates='reminderperiods',",
          "    lazy=True",
          ")"
        ],
        "from_path": null
      }
    ]
  },
  "routes": null
}