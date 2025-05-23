1. POST /users -> Needs { email: string, password: string, name: string }  
   Returns: newly created user data excluding password_hash.  
2. GET /users -> Returns: list of all users excluding their password_hash.  
3. POST /users_login -> Needs { email: string, password: string }  
   Returns: authenticated user data excluding password_hash or 401 if invalid credentials.  
4. GET /users_<int:user_id>_notification_settings -> Returns: user's notification settings; creates default if none exist.  
5. PUT /users_<int:user_id>_notification_settings -> Needs { in_app_enabled: boolean, email_enabled: boolean }  
   Returns: updated notification settings.  
6. POST /users_<int:user_id>_reminder_periods -> Needs { days_before_deadline: integer }  
   Returns: newly created reminder period for user.  
7. GET /users_<int:user_id>_reminder_periods -> Returns: list of reminder periods for user.  
8. PUT /users_<int:user_id>_reminder_periods_<int:id> -> Needs { days_before_deadline: integer }  
   Returns: updated reminder period or 404 if not found.  
9. DELETE /users_<int:user_id>_reminder_periods_<int:id> -> Returns: message on successful deletion or 404 if not found.  
10. POST /theses -> Needs { type: string, title: string, description: string, student_name: string, start_supervision_date: string (ISO date), official_registration_date: string (ISO date), submission_date: string (ISO date), colloquium_date: string (ISO date), grade: string, second_examiner_id: integer }  
    Returns: newly created thesis data.  
11. GET /theses -> Returns: list of all theses with normalized 'type' field.  
12. GET /theses_type_<string:type> -> Returns: list of theses filtered by normalized type.  
13. GET /theses_grade_<string:grade> -> Returns: list of theses filtered by grade.  
14. GET /theses_second_examiner_<int:user_id> -> Returns: list of theses filtered by second examiner's user ID.  
15. GET /theses_supervisor_<int:user_id> -> Returns: list of theses supervised by user via SupervisorAssignment.  
16. GET /theses_deadline_proximity_<int:days> -> Returns: theses with submission_date within specified days from now.  
17. GET /theses_<int:id> -> Returns: thesis by ID or 404 if not found.  
18. PUT /theses_<int:id> -> Needs { type: string, title: string, description: string, student_name: string, start_supervision_date: string (ISO date), official_registration_date: string (ISO date), submission_date: string (ISO date), colloquium_date: string (ISO date), grade: string, second_examiner_id: integer }  
    Returns: updated thesis or 404 if not found.  
19. POST /theses_<int:thesis_id>_supervisors -> Needs { assignments: [ { user_id: integer, assignment_date: string (ISO date) } ] }  
    Returns: list of newly created supervisor assignments.  
20. PUT /theses_<int:thesis_id>_supervisors -> Needs { assignments: [ { user_id: integer, assignment_date: string (ISO date) } ] }  
    Returns: list of replaced supervisor assignments.  
21. GET /theses_<int:thesis_id>_supervisors -> Returns: list of supervisor assignments for thesis.  
22. DELETE /theses_<int:thesis_id>_supervisors_<int:user_id> -> Returns: message on successful deletion or 404 if not found.  
23. POST /theses_<int:thesis_id>_meeting_notes -> Needs { date: string (ISO date), content: string, author_id: integer }  
    Returns: newly created meeting note.  
24. GET /theses_<int:thesis_id>_meeting_notes -> Returns: list of meeting notes for thesis.  
25. GET /theses_<int:thesis_id>_meeting_notes_<int:id> -> Returns: specific meeting note or 404.  
26. PUT /theses_<int:thesis_id>_meeting_notes_<int:id> -> Needs { date: string (ISO date), content: string, thesis_id: integer, author_id: integer }  
    Returns: updated meeting note or 404 if not found.  
27. DELETE /theses_<int:thesis_id>_meeting_notes_<int:id> -> Returns: message on successful deletion or 404 if not found.  
28. GET /theses_<int:thesis_id>_deadline -> Returns: deadline info for thesis or 404.  
29. PUT /theses_<int:thesis_id>_deadline -> Needs { deadline_date: string (ISO date) }  
    Returns: newly created or updated deadline for thesis.  
