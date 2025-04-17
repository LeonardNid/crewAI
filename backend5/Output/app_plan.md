### Routes Plan

1. **Frames**
   - **GET /frames**: Retrieve a list of all frames.
     - **Response**: JSON array of Frame objects.
   - **POST /frames**: Create a new frame.
     - **Request Body**: Frame object fields (name, brand, material, ...) 
     - **Response**: Created Frame object.
   - **GET /frames/{id}**: Retrieve a specific frame by ID.
     - **Response**: Frame object for the specified ID.
   - **PUT /frames/{id}**: Update a specific frame by ID.
     - **Request Body**: Frame object fields to update.
     - **Response**: Updated Frame object.
   - **DELETE /frames/{id}**: Delete a specific frame by ID.
     - **Response**: Success message or deleted Frame object.

2. **Rims**
   - **GET /rims**: Retrieve a list of all rims.
     - **Response**: JSON array of Rim objects.
   - **POST /rims**: Create a new rim.
     - **Request Body**: Rim object fields (tire_width, brand, ...)
     - **Response**: Created Rim object.
   - **GET /rims/{id}**: Retrieve a specific rim by ID.
     - **Response**: Rim object for the specified ID.
   - **PUT /rims/{id}**: Update a specific rim by ID.
     - **Request Body**: Rim object fields to update.
     - **Response**: Updated Rim object.
   - **DELETE /rims/{id}**: Delete a specific rim by ID.
     - **Response**: Success message or deleted Rim object.

3. **Brakes**
   - **GET /brakes**: Retrieve a list of all brakes.
     - **Response**: JSON array of Brake objects.
   - **POST /brakes**: Create a new brake.
     - **Request Body**: Brake object fields (type, brand, ...)
     - **Response**: Created Brake object.
   - **GET /brakes/{id}**: Retrieve a specific brake by ID.
     - **Response**: Brake object for the specified ID.
   - **PUT /brakes/{id}**: Update a specific brake by ID.
     - **Request Body**: Brake object fields to update.
     - **Response**: Updated Brake object.
   - **DELETE /brakes/{id}**: Delete a specific brake by ID.
     - **Response**: Success message or deleted Brake object.

4. **Gears**
   - **GET /gears**: Retrieve a list of all gears.
     - **Response**: JSON array of Gear objects.
   - **POST /gears**: Create a new gear.
     - **Request Body**: Gear object fields (type, brand, ...)
     - **Response**: Created Gear object.
   - **GET /gears/{id}**: Retrieve a specific gear by ID.
     - **Response**: Gear object for the specified ID.
   - **PUT /gears/{id}**: Update a specific gear by ID.
     - **Request Body**: Gear object fields to update.
     - **Response**: Updated Gear object.
   - **DELETE /gears/{id}**: Delete a specific gear by ID.
     - **Response**: Success message or deleted Gear object.

5. **Handlebars**
   - **GET /handlebars**: Retrieve a list of all handlebars.
     - **Response**: JSON array of Handlebar objects.
   - **POST /handlebars**: Create a new handlebar.
     - **Request Body**: Handlebar object fields (type, brand, ...)
     - **Response**: Created Handlebar object.
   - **GET /handlebars/{id}**: Retrieve a specific handlebar by ID.
     - **Response**: Handlebar object for the specified ID.
   - **PUT /handlebars/{id}**: Update a specific handlebar by ID.
     - **Request Body**: Handlebar object fields to update.
     - **Response**: Updated Handlebar object.
   - **DELETE /handlebars/{id}**: Delete a specific handlebar by ID.
     - **Response**: Success message or deleted Handlebar object.

6. **Saddles**
   - **GET /saddles**: Retrieve a list of all saddles.
     - **Response**: JSON array of Saddle objects.
   - **POST /saddles**: Create a new saddle.
     - **Request Body**: Saddle object fields (type, brand, ...)
     - **Response**: Created Saddle object.
   - **GET /saddles/{id}**: Retrieve a specific saddle by ID.
     - **Response**: Saddle object for the specified ID.
   - **PUT /saddles/{id}**: Update a specific saddle by ID.
     - **Request Body**: Saddle object fields to update.
     - **Response**: Updated Saddle object.
   - **DELETE /saddles/{id}**: Delete a specific saddle by ID.
     - **Response**: Success message or deleted Saddle object.

7. **Seatposts**
   - **GET /seatposts**: Retrieve a list of all seatposts.
     - **Response**: JSON array of Seatpost objects.
   - **POST /seatposts**: Create a new seatpost.
     - **Request Body**: Seatpost object fields (material, brand, ...)
     - **Response**: Created Seatpost object.
   - **GET /seatposts/{id}**: Retrieve a specific seatpost by ID.
     - **Response**: Seatpost object for the specified ID.
   - **PUT /seatposts/{id}**: Update a specific seatpost by ID.
     - **Request Body**: Seatpost object fields to update.
     - **Response**: Updated Seatpost object.
   - **DELETE /seatposts/{id}**: Delete a specific seatpost by ID.
     - **Response**: Success message or deleted Seatpost object.

8. **BrakePads**
   - **GET /brakepads**: Retrieve a list of all brake pads.
     - **Response**: JSON array of BrakePad objects.
   - **POST /brakepads**: Create a new brake pad.
     - **Request Body**: BrakePad object fields (brake_type, brand, ...)
     - **Response**: Created BrakePad object.
   - **GET /brakepads/{id}**: Retrieve a specific brake pad by ID.
     - **Response**: BrakePad object for the specified ID.
   - **PUT /brakepads/{id}**: Update a specific brake pad by ID.
     - **Request Body**: BrakePad object fields to update.
     - **Response**: Updated BrakePad object.
   - **DELETE /brakepads/{id}**: Delete a specific brake pad by ID.
     - **Response**: Success message or deleted BrakePad object.

### Additional Queries
- **GET /frames/{id}/compatibles**: Retrieve compatible components for a specific frame by ID.
  - **Response**: List of compatible Brakes, Gears, Handlebars, and Seatposts.

- **GET /components/compatible?frame_id={id}**: Retrieve all compatible components for a specified frame.
  - **Response**: Combined list of compatible components.