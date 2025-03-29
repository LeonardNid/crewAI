```markdown
# Test Report

## /teams Endpoints
- **GET /teams** -> 200 OK, returned [{"city":"London","country":"UK","id":1,"name":"Dream Team","stadium":"Stadium of Dreams"}].
- **POST /teams** -> 201 Created, returned {"city":"Paris","country":"France","id":2,"name":"New Team","stadium":"Parc des Princes"}.
- **GET /teams/2** -> 200 OK, returned {"city":"Paris","country":"France","id":2,"name":"New Team","stadium":"Parc des Princes"}.
- **PUT /teams/2** -> 200 OK, returned {"city":"Marseille","country":"France","id":2,"name":"Updated Team","stadium":"Stade Vélodrome"}.
- **DELETE /teams/2** -> 200 OK, returned {"message":"Team deleted successfully"}.

## /players Endpoints
- **GET /players** -> 200 OK, returned [].
- **POST /players** -> 201 Created, returned {"country":"USA","id":1,"name":"John Doe","position":"Forward","team_id":1}.
- **GET /players/1** -> 200 OK, returned {"country":"USA","id":1,"name":"John Doe","position":"Forward","team_id":1}.
- **PUT /players/1** -> 200 OK, returned {"country":"USA","id":1,"name":"John Smith","position":"Midfielder","team_id":1}.
- **DELETE /players/1** -> 200 OK, returned {"message":"Player deleted successfully"}.
```