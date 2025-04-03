1. POST /teams -> Needs { id: string, name: string, city: string, country: string, stadium: string } 
   Returns the newly created team data.
   
2. POST /players -> Needs { id: string, name: string, position: string, team_id: string, country: string } 
   Returns the newly created player data.

3. GET /teams -> Returns a list of all teams.

4. GET /teams/<id> -> Returns the team data for the specified id.

5. GET /players -> Returns a list of all players.

6. GET /players/<id> -> Returns the player data for the specified id.

7. PUT /teams/<id> -> Needs { name: string, city: string, country: string, stadium: string } 
   Returns the updated team data.

8. PUT /players/<id> -> Needs { name: string, position: string, team_id: string, country: string } 
   Returns the updated player data.

9. DELETE /teams/<id> -> Returns { message: 'Team deleted successfully' }.

10. DELETE /players/<id> -> Returns { message: 'Player deleted successfully' }.