1. POST /users -> Needs { username: string, password: string, email: string, name: string }
   Returns the newly created user data.

2. POST /movies -> Needs { title: string, description: string, length: integer, rating: integer, director_id: integer, sequel_id: integer (optional), prequel_id: integer (optional) }
   Returns the newly created movie data.

3. POST /series -> Needs { title: string, description: string, rating: integer, director_id: integer, seasons_count: integer, episodes_per_season: integer }
   Returns the newly created series data.

4. POST /directors -> Needs { name: string }
   Returns the newly created director data.

5. POST /actors -> Needs { name: string }
   Returns the newly created actor data.

6. POST /movies/<int:movie_id>/actors -> Needs { actor_id: integer }
   Returns a success message for associating actor with movie.

7. POST /series/<int:series_id>/actors -> Needs { actor_id: integer }
   Returns a success message for associating actor with series.

8. GET /users -> Returns a list of all users.

9. GET /users/<int:id> -> Returns the user data for the specified ID.

10. GET /movies -> Returns a list of all movies.

11. GET /movies/<int:id> -> Returns the movie data for the specified ID.

12. GET /series -> Returns a list of all series.

13. GET /series/<int:id> -> Returns the series data for the specified ID.

14. GET /directors -> Returns a list of all directors.

15. GET /directors/<int:id> -> Returns the director data for the specified ID.

16. GET /actors -> Returns a list of all actors.

17. GET /actors/<int:id> -> Returns the actor data for the specified ID.

18. PUT /users/<int:id> -> Needs { username: string, password: string, email: string, name: string }
   Returns the updated user data.

19. PUT /movies/<int:id> -> Needs { title: string, description: string, length: integer, rating: integer, director_id: integer, sequel_id: integer (optional), prequel_id: integer (optional) }
   Returns the updated movie data.

20. PUT /series/<int:id> -> Needs { title: string, description: string, rating: integer, director_id: integer, seasons_count: integer, episodes_per_season: integer }
   Returns the updated series data.

21. PUT /directors/<int:id> -> Needs { name: string }
   Returns the updated director data.

22. PUT /actors/<int:id> -> Needs { name: string }
   Returns the updated actor data.

23. DELETE /users/<int:id> -> Returns a success message for user deletion.

24. DELETE /movies/<int:id> -> Returns a success message for movie deletion.

25. DELETE /series/<int:id> -> Returns a success message for series deletion.

26. DELETE /directors/<int:id> -> Returns a success message for director deletion.

27. DELETE /actors/<int:id> -> Returns a success message for actor deletion.