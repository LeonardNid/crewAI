### Database Schema

- **Team**
  - **id**: integer (Primary Key, Auto-increment) 
  - **name**: string (Name of the team)
  - **city**: string (City where the team is based)
  - **country**: string (Country of the team)
  - **stadium**: string (Name of the stadium used by the team)

- **Player**
  - **id**: integer (Primary Key, Auto-increment)
  - **name**: string (Full name of the player)
  - **position**: string (Position played by the player, e.g., goalkeeper, defender, midfielder, forward)
  - **team_id**: integer (Foreign Key referencing Team.id)
  - **country**: string (Country of the player)

### Relationships
- The `Player` model has a foreign key `team_id` that references the `id` of the `Team` model, establishing a one-to-many relationship where one team can have multiple players, but each player belongs to one team.