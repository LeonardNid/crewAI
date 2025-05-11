{
  "requests": [
    {
      "route": "/books",
      "method": "POST",
      "json_data": {
        "title": "Dummy Book Title",
        "author": "Jane Doe",
        "isbn": "123-4567890123",
        "genre": "Fiction",
        "publication_year": 2020,
        "borrowed_flag": false
      }
    },
    {
      "route": "/members",
      "method": "POST",
      "json_data": {
        "name": "John Smith",
        "email_address": "john.smith@example.com",
        "membership_number": "M12345678",
        "membership_expiry_date": "2025-12-31"
      }
    },
    {
      "route": "/loans",
      "method": "POST",
      "json_data": {
        "book_id": 1,
        "member_id": 1,
        "checkout_date": "2024-01-01",
        "due_date": "2024-02-01",
        "returned_flag": false
      }
    },
    {
      "route": "/books",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/books/1",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/books/title/Dummy Book Title",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/books/author/Jane Doe",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/members",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/members/1",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/loans",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/loans/1",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/loans/overdue",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/books/1",
      "method": "PUT",
      "json_data": {
        "title": "Updated Book Title",
        "author": "Jane Doe",
        "isbn": "123-4567890123",
        "genre": "Non-fiction",
        "publication_year": 2022,
        "borrowed_flag": true
      }
    },
    {
      "route": "/members/1",
      "method": "PUT",
      "json_data": {
        "name": "John Smith Updated",
        "email_address": "john.smith.updated@example.com",
        "membership_number": "M87654321",
        "membership_expiry_date": "2026-01-01"
      }
    },
    {
      "route": "/loans/1",
      "method": "PUT",
      "json_data": {
        "book_id": 1,
        "member_id": 1,
        "checkout_date": "2024-01-10",
        "due_date": "2024-02-10",
        "returned_flag": true
      }
    },
    {
      "route": "/loans/1",
      "method": "DELETE",
      "json_data": null
    },
    {
      "route": "/books/1",
      "method": "DELETE",
      "json_data": null
    },
    {
      "route": "/members/1",
      "method": "DELETE",
      "json_data": null
    }
  ]
}