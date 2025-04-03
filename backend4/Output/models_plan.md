### Database Schema

**1. Team**
   - **Fields:**
     - `id: string` (Primary Key, Unique Identifier for the team)
     - `name: string` (Name of the team)
     - `city: string` (City where the team is based)
     - `country: string` (Country where the team is located)
     - `stadium: string` (Name of the team's home stadium)
   - **Relationships:**
     - One-to-Many with Player (A team can have multiple players)

**2. Player**
   - **Fields:**
     - `id: string` (Primary Key, Unique Identifier for the player)
     - `name: string` (Full name of the player)
     - `position: string` (Position played by the player, e.g., Forward, Midfielder, Defender, Goalkeeper)
     - `team_id: string` (Foreign Key, references Team)
     - `country: string` (Country of the player)
   - **Relationships:**
     - Many-to-One with Team (A player belongs to one team)