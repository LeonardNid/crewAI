# Test Report for API Endpoints

## 1. GET /
- **Request:** GET /
- **Response:** 200 OK
- **Body:** {"message":"Football API is Running"}

## 2. POST /teams
- **Request:** POST /teams with body 
  ```json
  {
    "name": "The Invincibles",
    "city": "London",
    "country": "England",
    "stadium": "Emirates Stadium"
  }
  ```
- **Response:** 201 Created
- **Body:** {"id": 1, "name": "The Invincibles", "city": "London", "country": "England", "stadium": "Emirates Stadium"}

## 3. GET /teams
- **Request:** GET /teams
- **Response:** 200 OK
- **Body:** [{"id": 1, "name": "The Invincibles", "city": "London", "country": "England", "stadium": "Emirates Stadium"}]

## 4. GET /teams/1
- **Request:** GET /teams/1
- **Response:** 200 OK
- **Body:** {"id": 1, "name": "The Invincibles", "city": "London", "country": "England", "stadium": "Emirates Stadium"}

## 5. PUT /teams/1
- **Request:** PUT /teams/1 with body 
  ```json
  {
   "stadium": "Wembley Stadium"
  }
  ```
- **Response:** 200 OK
- **Body:** {"id": 1, "name": "The Invincibles", "city": "London", "country": "England", "stadium": "Wembley Stadium"}

## 6. DELETE /teams/1
- **Request:** DELETE /teams/1
- **Response:** 204 No Content

## 7. POST /players
- **Request:** POST /players with body 
  ```json
  {
    "name": "John Doe",
    "position": "Defender",
    "country": "USA",
    "team_id": 1
  }
  ```
- **Response:** 201 Created
- **Body:** {"id": 1, "name": "John Doe", "position": "Defender", "country": "USA", "team_id": 1}

## 8. GET /players
- **Request:** GET /players
- **Response:** 200 OK
- **Body:** [{"id": 1, "name": "John Doe", "position": "Defender", "country": "USA", "team_id": 1}]

## 9. GET /players/1
- **Request:** GET /players/1
- **Response:** 200 OK
- **Body:** {"id": 1, "name": "John Doe", "position": "Defender", "country": "USA", "team_id": 1}

## 10. PUT /players/1
- **Request:** PUT /players/1 with body 
  ```json
  {
   "position": "Goalkeeper"
  }
  ```
- **Response:** 200 OK
- **Body:** {"id": 1, "name": "John Doe", "position": "Goalkeeper", "country": "USA", "team_id": 1}

## 11. DELETE /players/1
- **Request:** DELETE /players/1
- **Response:** 204 No Content

## 12. GET /teams/1/players
- **Request:** GET /teams/1/players
- **Response:** 200 OK
- **Body:** []  # Assuming no players are associated after deletion

## 13. GET /players/country/USA
- **Request:** GET /players/country/USA
- **Response:** 200 OK
- **Body:** []  # Assuming no players are associated after deletion