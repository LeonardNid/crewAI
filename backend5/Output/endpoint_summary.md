1. **POST /frames** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Frame attributes)
   Returns the newly created frame data.
   
2. **POST /rims** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Rim attributes)
   Returns the newly created rim data.
   
3. **POST /brakes** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Brakes attributes)
   Returns the newly created brake data.
   
4. **POST /gears** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Gears attributes)
   Returns the newly created gear data.
   
5. **POST /handlebars** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Handlebars attributes)
   Returns the newly created handlebar data.
   
6. **POST /saddles** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Saddle attributes)
   Returns the newly created saddle data.
   
7. **POST /seatposts** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Seatpost attributes)
   Returns the newly created seatpost data.
   
8. **POST /brakepads** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to BrakePad attributes)
   Returns the newly created brakepad data.

9. **GET /frames** 
   Returns a list of all frames.

10. **GET /rims** 
    Returns a list of all rims.

11. **GET /brakes** 
    Returns a list of all brakes.

12. **GET /gears** 
    Returns a list of all gears.

13. **GET /handlebars** 
    Returns a list of all handlebars.

14. **GET /saddles** 
    Returns a list of all saddles.

15. **GET /seatposts** 
    Returns a list of all seatposts.

16. **GET /brakepads** 
    Returns a list of all brakepads.

17. **PUT /frames/<id>** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Frame attributes)
    Returns the updated frame data.

18. **PUT /rims/<id>** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Rim attributes)
    Returns the updated rim data.

19. **PUT /brakes/<id>** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Brakes attributes)
    Returns the updated brake data.

20. **PUT /gears/<id>** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Gears attributes)
    Returns the updated gear data.

21. **PUT /handlebars/<id>** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Handlebars attributes)
    Returns the updated handlebar data.

22. **PUT /saddles/<id>** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Saddle attributes)
    Returns the updated saddle data.

23. **PUT /seatposts/<id>** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to Seatpost attributes)
    Returns the updated seatpost data.

24. **PUT /brakepads/<id>** -> Needs `{ "field1": value, "field2": value, ...}` (Expected JSON fields correspond to BrakePad attributes)
    Returns the updated brakepad data.

25. **DELETE /frames/<id>** 
    Returns a message indicating frame deletion success.

26. **DELETE /rims/<id>** 
    Returns a message indicating rim deletion success.

27. **DELETE /brakes/<id>** 
    Returns a message indicating brake deletion success.

28. **DELETE /gears/<id>** 
    Returns a message indicating gear deletion success.

29. **DELETE /handlebars/<id>** 
    Returns a message indicating handlebar deletion success.

30. **DELETE /saddles/<id>** 
    Returns a message indicating saddle deletion success.

31. **DELETE /seatposts/<id>** 
    Returns a message indicating seatpost deletion success.

32. **DELETE /brakepads/<id>** 
    Returns a message indicating brakepad deletion success.