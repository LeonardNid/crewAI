### POST /teams
Payload: {"name": "Test FC", "city": "Berlin", "country": "Germany", "stadium": "Olympiastadion"}
Result: ✅ 201 Created
Response: { "city": "Berlin", "country": "Germany", "id": 1, "name": "Test FC", "stadium": "Olympiastadion" }

### POST /players
Payload: {"name": "John Doe", "position": "Forward", "team_id": 1, "country": "Germany"}
Result: ✅ 201 Created
Response: { "country": "Germany", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 }

### GET /teams
Payload: None
Result: ✅ 200 OK
Response: [ { "city": "Berlin", "country": "Germany", "id": 1, "name": "Test FC", "stadium": "Olympiastadion" } ]

### GET /teams/1
Payload: None
Result: ✅ 200 OK
Response: { "city": "Berlin", "country": "Germany", "id": 1, "name": "Test FC", "stadium": "Olympiastadion" }

### GET /players
Payload: None
Result: ✅ 200 OK
Response: [ { "country": "Germany", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 } ]

### GET /players/1
Payload: None
Result: ✅ 200 OK
Response: { "country": "Germany", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 }

### GET /teams/1/players
Payload: None
Result: ✅ 200 OK
Response: [ { "country": "Germany", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 } ]

### GET /players/country/Germany
Payload: None
Result: ✅ 200 OK
Response: [ { "country": "Germany", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 } ]

### PUT /teams/1
Payload: {"name": "Updated FC", "city": "Berlin", "country": "Germany", "stadium": "Olympiastadion"}
Result: ✅ 200 OK
Response: { "city": "Berlin", "country": "Germany", "id": 1, "name": "Updated FC", "stadium": "Olympiastadion" }

### PUT /players/1
Payload: {"name": "John Doe Updated", "position": "Midfielder", "team_id": 1, "country": "Germany"}
Result: ✅ 200 OK
Response: { "country": "Germany", "id": 1, "name": "John Doe Updated", "position": "Midfielder", "team_id": 1 }

### DELETE /teams/1
Payload: None
Result: ❌ 500 Internal Server Error
Response: Internal Server Error: The server encountered an internal error and was unable to complete your request.

### DELETE /players/1
Payload: None
Result: ✅ 200 OK
Response: { "message": "Player deleted successfully" }