### Routes Plan

1. **Teams**
   - **GET /teams**
     - **Description**: Retrieve a list of all teams.
     - **Response**: Returns an array of team objects.

   - **GET /teams/<id>**
     - **Description**: Retrieve a specific team by ID.
     - **Response**: Returns a team object.

   - **POST /teams**
     - **Description**: Create a new team.
     - **Request Body**: 
       ```json
       {
         "name": "string",
         "city": "string",
         "country": "string",
         "stadium": "string"
       }
       ```
     - **Response**: Returns the created team object.

   - **PUT /teams/<id>**
     - **Description**: Update an existing team.
     - **Request Body**: 
       ```json
       {
         "name": "string",
         "city": "string",
         "country": "string",
         "stadium": "string"
       }
       ```
     - **Response**: Returns the updated team object.

   - **DELETE /teams/<id>**
     - **Description**: Delete a specific team by ID.
     - **Response**: Confirmation message or status.

2. **Players**
   - **GET /players**
     - **Description**: Retrieve a list of all players.
     - **Response**: Returns an array of player objects.

   - **GET /players/<id>**
     - **Description**: Retrieve a specific player by ID.
     - **Response**: Returns a player object.

   - **POST /players**
     - **Description**: Create a new player.
     - **Request Body**: 
       ```json
       {
         "name": "string",
         "position": "string",
         "team_id": "integer",
         "country": "string"
       }
       ```
     - **Response**: Returns the created player object.

   - **PUT /players/<id>**
     - **Description**: Update an existing player.
     - **Request Body**: 
       ```json
       {
         "name": "string",
         "position": "string",
         "team_id": "integer",
         "country": "string"
       }
       ```
     - **Response**: Returns the updated player object.

   - **DELETE /players/<id>**
     - **Description**: Delete a specific player by ID.
     - **Response**: Confirmation message or status.

3. **Special Routes**
   - **GET /teams/<id>/players**
     - **Description**: Retrieve all players for a specific team.
     - **Response**: Returns an array of player objects associated with the specified team.

   - **GET /players/country/<country>**
     - **Description**: Retrieve players from a specific country.
     - **Response**: Returns an array of player objects from the specified country.