1. POST /teams -> Needs { name: string, city: string, country: string, stadium: string } 
   Returns the newly created team data.
2. POST /players -> Needs { name: string, position: string, country: string, team_id: integer } 
   Returns the newly created player data.
3. GET /teams -> 
   Returns a list of all teams.
4. GET /players -> 
   Returns a list of all players.
5. GET /teams/<id> -> 
   Returns the team data for the specified ID.
6. GET /players/<id> -> 
   Returns the player data for the specified ID.
7. GET /teams/<id>/players -> 
   Returns a list of players associated with the specified team ID.
8. GET /players/country/<country> -> 
   Returns a list of players from the specified country.
9. PUT /teams/<id> -> Needs { name: string, city: string, country: string, stadium: string } (any of these can be omitted to keep current values) 
   Returns the updated team data.
10. PUT /players/<id> -> Needs { name: string, position: string, country: string, team_id: integer } (any of these can be omitted to keep current values) 
    Returns the updated player data.
11. DELETE /teams/<id> -> 
    Returns a message indicating success or error if the team is not found or has active players.
12. DELETE /players/<id> -> 
    Returns a message indicating success or error if the player is not found.