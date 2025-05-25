1. POST /users -> Needs { email: string, password: string, name: string }
   Returns: newly created user data with hashed password stored internally.
2. POST /users/login -> Needs { email: string, password: string }
   Returns: user data if authentication succeeds, otherwise 401 with message.
3. POST /users/<int:id>/reminder_periods -> Needs { days_before_deadline: integer }
   Returns: newly created reminder period for specified user.
4. POST /theses -> Needs { type: string, title: string, description: string, student_name: string, start_supervision_date: string, official_registration_date: string, submission_date: string, colloquium_date: string, grade: string, second_examiner_id: integer }
   Returns: newly created thesis data.
5. POST /theses/<int:id>/supervisors -> Needs { assignment_date: string, user_id: integer }
   Returns: newly created supervisor assignment for specified thesis.
6. POST /theses/<int:id>/meeting_notes -> Needs { date: string, content: string, author_id: integer }
   Returns: newly created meeting note for specified thesis.
7. GET /users/<int:id>/notification_settings
   Returns: array with one notification settings object or empty array if none.
8. GET /users/<int:id>/reminder_periods
   Returns: list of reminder periods for the user.
9. GET /theses
   Returns: list of all theses.
10. GET /theses/type/<string:type>
    Returns: list of theses filtered by thesis type, or 404 if none found.
11. GET /theses/grade/<string:grade>
    Returns: list of theses filtered by grade, or 404 if none found.
12. GET /theses/second_examiner/<int:user_id>
    Returns: list of theses filtered by second examiner user ID, or 404 if none found.
13. GET /theses/supervisor/<int:user_id>
    Returns: list of theses filtered by supervisor user ID via supervisor assignments, or 404 if none found.
14. GET /theses/deadline_proximity/<int:days>
    Returns: list of theses with submission_date within given deadline proximity, or 404 if none found.
15. GET /theses/<int:id>
    Returns: thesis data by ID, or 404 if not found.
16. GET /theses/<int:id>/supervisors
    Returns: list of supervisors assigned to the thesis, or 404 if thesis not found.
17. GET /theses/<int:id>/meeting_notes
    Returns: list of meeting notes for thesis, or 404 if thesis not found.
18. GET /theses/<int:id>/meeting_notes/<int:note_id>
    Returns: meeting note by thesis ID and note ID, or 404 if not found.
19. GET /theses/<int:id>/deadline
    Returns: deadline object for thesis, empty object if no deadline, or 404 if thesis not found.
20. GET /dashboard
    Returns: aggregated thesis overview list.
21. PUT /users/<int:id>/notification_settings -> Needs { in_app_enabled: boolean, email_enabled: boolean }
    Returns: updated notification settings if exist, otherwise creates new and returns it.
22. PUT /users/<int:id>/reminder_periods/<int:reminder_id> -> Needs { days_before_deadline: integer }
    Returns: updated reminder period, or 404 if not found.
23. PUT /theses/<int:id> -> Needs { type: string, title: string, description: string, student_name: string, start_supervision_date: string, official_registration_date: string, submission_date: string, colloquium_date: string, grade: string, second_examiner_id: integer }
    Returns: updated thesis data, or 404 if not found.
24. PUT /theses/<int:id>/supervisors -> Needs list of { assignment_date: string, user_id: integer }
    Returns: message indicating supervisors replaced, or 404 if thesis not found.
25. PUT /theses/<int:id>/meeting_notes/<int:note_id> -> Needs { date: string, content: string, author_id: integer }
    Returns: updated meeting note, or 404 if not found.
26. PUT /theses/<int:id>/deadline -> Needs { deadline_date: string }
    Returns: updated or newly created deadline for thesis, or 404 if thesis not found.
27. DELETE /users/<int:id>/reminder_periods/<int:reminder_id>
    Behavior: deletes existing reminder period by user ID and reminder ID; 404 if not found.
28. DELETE /theses/<int:id>/supervisors/<int:user_id>
    Behavior: deletes specific supervisor assignment by thesis ID and supervisor user ID; 404 if not found.
29. DELETE /theses/<int:id>/meeting_notes/<int:note_id>
    Behavior: deletes specific meeting note by thesis ID and note ID; 404 if not found.
30. DELETE /theses/<int:id>
    Behavior: deletes thesis by ID, cascading deletion of supervisor assignments, meeting notes, and deadline; 404 if not found.
31. DELETE /users/<int:id>
    Behavior: deletes user by ID, cascading deletion of supervisor assignments, notification settings, reminder periods; 404 if not found.

Explanation to ensure correctness of DELETE order:

- ReminderPeriod is child of User, so reminder periods must be deleted before users (route 27 before 31).
- SupervisorAssignment, MeetingNote, Deadline are children of Thesis; their deletes come before thesis delete (routes 28, 29 before 30).
- No DELETE route appears before any GET or PUT route.
- The order respects POST → GET → PUT → DELETE for each model.
- Dependencies honored in DELETE routes, children deleted before parents.

This completes a strict, coherent, and dependency-compliant API endpoint test execution plan.