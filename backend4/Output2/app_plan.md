### Routes Plan

**1. Teams Endpoints**
- **POST /teams**  
  - **Request Body:**  
    - `name`: string (required)  
    - `city`: string (required)  
    - `country`: string (required)  
    - `stadium`: string (required)  
  - **Response:**  
    - Status 201: Team Created with team ID, team details  
    - Status 400: Bad Request if any field is missing/invalid  

- **GET /teams**  
  - **Response:**  
    - Status 200: Array of all teams, each with ID, name, city, country, and stadium  

- **GET /teams/{id}**  
  - **Path Parameter:**  
    - `id`: integer (required)  
  - **Response:**  
    - Status 200: Team details for the specified ID  
    - Status 404: Not Found if team does not exist  

- **PUT /teams/{id}**  
  - **Path Parameter:**  
    - `id`: integer (required)  
  - **Request Body:**  
    - `name`: string (optional)  
    - `city`: string (optional)  
    - `country`: string (optional)  
    - `stadium`: string (optional)  
  - **Response:**  
    - Status 200: Updated team details  
    - Status 404: Not Found if team does not exist  
    - Status 400: Bad Request if all fields are empty  

- **DELETE /teams/{id}**  
  - **Path Parameter:**  
    - `id`: integer (required)  
  - **Response:**  
    - Status 204: No Content, team deleted successfully  
    - Status 404: Not Found if team does not exist  

**2. Players Endpoints**
- **POST /players**  
  - **Request Body:**  
    - `name`: string (required)  
    - `position`: string (required)  
    - `country`: string (required)  
    - `team_id`: integer (required, must reference an existing team)  
  - **Response:**  
    - Status 201: Player Created with player ID, player details  
    - Status 400: Bad Request if any field is missing/invalid  

- **GET /players**  
  - **Response:**  
    - Status 200: Array of all players, each with ID, name, position, country, and team_id  

- **GET /players/{id}**  
  - **Path Parameter:**  
    - `id`: integer (required)  
  - **Response:**  
    - Status 200: Player details for the specified ID  
    - Status 404: Not Found if player does not exist  

- **PUT /players/{id}**  
  - **Path Parameter:**  
    - `id`: integer (required)  
  - **Request Body:**  
    - `name`: string (optional)  
    - `position`: string (optional)  
    - `country`: string (optional)  
    - `team_id`: integer (optional, must reference an existing team)  
  - **Response:**  
    - Status 200: Updated player details  
    - Status 404: Not Found if player does not exist  
    - Status 400: Bad Request if all fields are empty  

- **DELETE /players/{id}**  
  - **Path Parameter:**  
    - `id`: integer (required)  
  - **Response:**  
    - Status 204: No Content, player deleted successfully  
    - Status 404: Not Found if player does not exist  

**3. Special Routes**
- **GET /teams/{team_id}/players**  
  - **Path Parameter:**  
    - `team_id`: integer (required)  
  - **Response:**  
    - Status 200: Array of players associated with the specified team ID  
    - Status 404: Not Found if team does not exist  

- **GET /players/country/{country}**  
  - **Path Parameter:**  
    - `country`: string (required)  
  - **Response:**  
    - Status 200: Array of players from the specified country  
    - Status 404: Not Found if no players exist from that country  

This structured plan outlines the necessary routes, expected data, and response formats to be implemented for the football team and player management system.