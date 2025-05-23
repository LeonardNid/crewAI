{
  "models": null,
  "routes": {
    "file_path": "Output/backendCrew/routes.json",
    "patch": [
      {
        "op": "replace",
        "path": "/endpoints/24/branches/PUT",
        "value": "obj = DiscountDistribution.query.get(id)\nif not obj:\n    return jsonify({'message': 'DiscountDistribution not found'}), 404\nfrom datetime import datetime\n\ndata = request.get_json()\ntry:\n    valid_from_str = data.get('valid_from')\n    valid_to_str = data.get('valid_to')\n    data['valid_from'] = datetime.strptime(valid_from_str, '%Y-%m-%d').date() if valid_from_str else None\n    data['valid_to'] = datetime.strptime(valid_to_str, '%Y-%m-%d').date() if valid_to_str else None\nexcept Exception:\n    return jsonify({'message': 'Invalid date format'}), 400\nfor k,v in data.items():\n    setattr(obj,k,v)\ndb.session.commit()\nreturn jsonify(obj.to_dict())",
        "from_path": null
      }
    ]
  }
}