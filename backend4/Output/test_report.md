### POST /users
Payload: {"username": "testuser", "password": "password", "email": "test@example.com", "name": "Test User"}
Result: ✅ 201 Created
Response: {"email":"test@example.com","id":3,"name":"Test User","username":"testuser"}

### POST /movies
Payload: {"title": "Test Movie", "description": "A test movie.", "length": 120, "rating": 5, "director_id": 1}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### POST /series
Payload: {"title": "Test Series", "description": "A test series.", "rating": 5, "director_id": 1, "seasons_count": 2, "episodes_per_season": 10}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### POST /directors
Payload: {"name": "Test Director"}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### POST /actors
Payload: {"name": "Test Actor"}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### POST /movies/1/actors
Payload: {"actor_id": 1}
Result: ✅ 201 Created
Response: {"message":"Actor associated with movie successfully"}

### POST /series/1/actors
Payload: {"actor_id": 1}
Result: ✅ 201 Created
Response: {"message":"Actor associated with series successfully"}

### GET /users
Payload: {}
Result: ✅ 200 OK
Response: [{"email":"testuser@example.com","id":1,"name":"Test User","username":"testuser"},{"email":"testuser@example.com","id":2,"name":"Test User","username":"testuser"},{"email":"test@example.com","id":3,"name":"Test User","username":"testuser"}]

### GET /users/1
Payload: {}
Result: ✅ 200 OK
Response: {"email":"testuser@example.com","id":1,"name":"Test User","username":"testuser"}

### GET /movies
Payload: {}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### GET /movies/1
Payload: {}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### GET /series
Payload: {}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### GET /series/1
Payload: {}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### GET /directors
Payload: {}
Result: ✅ 200 OK
Response: []

### GET /directors/1
Payload: {}
Result: ❌ 404 Not Found
Response: {"message":"Director not found"}

### GET /actors
Payload: {}
Result: ✅ 200 OK
Response: []

### GET /actors/1
Payload: {}
Result: ❌ 404 Not Found
Response: {"message":"Actor not found"}

### PUT /users/1
Payload: {"username": "updateduser", "password": "newpassword", "email": "updated@example.com", "name": "Updated User"}
Result: ✅ 200 OK
Response: {"email":"updated@example.com","id":1,"name":"Updated User","username":"updateduser"}

### PUT /movies/1
Payload: {"title": "Updated Test Movie", "description": "An updated test movie.", "length": 130, "rating": 4, "director_id": 1}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### PUT /series/1
Payload: {"title": "Updated Test Series", "description": "An updated test series.", "rating": 4, "director_id": 1, "seasons_count": 3, "episodes_per_season": 12}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### PUT /directors/1
Payload: {"name": "Updated Director"}
Result: ❌ 404 Not Found
Response: {"message":"Director not found"}

### PUT /actors/1
Payload: {"name": "Updated Actor"}
Result: ❌ 404 Not Found
Response: {"message":"Actor not found"}

### DELETE /users/1
Payload: {}
Result: ✅ 200 OK
Response: {"message":"User deleted successfully"}

### DELETE /movies/1
Payload: {}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### DELETE /series/1
Payload: {}
Result: ❌ 500 Internal Server Error
Response: <!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>

### DELETE /directors/1
Payload: {}
Result: ❌ 404 Not Found
Response: {"message":"Director not found"}

### DELETE /actors/1
Payload: {}
Result: ❌ 404 Not Found
Response: {"message":"Actor not found"}