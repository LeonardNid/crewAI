1. POST /users -> Needs { email: string, password: string, name: string }
   Returns: newly created user data with id.
2. POST /users/login -> Needs { email: string, password: string }
   Returns: message indicating login success or failure.
3. POST /users/<int:user_id>/reminder_periods -> Needs { days_before_deadline: integer, thesis_id: integer (optional) }
   Returns: newly created reminder period data with id.
4. POST /theses -> Needs { thesis_type: string, title: string, description: string, student_name: string, start_supervision_date: string, official_registration_date: string, submission_date: string, colloquium_date: string, grade: string, second_examiner_id: integer }
   Returns: newly created thesis data with id.
5. POST /theses/<int:thesis_id>/supervisors -> Needs { user_ids: list of integers }
   Returns: list of newly created supervisor assignments data.
6. POST /theses/<int:thesis_id>/meeting_notes -> Needs { date: string, summary: string, creator_id: integer }
   Returns: newly created meeting note data with id.
7. GET /users/<int:user_id>/notification_settings
   Returns: notification settings data or empty JSON if none.
8. GET /users/<int:user_id>/reminder_periods
   Returns: list of reminder periods for the user.
9. GET /theses
   Returns: list of all theses.
10. GET /theses/type/<string:thesis_type>
    Returns: list of theses filtered by thesis_type or 404 if none.
11. GET /theses/grade/<string:grade>
    Returns: list of theses filtered by grade or 404 if none.
12. GET /theses/second_examiner/<int:user_id>
    Returns: list of theses filtered by second_examiner_id or 404 if none.
13. GET /theses/supervisor/<int:user_id>
    Returns: list of theses supervised by user_id via SupervisorAssignment or 404 if none.
14. GET /theses/deadline_proximity/<int:days>
    Returns: list of theses with deadlines within given days or 404 if none.
15. GET /theses/<int:id>
    Returns: a single thesis by id or 404 if not found.
16. GET /theses/<int:thesis_id>/supervisors
    Returns: list of supervisor assignments for thesis.
17. GET /theses/<int:thesis_id>/meeting_notes
    Returns: list of meeting notes for thesis.
18. GET /theses/<int:thesis_id>/meeting_notes/<int:note_id>
    Returns: single meeting note by note_id within thesis or 404 if not found.
19. GET /theses/<int:thesis_id>/deadline
    Returns: deadline info for thesis or empty JSON if none.
20. GET /dashboard
    Returns: dashboard data with thesis list and filters.
21. PUT /users/<int:user_id>/notification_settings -> Needs { in_app_enabled: boolean, email_enabled: boolean }
    Returns: updated notification settings.
22. PUT /users/<int:user_id>/reminder_periods -> Needs { id: integer (existing ReminderPeriod), days_before_deadline: integer (optional), thesis_id: integer (optional) }
    Note: Requires the id field to locate the existing reminder period.
    Returns: updated reminder period data.
23. PUT /theses/<int:id> -> Needs { thesis_type: string, title: string, description: string, student_name: string, start_supervision_date: string, official_registration_date: string, submission_date: string, colloquium_date: string, grade: string, second_examiner_id: integer }
    Returns: updated thesis data.
24. PUT /theses/<int:thesis_id>/supervisors -> Needs { user_ids: list of integers }
    Returns: updated list of supervisor assignments replacing previous for the thesis.
25. PUT /theses/<int:thesis_id>/meeting_notes/<int:note_id> -> Needs { date: string, summary: string, creator_id: integer }
    Returns: updated meeting note data.
26. PUT /theses/<int:thesis_id>/deadline -> Needs { deadline_date: string }
    Returns: updated or newly created deadline data.
27. DELETE /theses/<int:thesis_id>/meeting_notes/<int:note_id>
    Description: Deletes a single meeting note within a thesis.
    Returns: message confirming deletion.
28. DELETE /theses/<int:thesis_id>/supervisors/<int:user_id>
    Description: Deletes a supervisor assignment by thesis and user.
    Returns: message confirming deletion.
29. DELETE /users/<int:user_id>/reminder_periods?id=<reminder_period_id>
    Description: Deletes a reminder period by id for a user.
    Returns: message confirming deletion.
30. DELETE /theses/<int:id>
    Description: Deletes a thesis by id with cascading delete to SupervisorAssignment and MeetingNote.
    Returns: message confirming deletion.