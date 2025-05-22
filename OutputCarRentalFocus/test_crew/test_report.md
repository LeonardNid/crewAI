{
  "requests": [
    {
      "route": "/cars",
      "method": "POST",
      "json_data": {
        "brand": "Honda",
        "model": "Civic",
        "category": "Sedan",
        "status": "available",
        "plate_no": "DEF456",
        "location_id": 2,
        "price_per_day": 55.99
      }
    },
    {
      "route": "/customers",
      "method": "POST",
      "json_data": {
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "phone": "321-654-0987"
      }
    },
    {
      "route": "/rentals",
      "method": "POST",
      "json_data": {
        "customer_id": 2,
        "car_id": 2,
        "start_date": "2024-08-01",
        "end_date": "2024-08-07",
        "status": "booked",
        "total_price": 0
      }
    },
    {
      "route": "/locations",
      "method": "POST",
      "json_data": {
        "name": "Uptown Branch",
        "address": "789 Pine St, Anytown"
      }
    }
  ]
}