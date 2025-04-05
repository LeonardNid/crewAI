### POST /teams
Payload: {"name": "Test FC", "city": "Berlin", "country": "Germany", "stadium": "Olympiastadion"}
Result: ✅ 201 Created
Response: { "city": "Berlin", "country": "Germany", "id": 1, "name": "Test FC", "stadium": "Olympiastadion" }

### POST /players
Payload: {"name": "John Doe", "position": "Forward", "team_id": 1, "country": "USA"}
Result: ✅ 201 Created
Response: { "country": "USA", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 }

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
Response: [ { "country": "USA", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 } ]

### GET /players/1
Payload: None
Result: ✅ 200 OK
Response: { "country": "USA", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 }

### GET /teams/1/players
Payload: None
Result: ✅ 200 OK
Response: [ { "country": "USA", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 } ]

### GET /players/country/USA
Payload: None
Result: ✅ 200 OK
Response: [ { "country": "USA", "id": 1, "name": "John Doe", "position": "Forward", "team_id": 1 } ]

### PUT /teams/1
Payload: {"name": "Updated FC", "city": "Berlin", "country": "Germany", "stadium": "Olympiastadion"}
Result: ✅ 200 OK
Response: { "city": "Berlin", "country": "Germany", "id": 1, "name": "Updated FC", "stadium": "Olympiastadion" }

### PUT /players/1
Payload: {"name": "John Doe", "position": "Striker", "team_id": 1, "country": "USA"}
Result: ✅ 200 OK
Response: { "country": "USA", "id": 1, "name": "John Doe", "position": "Striker", "team_id": 1 }

### DELETE /teams/1
Payload: None
Result: ✅ 200 OK
Response: { "message": "Team deleted successfully" }

### DELETE /players/1
Payload: None
Result: ✅ 200 OK
Response: { "message": "Player deleted successfully" }