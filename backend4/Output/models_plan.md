Database Schema:

1. **User**
   - id: integer (auto-increment)
   - username: string
   - password: string (hashed)
   - email: string
   - name: string

2. **Movie**
   - id: integer (auto-increment)
   - title: string
   - description: string
   - length: integer (in minutes)
   - rating: integer (1 to 10)
   - director_id: integer (ForeignKey referencing Director.id)
   - sequel_id: integer (ForeignKey referencing Movie.id, nullable)
   - prequel_id: integer (ForeignKey referencing Movie.id, nullable)

3. **Series**
   - id: integer (auto-increment)
   - title: string
   - description: string
   - rating: integer (1 to 10)
   - director_id: integer (ForeignKey referencing Director.id)
   - seasons_count: integer
   - episodes_per_season: integer (this could be further normalized by creating a Seasons table)

4. **Director**
   - id: integer (auto-increment)
   - name: string

5. **Actor**
   - id: integer (auto-increment)
   - name: string

6. **MovieActor (to establish a many-to-many relationship between Movies and Actors)**
   - id: integer (auto-increment)
   - movie_id: integer (ForeignKey referencing Movie.id)
   - actor_id: integer (ForeignKey referencing Actor.id)

7. **SeriesActor (to establish a many-to-many relationship between Series and Actors)**
   - id: integer (auto-increment)
   - series_id: integer (ForeignKey referencing Series.id)
   - actor_id: integer (ForeignKey referencing Actor.id)

This schema allows for the safe storing of watched movies and series, their ratings, and provides the necessary relationships to access sequels and prequels, as well as allowing retrieval of all works by a given director or involving specific actors.