30. DELETE /theses_<int:id> -> Returns: message on successful thesis deletion or 404 if not found. Deletion cascades supervisor assignments, meeting notes, and deadline.  
31. GET /dashboard -> Returns: aggregated thesis overview with normalized 'type'.  
32. POST /billtasks -> Needs { task_name: string, due_date: string (ISO date), priority: integer, completed: boolean }  
    Returns: newly created bill task.  
33. GET /billtasks -> Returns: list of all bill tasks.  
34. GET /billtasks/<int:id> -> Returns: bill task by ID or 404.  
35. PUT /billtasks/<int:id> -> Needs { task_name: string, due_date: string (ISO date), priority: integer, completed: boolean }  
    Returns: updated bill task or 404 if not found.  
36. DELETE /billtasks/<int:id> -> Returns: message on successful deletion or 404 if not found.  
37. POST /calpolicys -> Needs { policy_name: string, effective_date: string (ISO date), expiration_date: string (ISO date), active: boolean }  
    Returns: newly created calpolicy.  
38. GET /calpolicys -> Returns: list of all calpolicys.  
39. GET /calpolicys/<int:id> -> Returns: calpolicy by ID or 404.  
40. PUT /calpolicys/<int:id> -> Needs { policy_name: string, effective_date: string (ISO date), expiration_date: string (ISO date), active: boolean }  
    Returns: updated calpolicy or 404 if not found.  
41. DELETE /calpolicys/<int:id> -> Returns: message on successful deletion or 404 if not found.  
42. POST /campaigns -> Needs { campaign_name: string, start_date: string (ISO date), end_date: string (ISO date), budget: number }  
    Returns: newly created campaign.  
43. GET /campaigns -> Returns: list of all campaigns.  
44. GET /campaigns/<int:id> -> Returns: campaign by ID or 404.  
45. PUT /campaigns/<int:id> -> Needs { campaign_name: string, start_date: string (ISO date), end_date: string (ISO date), budget: number }  
    Returns: updated campaign or 404 if not found.  
46. DELETE /campaigns/<int:id> -> Returns: message on successful deletion or 404 if not found.  
47. POST /discountdistributions -> Needs { distribution_name: string, discount_percentage: number, valid_from: string (ISO date), valid_to: string (ISO date) }  
    Returns: newly created discount distribution.  
48. GET /discountdistributions -> Returns: list of all discount distributions.  
49. GET /discountdistributions/<int:id> -> Returns: discount distribution by ID or 404.  
50. PUT /discountdistributions/<int:id> -> Needs { distribution_name: string, discount_percentage: number, valid_from: string (ISO date), valid_to: string (ISO date) }  
    Returns: updated discount distribution or 404 if not found.  
51. DELETE /discountdistributions/<int:id> -> Returns: message on successful deletion or 404 if not found.  
52. POST /donorrewards -> Needs { reward_type: string, amount: number }  
    Returns: newly created donor reward.  
53. GET /donorrewards -> Returns: list of all donor rewards.  
54. GET /donorrewards/<int:id> -> Returns: donor reward by ID or 404.  
55. PUT /donorrewards/<int:id> -> Needs { reward_type: string, amount: number }  
    Returns: updated donor reward or 404 if not found.  
56. DELETE /donorrewards/<int:id> -> Returns: message on successful deletion or 404 if not found.  

Note on DELETE ordering:  
- For Thesis related deletes, child resources such as SupervisorAssignment, MeetingNote, and Deadline are deleted automatically due to cascade on thesis deletion (route 30).  
- Separate deletes for SupervisorAssignment and MeetingNote exist for specific entries and come before deleting Thesis (routes 22 and 27).  
- BillTask, CalPolicy, Campaign, DiscountDistribution, and DonorReward have independent DELETE endpoints and no indicated dependencies; order of their DELETE routes respects no dependencies between them.  

All routes follow the strict POST→GET→PUT→DELETE order per model and respect dependency order for DELETE.