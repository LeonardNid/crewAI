```markdown
# feature_checklist.md

1. Create a new car
2. Retrieve details of a car by plate number
3. Update details of a car by plate number
4. Delete a car by plate number
5. List all cars with optional filters: by location, category, seats, transmission, price range
6. Search cars by partial or full match on plate number or model

7. Create a new location
8. Retrieve details of a location by location ID
9. Update details of a location by location ID
10. Delete a location by location ID
11. List all locations

12. Create a new customer
13. Retrieve details of a customer by customer ID
14. Update details of a customer by customer ID
15. Delete a customer by customer ID
16. Search customers by partial or full name match

17. Book a new rental by selecting an available car filtered by category, pickup location, and date range; create rental record with daily_rate snapshot and total price; set car status to “rented”
18. Retrieve details of a rental by rental ID
19. Update rental details by rental ID (e.g., status)
20. Cancel a rental by rental ID only if rental start date is in the future; trigger payment refund
21. List rentals with optional filters: by status, customer ID, date range

22. Mark a rental as returned by rental ID; update rental status to “closed”; update car status to “available”; update car’s current_odometer and location based on return data

23. Create a new payment
24. Retrieve details of a payment by payment ID
25. Update a payment record by payment ID (e.g., mark refunded)
26. List payments with optional filters: by rental ID, date range

27. Create a new service record by car plate number; set car status to “service”
28. Retrieve details of a service record by service ID
29. Update a service record by service ID (e.g., end_date, notes)
30. Delete a service record by service ID
31. List service records with optional filters: by car plate number, service type, active status

32. List cars available for rental filtered by category, pickup location, and date range (to support booking workflow)
```