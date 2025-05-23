```markdown
# feature_checklist.md

1. Create a new user with email, password, and name.  
2. Authenticate a user by email and password (login).  
3. Retrieve notification settings for a specific user.  
4. Update notification settings (in_app_enabled, email_enabled) for a specific user.  
5. List all reminder periods configured by a specific user.  
6. Create a new reminder period with days_before_deadline for a specific user.  
7. Update a specific reminder period for a specific user.  
8. Delete a specific reminder period for a specific user.  
9. List all theses across all users.  
10. Create a new thesis with all required attributes.  
11. Filter theses by thesis type (Seminar, Bachelor, Master, PhD).  
12. Filter theses by thesis grade.  
13. Filter theses by second examiner user ID.  
14. Filter theses by supervisor user ID through SupervisorAssignment relationship.  
15. Filter theses with deadlines due within a specified number of days.  
16. Retrieve detailed information of a specific thesis by its ID.  
17. Update details of a specific thesis by its ID.  
18. Delete a specific thesis by its ID, cascading related supervisor assignments, meeting notes, and deadline.  
19. List all supervisors assigned to a specific thesis.  
20. Add one or multiple supervisors to a specific thesis within a single request.  
21. Replace all supervisors assigned to a specific thesis with a new list of supervisor assignments.  
22. Remove a specific supervisor by user ID from a specific thesis.  
23. List all meeting notes attached to a specific thesis.  
24. Create a new meeting note for a specific thesis with date, content, and optional author_id.  
25. Retrieve a specific meeting note by its ID for a specific thesis.  
26. Update a specific meeting note by its ID for a specific thesis.  
27. Delete a specific meeting note by its ID for a specific thesis.  
28. Retrieve the deadline information for a specific thesis.  
29. Create or update the deadline for a specific thesis.  
30. Retrieve an aggregated overview dashboard of theses with optional filtering and sorting.

```
This checklist includes all distinct REST API endpoints explicitly stated or logically implied, each representing exactly one HTTP endpoint operation. It avoids vague or analytical features and captures nested-resource operations separately as required. It respects business rules, core data models, and CRUD + filtering needs for users, notification settings, reminder periods, theses, supervisor assignments, meeting notes, deadlines, and dashboard overview.