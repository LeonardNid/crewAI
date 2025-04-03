1. GET / -> returns a message indicating the API is running.
2. POST /teams -> needs {
    name: string,
    city: string,
    country: string,
    stadium: string
   }
3. GET /teams -> returns a list of all teams.
4. GET /teams/<id> -> returns details of a specific team by ID.
5. PUT /teams/<id> -> needs at least one of the following fields to update: {
    name: string,
    city: string,
    country: string,
    stadium: string
   }
6. DELETE /teams/<id> -> deletes a specific team by ID.
7. POST /players -> needs {
    name: string,
    position: string,
    country: string,
    team_id: integer
   }
8. GET /players -> returns a list of all players.
9. GET /players/<id> -> returns details of a specific player by ID.
10. PUT /players/<id> -> needs at least one of the following fields to update: {
    name: string,
    position: string,
    country: string,
    team_id: integer
   }
11. DELETE /players/<id> -> deletes a specific player by ID.
12. GET /teams/<team_id>/players -> returns a list of players for a specific team by team ID.
13. GET /players/country/<country> -> returns a list of players from a specific country.