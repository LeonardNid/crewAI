### Routes Plan

1. **Team Endpoints**
   - **GET /teams**
     - **Description**: Fetch all teams.
     - **Response**: List of all teams with their details.

   - **GET /teams/<id>**
     - **Description**: Fetch a specific team by ID.
     - **Response**: Details of the team with the specified ID.

   - **POST /teams**
     - **Description**: Create a new team.
     - **Request Body**: JSON object containing `name`, `city`, `country`, and `stadium`.
     - **Response**: Details of the newly created team.

   - **PUT /teams/<id>**
     - **Description**: Update an existing team by ID.
     - **Request Body**: JSON object containing any of `name`, `city`, `country`, and `stadium` fields to update.
     - **Response**: Details of the updated team.

   - **DELETE /teams/<id>**
     - **Description**: Delete a specific team by ID.
     - **Response**: Confirmation of deletion.

2. **Player Endpoints**
   - **GET /players**
     - **Description**: Fetch all players.
     - **Response**: List of all players with their details.

   - **GET /players/<id>**
     - **Description**: Fetch a specific player by ID.
     - **Response**: Details of the player with the specified ID.

   - **POST /players**
     - **Description**: Create a new player.
     - **Request Body**: JSON object containing `name`, `position`, `country`, and `team_id`.
     - **Response**: Details of the newly created player.

   - **PUT /players/<id>**
     - **Description**: Update an existing player by ID.
     - **Request Body**: JSON object containing any of `name`, `position`, `country`, or `team_id` fields to update.
     - **Response**: Details of the updated player.

   - **DELETE /players/<id>**
     - **Description**: Delete a specific player by ID.
     - **Response**: Confirmation of deletion.

   - **GET /teams/<id>/players**
     - **Description**: Fetch all players in a specific team.
     - **Response**: List of all players associated with the team with the specified ID.

   - **GET /players/country/<country>**
     - **Description**: Fetch all players from a specific country.
     - **Response**: List of players belonging to the specified country.