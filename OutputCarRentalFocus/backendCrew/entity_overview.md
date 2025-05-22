```markdown
# entity_overview.md

## Entities Catalogue for Car Rental Service

---

### 1. Car  
- **Description:** Represents a vehicle available for rent in the system.  
- **Attributes:**  
  - `id`: Unique identifier for each car.  
  - `brand`: Manufacturer or brand of the car (e.g., Toyota, Ford).  
  - `model`: Specific model name of the car (e.g., Camry, Focus).  
  - `category`: Classification of the car to segment offerings (e.g., SUV, sedan, compact).  
  - `status`: Current rental state of the car (e.g., "available", "rented").  
  - `plate_no`: Unique license plate number of the car.  
  - `location_id`: Reference to the Location entity indicating where the car is stationed.  
  - `price_per_day`: Daily rental price charged for the car.  
- **Relations:**  
  - **Location 1-n Car:** Each Car belongs to exactly one Location.  
  - **Car 1-n Rental:** A Car may be associated with many Rental records over time.

---

### 2. Customer  
- **Description:** An individual or entity who rents cars from the service.  
- **Attributes:**  
  - `id`: Unique customer identifier.  
  - `name`: Full name of the customer.  
  - `email`: Contact email address.  
  - `phone`: Contact phone number.  
- **Relations:**  
  - **Customer 1-n Rental:** Each Customer can have multiple Rentals.

---

### 3. Rental  
- **Description:** Represents a rental transaction where a Customer books a Car for a specific period. Tracks booking details, lifecycle, and status.  
- **Attributes:**  
  - `id`: Unique rental identifier.  
  - `customer_id`: Reference to the Customer who booked the rental.  
  - `car_id`: Reference to the Car being rented.  
  - `start_date`: Rental period start date.  
  - `end_date`: Rental period end date.  
  - `total_price`: Calculated total rental cost (`price_per_day` × rental duration in days).  
  - `status`: Current rental status (e.g., "active", "completed", "cancelled").  
- **Relations:**  
  - **Customer 1-n Rental:** Each Rental is associated with exactly one Customer.  
  - **Car 1-n Rental:** Each Rental is associated with exactly one Car.

---

### 4. Location  
- **Description:** Physical or operational place where cars are stored or rented from.  
- **Attributes:**  
  - `id`: Unique location identifier.  
  - `name`: Name of the location (e.g., "Downtown Branch").  
  - `address`: Full address or description.  
- **Relations:**  
  - **Location 1-n Car:** One Location hosts many Cars.

---

## Summary of Relationships

- **Location 1-n Car:** One Location can have many Cars; each Car belongs to exactly one Location.  
- **Car 1-n Rental:** One Car may be rented multiple times over its lifecycle; each Rental refers to a single Car.  
- **Customer 1-n Rental:** One Customer can have many Rentals; each Rental belongs to a single Customer.

---

## Business Logic Notes

- Rental periods for the same Car must never overlap to ensure availability.  
- Creating a Rental:  
  - Validate Car availability for requested dates before confirming booking.  
  - Automatically calculate `total_price` as `price_per_day` × rental days.  
  - Set Rental status initially to "active".  
  - Update Car’s status to "rented".  
- Cancelling a Rental:  
  - Allowed only if the Rental period has not yet started.  
  - Triggers refund process (mocked implementation).  
- Returning a Rental:  
  - Marks Rental status as "completed".  
  - Updates Car status back to "available".  
- Location entity serves as a static organizational unit for Cars.

---
```