```markdown
# entity_overview.md

## User
- Description: Represents system users including students, supervisors, and second examiners.
- Attributes:
  - email (unique, used for login)
  - password (stored securely as a hash)
  - name
- Relations:
  - One-to-many to SupervisorAssignment (a User may supervise multiple Theses)
  - One-to-many to ReminderPeriod (a User can have multiple reminder periods)
  - One-to-one to NotificationSettings (each User has exactly one NotificationSettings)
  - One-to-many as second_examiner to Thesis (a User may be second examiner on multiple Theses)
  - One-to-many to MeetingNote as optional author (a User may author multiple MeetingNotes)
- Notes:
  - On deletion, cascades deletion of related SupervisorAssignments and NotificationSettings

## Thesis
- Description: Represents an academic thesis/project with supervision, milestones, grading, and evaluation information.
- Attributes:
  - type (Enum: Seminar, Bachelor, Master, PhD)
  - title
  - description
  - student_name
  - start_supervision_date
  - official_registration_date
  - submission_date
  - colloquium_date
  - grade
  - second_examiner_id (foreign key referencing User)
- Relations:
  - Many-to-many to User via SupervisorAssignment (multiple supervisors can be assigned)
  - One-to-many to MeetingNote (a Thesis can have multiple meeting notes)
  - One-to-one to Deadline (each Thesis can have zero or one Deadline)
- Notes:
  - Deletion cascades to SupervisorAssignments, MeetingNotes, and Deadline

## SupervisorAssignment
- Description: Junction entity linking Users (supervisors) to Theses; tracks the assignment date.
- Attributes:
  - assignment_date
- Relations:
  - Many-to-one to Thesis
  - Many-to-one to User (supervisor)
- Business Rules:
  - Prevents duplicate assignments of the same User to the same Thesis

## MeetingNote
- Description: Notes recorded during meetings about a Thesis.
- Attributes:
  - date
  - content
  - author_id (optional foreign key to User as author; nullable)
- Relations:
  - Many-to-one to Thesis (each MeetingNote belongs to exactly one Thesis)
  - Optional many-to-one to User as author (nullable)
- Notes:
  - Deleted automatically when associated Thesis is deleted

## NotificationSettings
- Description: Stores notification preferences for an individual User.
- Attributes:
  - in_app_enabled (boolean)
  - email_enabled (boolean)
- Relations:
  - One-to-one to User (each User has exactly one NotificationSettings)
- Business Rules:
  - Created only if missing; updates overwrite preferences
- Notes:
  - Deleted when the User is deleted

## Deadline
- Description: Stores a single deadline date associated with a Thesis.
- Attributes:
  - deadline_date
- Relations:
  - One-to-one to Thesis (each Thesis has zero or one Deadline)
- Business Rules:
  - Created only if missing; can be updated
- Notes:
  - Deleted when associated Thesis is deleted

## ReminderPeriod
- Description: Configuration entity per User, specifying how many days before a Deadline reminders should be sent.
- Attributes:
  - days_before_deadline (integer)
- Relations:
  - Many-to-one to User (a User can have multiple ReminderPeriods)
- Business Rules:
  - Multiple distinct ReminderPeriods allowed per User; each ReminderPeriod belongs uniquely to one User
```