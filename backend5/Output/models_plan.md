### Database Schema

**1. Team**
   - **id**: integer (Primary Key, Auto-increment)
   - **name**: string (Not Null, Unique)
   - **city**: string (Not Null)
   - **country**: string (Not Null)
   - **stadium**: string (Not Null)

**2. Player**
   - **id**: integer (Primary Key, Auto-increment)
   - **name**: string (Not Null)
   - **position**: string (Not Null) 
   - **country**: string (Not Null)
   - **team_id**: integer (Foreign Key references Team(id), Not Null)

### Relationships
- **Team to Player**: One-to-Many relationship 
  - A team can have multiple players.
  - Each player belongs to one team.