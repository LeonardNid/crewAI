1. POST /teams -> Needs { name: string, city: string, country: string, stadium: string } 
   Returns the newly created team data.
2. POST /players -> Needs { name: string, position: string, team_id: integer, country: string } 
   Returns the newly created player data.
3. GET /teams 
   Returns a list of all teams.
4. GET /teams/<id> 
   Returns the team data for the specified id.
5. GET /players 
   Returns a list of all players.
6. GET /players/<id> 
   Returns the player data for the specified id.
7. GET /teams/<id>/players 
   Returns a list of players belonging to the specified team.
8. GET /players/country/<country> 
   Returns a list of players from the specified country.
9. PUT /teams/<id> -> Needs { name: string, city: string, country: string, stadium: string } 
   Returns the updated team data.
10. PUT /players/<id> -> Needs { name: string, position: string, team_id: integer, country: string } 
    Returns the updated player data.
11. DELETE /teams/<id>
    Returns a success message if the team is deleted.
12. DELETE /players/<id>
    Returns a success message if the player is deleted.