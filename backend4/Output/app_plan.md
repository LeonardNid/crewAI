### Routes Plan

1. **Get All Teams**
   - **Method**: GET
   - **Endpoint**: `/teams`
   - **Request Body**: None
   - **Response**: A list of all teams with their details (id, name, city, country, stadium).

2. **Get Specific Team**
   - **Method**: GET
   - **Endpoint**: `/teams/<id>`
   - **Request Body**: None
   - **Response**: Details of the team with the specified id (id, name, city, country, stadium).

3. **Create a New Team**
   - **Method**: POST
   - **Endpoint**: `/teams`
   - **Request Body**: 
     ```json
     {
       "name": "string",
       "city": "string",
       "country": "string",
       "stadium": "string"
     }
     ```
   - **Response**: Details of the created team, including the generated id.

4. **Update a Team**
   - **Method**: PUT
   - **Endpoint**: `/teams/<id>`
   - **Request Body**: 
     ```json
     {
       "name": "string",
       "city": "string",
       "country": "string",
       "stadium": "string"
     }
     ```
   - **Response**: Details of the updated team.

5. **Delete a Team**
   - **Method**: DELETE
   - **Endpoint**: `/teams/<id>`
   - **Request Body**: None
   - **Response**: Confirmation that the team has been deleted.

6. **Get All Players**
   - **Method**: GET
   - **Endpoint**: `/players`
   - **Request Body**: None
   - **Response**: A list of all players with their details (id, name, position, team_id, country).

7. **Get Specific Player**
   - **Method**: GET
   - **Endpoint**: `/players/<id>`
   - **Request Body**: None
   - **Response**: Details of the player with the specified id (id, name, position, team_id, country).

8. **Create a New Player**
   - **Method**: POST
   - **Endpoint**: `/players`
   - **Request Body**: 
     ```json
     {
       "name": "string",
       "position": "string",
       "team_id": "integer",
       "country": "string"
     }
     ```
   - **Response**: Details of the created player, including the generated id.

9. **Update a Player**
   - **Method**: PUT
   - **Endpoint**: `/players/<id>`
   - **Request Body**: 
     ```json
     {
       "name": "string",
       "position": "string",
       "team_id": "integer",
       "country": "string"
     }
     ```
   - **Response**: Details of the updated player.

10. **Delete a Player**
    - **Method**: DELETE
    - **Endpoint**: `/players/<id>`
    - **Request Body**: None
    - **Response**: Confirmation that the player has been deleted.

11. **Get Players by Team**
    - **Method**: GET
    - **Endpoint**: `/teams/<team_id>/players`
    - **Request Body**: None
    - **Response**: A list of players that belong to the specified team.

12. **Get Players by Country**
    - **Method**: GET
    - **Endpoint**: `/players/country/<country>`
    - **Request Body**: None
    - **Response**: A list of players from the specified country.