1. POST /cars -> Needs { brand: string, model: string, category: string, status: string, plate_no: string, location_id: integer, price_per_day: number }  
   Returns: newly created car data with unique plate_no and references to location.

2. GET /cars  
   Returns: list of all cars.

3. PUT /cars/<int:id> -> Needs { brand: string, model: string, category: string, status: string, plate_no: string, location_id: integer, price_per_day: number } (all optional for update)  
   Returns: updated car data or 404 if car not found.

4. GET /cars/<int:id>  
   Returns: specific car data by ID or 404 if not found.

5. DELETE /cars/<int:id>  
   Deletes a car by ID; deletes all associated rentals due to cascade delete. Returns confirmation message or 404 if not found.

6. GET /cars_available  
   Query parameters: category (string), location (integer), start_date (string, YYYY-MM-DD), end_date (string, YYYY-MM-DD)  
   Returns: list of available cars filtered by criteria and excluding those with overlapping active rentals.

7. POST /customers -> Needs { name: string, email: string, phone: string (optional) }  
   Returns: newly created customer data with unique email.

8. GET /customers  
   Returns: list of all customers.

9. PUT /customers/<int:id> -> Needs { name: string, email: string, phone: string } (all optional for update)  
   Returns: updated customer data or 404 if not found.

10. GET /customers/<int:id>  
    Returns: specific customer by ID or 404 if not found.

11. DELETE /customers/<int:id>  
    Deletes a customer by ID; all associated rentals will be deleted due to cascade delete. Returns confirmation message or 404 if not found.

12. POST /rentals -> Needs { customer_id: integer, car_id: integer, start_date: string (YYYY-MM-DD), end_date: string (YYYY-MM-DD), status: string (optional: rented/reserved/booked), total_price: number (ignored, calculated) }  
    Validates car availability, start/end dates, and calculates total_price as price_per_day * rental days. Updates car status to 'rented'. Returns newly created rental data or error messages.

13. GET /rentals  
    Returns: list of all rentals.

14. PUT /rentals/<int:id> -> Needs { customer_id: integer (optional), car_id: integer (optional), start_date: string (YYYY-MM-DD), end_date: string (YYYY-MM-DD), status: string, total_price: number (ignored, recalculated) } (all optional for update)  
    Validates date formats, availability excluding current rental, recalculates total_price, updates car rental status accordingly. Returns updated rental or errors.

15. GET /rentals/<int:id>  
    Returns: specific rental by ID or 404 if not found.

16. DELETE /rentals/<int:id>  
    Permitted only if rental period has not started. Triggers refund placeholder and makes car available. Returns confirmation or error.

17. POST /rentals/<int:id>/return  
    Marks rental as returned and completed; updates rental status to 'completed' and car status to 'available'. Returns updated rental or 404 if not found.

18. POST /locations -> Needs { name: string, address: string }  
    Returns: newly created location data.

19. GET /locations  
    Returns: list of all locations.

20. PUT /locations/<int:id> -> Needs { name: string, address: string } (all optional for update)  
    Returns: updated location data or 404 if not found.

21. GET /locations/<int:id>  
    Returns: specific location by ID or 404 if not found.

22. DELETE /locations/<int:id>  
    Deletes location by ID; cascade deletes all cars at this location, which in turn cascade delete their rentals (due to model relations). Must be after deleting rentals and cars for dependency rules. Returns confirmation or 404 if not found.

23. GET /analytics_revenue_monthly  
    Returns: aggregated monthly revenue summaries with year, month, and total revenue.

24. GET /analytics_utilization_car_category  
    Returns: utilization rate per car category, defined as total rental days divided by number of cars * 30 days (monthly approximation), rounded to 4 decimals.

---

Note on DELETE ordering for dependency tree compliance:  
- Rentals (children of Cars and Customers) must be deleted before Cars and Customers.  
- Cars (children of Locations) must be deleted before Locations.  
Following this, the DELETE order is: Rentals → Cars → Customers → Locations.  
The only DELETE endpoints available are Rentals, Cars, Customers, Locations.  
They appear strictly in this order respecting dependencies.  

This completes the strict, dependency- and HTTP method-ordered API testing plan.