```markdown
# entity_overview.md

## Entities and Relationships for Small Public Library Management

### 1. Book
- **Description**: Represents a book available in the library collection.
- **Attributes**:
  - Title (string)
  - Author (string)
  - ISBN (string, unique identifier)
  - Genre (string)
  - Publication Year (integer)
  - Borrowed Flag (boolean, indicates if the book is currently borrowed)
- **Relations**:
  - Can be referenced by zero or one active Loan
  - One book can have many past Loans (historical records)

### 2. Member
- **Description**: Represents a registered member of the library who can borrow books.
- **Attributes**:
  - Name (string)
  - E-mail Address (string)
  - Membership Number (string or integer, unique identifier)
  - Membership Expiry Date (date)
- **Relations**:
  - Can have many Loans (1-to-many relationship)

### 3. Loan
- **Description**: Tracks the borrowing of a book by a member.
- **Attributes**:
  - Checkout Date (date)
  - Due Date (date)
- **Relations**:
  - References one Book (1-to-1 per active loan)
  - References one Member (1-to-1)
  - One Loan relates one Book and one Member
  - Loan is created when a book is borrowed and closed when returned

```
This covers all domain objects and their relationships clearly based on the customer description and functional needs.