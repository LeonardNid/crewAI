{
  "requests": [
    {
      "route": "/users",
      "method": "POST",
      "json_data": {
        "email": "user@example.com",
        "password": "password123",
        "name": "John Doe"
      }
    },
    {
      "route": "/users/login",
      "method": "POST",
      "json_data": {
        "email": "user@example.com",
        "password": "password123"
      }
    },
    {
      "route": "/users/1/reminder_periods",
      "method": "POST",
      "json_data": {
        "days_before_deadline": 5
      }
    },
    {
      "route": "/theses",
      "method": "POST",
      "json_data": {
        "type": "Master",
        "title": "Thesis Title",
        "description": "Description of the thesis.",
        "student_name": "Alice Student",
        "start_supervision_date": "2024-01-01",
        "official_registration_date": "2024-01-10",
        "submission_date": "2024-12-15",
        "colloquium_date": "2025-01-20",
        "grade": "A",
        "second_examiner_id": 1
      }
    },
    {
      "route": "/theses/1/supervisors",
      "method": "POST",
      "json_data": {
        "assignment_date": "2024-01-01",
        "user_id": 1
      }
    },
    {
      "route": "/theses/1/meeting_notes",
      "method": "POST",
      "json_data": {
        "date": "2024-02-15",
        "content": "Discussed thesis progress.",
        "author_id": 1
      }
    },
    {
      "route": "/users/1/notification_settings",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/users/1/reminder_periods",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/type/Master",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/grade/A",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/second_examiner/1",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/supervisor/1",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/deadline_proximity/7",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/1",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/1/supervisors",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/1/meeting_notes",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/1/meeting_notes/1",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/theses/1/deadline",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/dashboard",
      "method": "GET",
      "json_data": null
    },
    {
      "route": "/users/1/notification_settings",
      "method": "PUT",
      "json_data": {
        "in_app_enabled": true,
        "email_enabled": false
      }
    },
    {
      "route": "/users/1/reminder_periods/1",
      "method": "PUT",
      "json_data": {
        "days_before_deadline": 3
      }
    },
    {
      "route": "/theses/1",
      "method": "PUT",
      "json_data": {
        "type": "Master",
        "title": "Updated Thesis Title",
        "description": "Updated description",
        "student_name": "Alice Student",
        "start_supervision_date": "2024-01-02",
        "official_registration_date": "2024-01-12",
        "submission_date": "2024-12-20",
        "colloquium_date": "2025-01-25",
        "grade": "B",
        "second_examiner_id": 2
      }
    },
    {
      "route": "/theses/1/supervisors",
      "method": "PUT",
      "json_data": {
        "assignment_date": "2024-02-01",
        "user_id": 2
      }
    },
    {
      "route": "/theses/1/meeting_notes/1",
      "method": "PUT",
      "json_data": {
        "date": "2024-03-01",
        "content": "Updated meeting notes content.",
        "author_id": 2
      }
    },
    {
      "route": "/theses/1/deadline",
      "method": "PUT",
      "json_data": {
        "deadline_date": "2024-12-25"
      }
    },
    {
      "route": "/users/1/reminder_periods/1",
      "method": "DELETE",
      "json_data": null
    },
    {
      "route": "/theses/1/supervisors/1",
      "method": "DELETE",
      "json_data": null
    },
    {
      "route": "/theses/1/meeting_notes/1",
      "method": "DELETE",
      "json_data": null
    },
    {
      "route": "/theses/1",
      "method": "DELETE",
      "json_data": null
    },
    {
      "route": "/users/1",
      "method": "DELETE",
      "json_data": null
    }
  ]
}