{
  "models": null,
  "routes": {
    "file_path": "Output/backendCrew/routes.json",
    "patch": [
      {
        "op": "replace",
        "path": "/endpoints/5/branches/PUT",
        "value": "from datetime import date\nobj = Member.query.get(id)\nif not obj:\n    return jsonify({\"message\": \"Member not found\"}), 404\ndata = request.get_json()\nif 'membership_expiry_date' in data:\n    data['membership_expiry_date'] = date.fromisoformat(data['membership_expiry_date'])\nfor k, v in data.items():\n    setattr(obj, k, v)\ndb.session.commit()\nreturn jsonify(obj.to_dict())",
        "from_path": null
      },
      {
        "op": "replace",
        "path": "/endpoints/7/branches/PUT",
        "value": "from datetime import date\nobj = Loan.query.get(id)\nif not obj:\n    return jsonify({\"message\": \"Loan not found\"}), 404\ndata = request.get_json()\nif 'checkout_date' in data:\n    data['checkout_date'] = date.fromisoformat(data['checkout_date'])\nif 'due_date' in data:\n    data['due_date'] = date.fromisoformat(data['due_date'])\nfor k, v in data.items():\n    setattr(obj, k, v)\ndb.session.commit()\nreturn jsonify(obj.to_dict())",
        "from_path": null
      }
    ]
  }
}