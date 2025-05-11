# Python Issue Report

| #  | File & location                          | Failing request                          | Root cause                                                                                                  | Suggested fix                                                                                                          |
|-----|----------------------------------------|-----------------------------------------|-------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| 1   | app.py: `members_int_id` function (PUT method) | PUT /members/1 with membership_expiry_date | The `membership_expiry_date` is a `db.Date` column requiring a Python `date` object, but the PUT handler sets raw ISO string from JSON without conversion, causing SQLAlchemy `StatementError`. | Modify the PUT handler in `members_int_id` to convert `membership_expiry_date` string into a `date` object before setting it on the model, similar to what is done in the POST handler in `/members`. |
| 2   | app.py: `loans_int_id` function (PUT method)   | PUT /loans/1 with checkout_date, due_date | The `checkout_date` and `due_date` fields are `db.Date` columns but are assigned raw ISO string values from JSON in the PUT handler, causing SQLAlchemy `StatementError`. | Modify the PUT handler in `loans_int_id` to convert `checkout_date` and `due_date` strings into `date` objects before setting them on the Loan model instance. Implement same date parsing as in the POST handler for `/loans`. |
  
Explanation:  
- The POST handlers for `/members` and `/loans` already convert date strings to Python `date` objects before instantiating ORM models, which prevents the errors.  
- The PUT handlers, however, directly assign the JSON values without date conversion, causing the mismatch and failure.  
- Other requests passed successfully, indicating that the database schema and model relations are correct and not the source of the failures.

This fix plan addresses the root cause precisely and provides consistency to date handling throughout the API.  
No missing fields or faulty relationships are identified.  
No other routes or model definitions require modifications based on the failing tests.

# Summary of Action Items

- In app.py, `members_int_id` PUT method: add date conversion for `membership_expiry_date`.
- In app.py, `loans_int_id` PUT method: add date conversions for `checkout_date` and `due_date`.

This will prevent the `TypeError` caused by assigning strings to SQLite `Date` columns and fix the 500 errors seen in the PUT requests for members and loans.