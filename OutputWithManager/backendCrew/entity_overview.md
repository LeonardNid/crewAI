# Entity Overview for Library Management Application

## Entities

### Book
- **Description:** Represents a book in the library's collection.
- **Attributes:**
  - Title: The name of the book.
  - Author: The author(s) of the book.
  - ISBN: International Standard Book Number, unique identifier.
  - Genre: Category or type of the book (e.g., fiction, non-fiction).
  - Publication Year: The year the book was published.
  - Is Borrowed: A boolean flag indicating if the book is currently borrowed.

### Member
- **Description:** Represents a registered user who can borrow books.
- **Attributes:**
  - Name: Full name of the member.
  - Email Address: Contact email of the member.
  - Membership Number: Unique identifier assigned to the member.
  - Membership Expiration Date: The date the membership is valid until.

### Loan
- **Description:** Represents the transaction of borrowing a book by a member.
- **Attributes:**
  - Book: Reference to the borrowed Book entity.
  - Member: Reference to the Member who borrowed the book.
  - Checkout Date: The date when the book was borrowed.
  - Due Date: The date by which the book should be returned.

## Relationships

- **Book 1 - N Loan:**  
  Each Book can be associated with zero or many Loan records over time (reflecting multiple loans of the same book). At any one time, a Book may have zero or one active loan.
  
- **Member 1 - N Loan:**  
  Each Member can have zero or many Loan records, representing the books they have borrowed over time.

- **Loan N - 1 Book:**  
  Each Loan instance corresponds to exactly one Book being borrowed.

- **Loan N - 1 Member:**  
  Each Loan corresponds to exactly one Member who borrowed the book.

---

This entity overview comprehensively captures all primary data structures needed for the application to support CRUD operations on books and members, book borrowing and returning, overdue loan management, and book searching functionality.