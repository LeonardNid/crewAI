```markdown
# entity_overview.md

## Entities and Relationships Catalogue for Multi-Branch Car Rental System

### 1. Car
- **Description:** Represents a vehicle available for rental across branches.
- **Attributes:**
  - plate_no (primary key, unique identifier)
  - brand
  - model
  - year
  - category (e.g., compact, SUV, van)
  - seats (number of seats)
  - transmission (automatic/manual)
  - fuel_type
  - daily_rate (rental cost per day)
  - current_odometer (latest recorded mileage)
  - status (current state: available, rented, service)
  - location_id (foreign key - current location of the car)
- **Relationships:**
  - Assigned to one Location (1 Car → 1 Location)
  - May have many Rentals (1 Car → many Rentals)
  - May have many Services (1 Car → many Services)

---

### 2. Location
- **Description:** Branch or rental office location where cars can be picked up or dropped off.
- **Attributes:**
  - location_id (primary key)
  - name (branch name)
  - address
  - city
  - country
  - phone
- **Relationships:**
  - Has many Cars (1 Location → many Cars)
  - Is pickup location for many Rentals (1 Location → many Rentals as pickup_location)
  - Is dropoff location for many Rentals (1 Location → many Rentals as dropoff_location)

---

### 3. Customer
- **Description:** Person who rents vehicles from the company.
- **Attributes:**
  - customer_id (primary key)
  - name
  - email
  - phone
  - driver_license_no
  - license_expiry (date the license expires)
  - vip (boolean flag indicating VIP status)
- **Relationships:**
  - Can have many Rentals (1 Customer → many Rentals)

---

### 4. Rental
- **Description:** Represents the booking and usage of a car by a customer over a specific time period.
- **Attributes:**
  - rental_id (primary key)
  - car_plate_no (foreign key referencing Car)
  - customer_id (foreign key referencing Customer)
  - pickup_location_id (foreign key referencing Location)
  - dropoff_location_id (foreign key referencing Location)
  - pickup_date
  - dropoff_date
  - daily_rate_snapshot (rate locked at booking time)
  - total_price (calculated rental cost)
  - status (active, closed, cancelled)
- **Relationships:**
  - References one Car (1 Rental → 1 Car)
  - References one Customer (1 Rental → 1 Customer)
  - References one pickup Location (1 Rental → 1 Location)
  - References one dropoff Location (1 Rental → 1 Location)
  - May have many Payments (1 Rental → many Payments)

---

### 5. Payment
- **Description:** Represents payment made for a rental, including potential refunds.
- **Attributes:**
  - payment_id (primary key)
  - rental_id (foreign key referencing Rental)
  - amount
  - method (e.g., card, cash)
  - paid_at (timestamp)
  - refunded (boolean flag indicating if a refund was issued)
- **Relationships:**
  - Linked to one Rental (1 Payment → 1 Rental)

---

### 6. Service
- **Description:** Records maintenance or repair service periods for cars.
- **Attributes:**
  - service_id (primary key)
  - car_plate_no (foreign key referencing Car)
  - service_type (e.g., oil change, tires, repair)
  - start_date
  - end_date
  - cost
  - notes (additional details)
- **Relationships:**
  - Assigned to one Car (1 Service → 1 Car)

---

## Summary of Key Relationships:
- **Car** belongs to one **Location** but **Location** has many **Cars**.
- **Rental** associates one **Car**, one **Customer**, one pickup **Location**, and one dropoff **Location**.
- **Customer** can have many **Rentals**.
- **Rental** can have many **Payments**.
- **Car** can have many **Services**.

---

## Core Business Logic Integration Notes
- When booking a rental, the system must:
  - Filter available cars by category, location, and date range.
  - Lock selected car by setting status to "rented".
  - Create Rental with daily_rate snapshot and computed total_price.

- When returning a car:
  - Mark Rental status as "closed".
  - Update Car status to "available".
  - Update Car current_odometer and current location.

- When cancelling a rental (only if pickup_date is in the future):
  - Validate cancellation eligibility.
  - Set Rental status to "cancelled".
  - Trigger Payment refund (update Payment refunded flag).

- Service management:
  - When creating Service, set Car status to "service".
  - Car is not available for booking during active service dates.
  - Service record includes service_type, duration, cost, and notes.

- Analytics and Search:
  - Revenue and utilization analytics will aggregate across Rentals and Payments.
  - Search endpoints for Customers (by name) and Cars (by plate number or model).

This entity overview fully encapsulates all domain objects and relationships necessary to support the required features: CRUD operations, booking workflow, return & cancellation with refund, service management, filtering and search for cars, and analytics.
```