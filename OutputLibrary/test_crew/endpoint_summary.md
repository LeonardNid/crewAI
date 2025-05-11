1. POST /books -> Needs { title: string, author: string, isbn: string, genre: string, publication_year: integer, borrowed_flag: boolean }
   Returns: newly created book data with status 201.
2. POST /members -> Needs { name: string, email_address: string, membership_number: string, membership_expiry_date: string (ISO date) }
   Returns: newly created member data with status 201.
3. POST /loans -> Needs { book_id: integer, member_id: integer, checkout_date: string (ISO date), due_date: string (ISO date), returned_flag: boolean }
   Returns: newly created loan data with status 201.

4. GET /books
   Returns: list of all books as JSON array.
5. GET /books/<int:id>
   Returns: single book data by id or 404 if not found.
6. GET /books/title/<string:title>
   Returns: list of books matching title or 404 if none found.
7. GET /books/author/<string:author>
   Returns: list of books matching author or 404 if none found.
8. GET /members
   Returns: list of all members as JSON array.
9. GET /members/<int:id>
   Returns: single member data by id or 404 if not found.
10. GET /loans
    Returns: list of all loans as JSON array.
11. GET /loans/<int:id>
    Returns: single loan data by id or 404 if not found.
12. GET /loans/overdue
    Returns: list of loans where due date is past and returned_flag is false.

13. PUT /books/<int:id> -> Needs { title: string, author: string, isbn: string, genre: string, publication_year: integer, borrowed_flag: boolean }
    Returns: updated book data or 404 if not found.
14. PUT /members/<int:id> -> Needs { name: string, email_address: string, membership_number: string, membership_expiry_date: string (ISO date) }
    Returns: updated member data or 404 if not found.
15. PUT /loans/<int:id> -> Needs { book_id: integer, member_id: integer, checkout_date: string (ISO date), due_date: string (ISO date), returned_flag: boolean }
    Returns: updated loan data or 404 if not found.

16. DELETE /loans/<int:id>
    Returns: message "Loan deleted" or 404 if not found.
17. DELETE /books/<int:id>
    Returns: message "Book deleted" or 404 if not found.
18. DELETE /members/<int:id>
    Returns: message "Member deleted" or 404 if not found.

Explanation of DELETE order: Loan has foreign keys referencing Book and Member, so loans must be deleted before deleting books or members to respect database constraints and dependency integrity. The order is therefore DELETE loans first, then books and members in any order. Here members are deleted after books arbitrarily since they have no direct dependency between each other in deletion order.