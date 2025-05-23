```markdown
# feature_checklist.md

1. Register a new user via email
2. Authenticate a user via email login
3. Create a new thesis record
4. Retrieve a list of all thesis records
5. Filter thesis records by thesis type
6. Filter thesis records by thesis grade
7. Filter thesis records by second examiner user ID
8. Retrieve thesis records supervised by a specific supervisor user ID (via SupervisorAssignment relationship)
9. Filter thesis records with deadlines due within X days (deadline proximity), implemented via query logic on custom deadline date
10. Retrieve details of a single thesis record by thesis ID
11. Update an existing thesis record by thesis ID
12. Delete an existing thesis record by thesis ID, cascading deletions to related supervisor assignments and meeting notes
13. Assign one or multiple supervisors to a thesis by thesis ID with a single POST endpoint accepting multiple supervisor user IDs
14. Retrieve all supervisors assigned to a specific thesis by thesis ID
15. Update the list of supervisors assigned to a thesis by thesis ID (e.g., replace existing supervisor assignments)
16. Remove a specific supervisor assignment from a thesis by thesis ID and supervisor user ID
17. Create a new meeting note for a specific thesis by thesis ID
18. Retrieve all meeting notes for a specific thesis by thesis ID
19. Retrieve a single meeting note by note ID within a thesis by thesis ID
20. Update an existing meeting note by note ID within a thesis by thesis ID
21. Delete a meeting note by note ID within a thesis by thesis ID
22. Set or update a custom deadline date for a thesis by thesis ID
23. Retrieve the custom deadline date and associated reminder settings for a thesis by thesis ID
24. Configure a user's notification preferences (enable/disable in-app notifications and email notifications) by user ID
25. Set or update reminder periods for deadlines by user ID and optionally by thesis ID (to support per-user and per-thesis reminder periods)
26. Retrieve notification and reminder settings for a user by user ID
27. Retrieve dashboard data including thesis list with sorting, filtering (thesis type, grade, supervisor, deadline proximity), and visual status indicators optimized for UI
```
This checklist strictly respects the one-REST-endpoint-per-feature rule, resolves previous defects by removing filters on non-existing 'status' field and using correct relationships (SupervisorAssignment) to filter supervisors, handling deadline proximity with query logic, properly supporting multiple supervisor assignments in batch, implementing update and delete for nested resources correctly, separating user notification and reminder settings into comprehensible APIs, and ensuring the dashboard endpoint supports advanced filtering and visual data as requested.