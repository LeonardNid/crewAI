[
  {
    "method": "POST",
    "route": "/teams",
    "status_code": 201,
    "response": "{\"city\":\"Berlin\",\"country\":\"Germany\",\"id\":2,\"name\":\"Test FC\",\"stadium\":\"Olympiastadion\"}\n"
  },
  {
    "method": "POST",
    "route": "/players",
    "status_code": 201,
    "response": "{\"country\":\"Germany\",\"id\":1,\"name\":\"John Doe\",\"position\":\"Forward\",\"team_id\":1}\n"
  },
  {
    "method": "GET",
    "route": "/teams",
    "status_code": 200,
    "response": "[{\"city\":\"Berlin\",\"country\":\"Germany\",\"id\":1,\"name\":\"Updated Test FC\",\"stadium\":\"Olympiastadion\"},{\"city\":\"Berlin\",\"country\":\"Germany\",\"id\":2,\"name\":\"Test FC\",\"stadium\":\"Olympiastadion\"}]\n"
  },
  {
    "method": "GET",
    "route": "/players",
    "status_code": 200,
    "response": "[{\"country\":\"Germany\",\"id\":1,\"name\":\"John Doe\",\"position\":\"Forward\",\"team_id\":1}]\n"
  },
  {
    "method": "GET",
    "route": "/teams/1",
    "status_code": 200,
    "response": "{\"city\":\"Berlin\",\"country\":\"Germany\",\"id\":1,\"name\":\"Updated Test FC\",\"stadium\":\"Olympiastadion\"}\n"
  },
  {
    "method": "GET",
    "route": "/players/1",
    "status_code": 200,
    "response": "{\"country\":\"Germany\",\"id\":1,\"name\":\"John Doe\",\"position\":\"Forward\",\"team_id\":1}\n"
  },
  {
    "method": "GET",
    "route": "/teams/1/players",
    "status_code": 200,
    "response": "[{\"country\":\"Germany\",\"id\":1,\"name\":\"John Doe\",\"position\":\"Forward\",\"team_id\":1}]\n"
  },
  {
    "method": "GET",
    "route": "/players/country/Germany",
    "status_code": 200,
    "response": "[{\"country\":\"Germany\",\"id\":1,\"name\":\"John Doe\",\"position\":\"Forward\",\"team_id\":1}]\n"
  },
  {
    "method": "PUT",
    "route": "/teams/1",
    "status_code": 200,
    "response": "{\"city\":\"Berlin\",\"country\":\"Germany\",\"id\":1,\"name\":\"Updated Test FC\",\"stadium\":\"Updated Olympiastadion\"}\n"
  },
  {
    "method": "PUT",
    "route": "/players/1",
    "status_code": 200,
    "response": "{\"country\":\"Germany\",\"id\":1,\"name\":\"Jane Doe\",\"position\":\"Midfielder\",\"team_id\":1}\n"
  },
  {
    "method": "DELETE",
    "route": "/teams/1",
    "status_code": 400,
    "response": "{\"error\":\"Cannot delete team with active players.\"}\n"
  },
  {
    "method": "DELETE",
    "route": "/players/1",
    "status_code": 200,
    "response": "{\"message\":\"Player deleted successfully\"}\n"
  }
]