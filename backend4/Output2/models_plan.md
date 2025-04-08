```
Database Schema:

1. Team
   - id: integer (auto-increment, primary key)
   - name: string (team name)
   - city: string (city where the team is based)
   - country: string (country where the team is located)
   - stadium: string (name of the stadium)

2. Player
   - id: integer (auto-increment, primary key)
   - name: string (player name)
   - position: string (player position, e.g., forward, midfielder)
   - team_id: integer (foreign key referencing Team.id)
   - country: string (country of the player)

Relationships:
- A Team has many Players (one-to-many relationship).
- Each Player belongs to one Team (many-to-one relationship).
```