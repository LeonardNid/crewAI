1. GET /teams -> returns a list of teams
2. POST /teams -> needs {
    "name": "string",
    "city": "string",
    "country": "string",
    "stadium": "string"
   }
3. GET /teams/<id> -> returns details of a specific team
4. PUT /teams/<id> -> needs {
    "name": "string",
    "city": "string",
    "country": "string",
    "stadium": "string"
   }
5. DELETE /teams/<id> -> deletes a specific team
  
6. GET /players -> returns a list of players
7. POST /players -> needs {
    "name": "string",
    "position": "string",
    "team_id": "integer",
    "country": "string"
   }
8. GET /players/<id> -> returns details of a specific player
9. PUT /players/<id> -> needs {
    "name": "string",
    "position": "string",
    "team_id": "integer",
    "country": "string"
   }
10. DELETE /players/<id> -> deletes a specific player