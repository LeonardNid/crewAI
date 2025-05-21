# Library Management Backend REST API Endpoint Checklist

1. **Add a new book** – Endpoint to create a book with title, author, ISBN, genre, publication year, and default `is_borrowed = false`.  
2. **Edit an existing book** – Endpoint to update any book details except the `is_borrowed` flag (which is managed internally).  
3. **Delete a book** – Endpoint to delete a book by its identifier.  
4. **Add a new member** – Endpoint to create a member with name, email, membership number, and membership expiry date.  
5. **Edit an existing member** – Endpoint to update any member details.  
6. **Delete a member** – Endpoint to delete a member by its identifier.  
7. **Borrow a book** – Endpoint allowing a member to borrow a book, which must:  
   - Set the book’s `is_borrowed` flag to true.  
   - Create a loan record with the book, member, checkout date, and due date.  
   - Ensure the loan’s `return_date` is unset/null upon borrowing.  
   - Validate the book is not already borrowed.  
8. **Return a book** – Endpoint to mark a borrowed book as returned, which must:  
   - Set the book's `is_borrowed` flag to false.  
   - Update the loan record’s `return_date` with the actual return date.  
   - Ensure the loan exists and is currently active (not already returned).  
9. **List all overdue loans** – Endpoint to retrieve loans where the current date is past the due date and `return_date` is null (book not yet returned).  
10. **Search books by title** – Endpoint to search and list books filtered by partial or full title matches.  
11. **Search books by author** – Endpoint to search and list books filtered by partial or full author name matches.  

This checklist provides a clear, complete, and endpoint-precise set of REST API features for managing a small public library backend per the customer’s specifications and defect corrections.