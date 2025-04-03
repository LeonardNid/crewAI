### Database Schema

#### Model: Team
- **Fields:**
  - `id`: integer (Primary Key, Auto-increment)
  - `name`: string (Not Null)
  - `city`: string (Not Null)
  - `country`: string (Not Null)
  - `stadium`: string (Not Null)

#### Model: Player
- **Fields:**
  - `id`: integer (Primary Key, Auto-increment)
  - `name`: string (Not Null)
  - `position`: string (Not Null)
  - `country`: string (Not Null)
  - `team_id`: integer (Foreign Key referencing Team(id))

### Relationships
- One-to-Many relationship between Team and Player, where one Team can have multiple Players, but each Player belongs to exactly one Team.

### CRUD Endpoints
1. **Teams**
   - `POST /teams` - Create a new team
   - `GET /teams` - Retrieve all teams
   - `GET /teams/{id}` - Retrieve a single team by ID
   - `PUT /teams/{id}` - Update an existing team by ID
   - `DELETE /teams/{id}` - Delete a team by ID

2. **Players**
   - `POST /players` - Create a new player
   - `GET /players` - Retrieve all players
   - `GET /players/{id}` - Retrieve a single player by ID
   - `PUT /players/{id}` - Update an existing player by ID
   - `DELETE /players/{id}` - Delete a player by ID