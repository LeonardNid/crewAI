```markdown
# entity_overview.md

## Entities Catalogue

### User
- **Description**: Represents a person who interacts with the thesis management system. Users can be students (thesis authors), supervisors, second examiners, or other roles identified by their involvement with theses.
- **Attributes**:  
  - email (string): Unique login identifier.  
  - password (hashed string): Secure credential for authentication.  
  - name (string): Full user name.
- **Relations**:  
  - 1-n SupervisorAssignment (a user can supervise multiple theses).  
  - 1-n MeetingNote (a user can optionally author multiple meeting notes).  
  - 1-1 NotificationSettings (each user has exactly one notification preferences record).  
  - 1-n ReminderPeriod (a user may have multiple reminder periods configured).  
  - Referenced by Thesis as second_examiner (a user may serve as second examiner for multiple theses).

---

### Thesis
- **Description**: Represents an academic thesis project with metadata including type, timeline, supervision, and assessment.
- **Attributes**:  
  - type (enum): Category of thesis; one of Seminar, Bachelor, Master, PhD.  
  - title (string): Official title of the thesis.  
  - description (string): Abstract or comprehensive description.  
  - student_name (string): Name of the thesis author (student).  
  - start_supervision_date (date): Date supervision commenced.  
  - official_registration_date (date): Date of formal thesis registration.  
  - submission_date (date): Date thesis was submitted for review.  
  - colloquium_date (date): Date of thesis defense or presentation.  
  - grade (string): Final grade awarded to the thesis.  
  - second_examiner_id (foreign key to User): The user assigned as second examiner.
- **Relations**:  
  - n-n User via SupervisorAssignment (multiple supervisors can be assigned per thesis).  
  - 1-n MeetingNote (multiple meeting notes related to the thesis).  
  - 1-1 Deadline (a single deadline record per thesis).  
  - Referenced by SupervisorAssignment entities to link supervisors.  
  - References User as second_examiner.

---

### SupervisorAssignment
- **Description**: Junction entity linking a User (supervisor) and a Thesis, representing the supervisory role assignment with metadata.
- **Attributes**:  
  - assignment_date (date): Date the supervisor was assigned to the thesis.
- **Relations**:  
  - n-1 User (supervisor).  
  - n-1 Thesis (the supervised thesis).
- **Business Rules**:  
  - Each (User, Thesis) pair is unique to prevent duplicate supervisor assignments.

---

### MeetingNote
- **Description**: Note or record documenting discussions or meetings related to a thesis. May be authored by a user or remain anonymous.
- **Attributes**:  
  - date (date): Date of the note or meeting.  
  - content (string): Text content of the note.  
  - author_id (optional foreign key to User): User who authored the note (optional).
- **Relations**:  
  - n-1 Thesis (each note belongs to exactly one thesis).  
  - optional n-1 User (author of the note).

---

### NotificationSettings
- **Description**: Stores per-user preferences for notification delivery via the app or email.
- **Attributes**:  
  - in_app_enabled (boolean): Flag to enable/disable in-app notifications.  
  - email_enabled (boolean): Flag to enable/disable email notifications.
- **Relations**:  
  - 1-1 User (each user has exactly one notification settings record).
- **Business Rules**:  
  - Exactly one NotificationSettings per User; created only if missing to avoid duplicates.

---

### Deadline
- **Description**: Defines a formal deadline date associated with a thesis, e.g., submission or defense deadline.
- **Attributes**:  
  - deadline_date (date): Deadline date for the thesis.
- **Relations**:  
  - 1-1 Thesis (each thesis has one deadline record).
- **Business Rules**:  
  - One Deadline per Thesis; created only if missing to prevent duplicates.

---

### ReminderPeriod
- **Description**: User-defined configuration specifying how many days before a thesis deadline a reminder should be sent.
- **Attributes**:  
  - days_before_deadline (integer): Number of days before the deadline when a reminder triggers.
- **Relations**:  
  - n-1 User (belongs to one user).
- **Business Rules**:  
  - Multiple ReminderPeriods are allowed per user to support multiple reminders per deadline.

---

## Summary of Relationships

- **User**  
  - Has many SupervisorAssignments (supervises many theses).  
  - Can author many MeetingNotes (optional association).  
  - Has one NotificationSettings record.  
  - Has many ReminderPeriods.  
  - May be assigned as second_examiner to multiple theses.

- **Thesis**  
  - Has many User supervisors via SupervisorAssignment (many-to-many).  
  - Has many MeetingNotes.  
  - Has one Deadline.  
  - References User as second_examiner.

- **SupervisorAssignment**  
  - Joins User and Thesis; tracks assignment_date.  
  - Unique per (User, Thesis) pair.

- **MeetingNote**  
  - Belongs to one Thesis.  
  - Optional link to one User author.

- **NotificationSettings**  
  - One-to-one with User.

- **Deadline**  
  - One-to-one with Thesis.

- **ReminderPeriod**  
  - Belongs to one User.

---

## Business Rules Summary

- When a User is deleted, cascade deletes to SupervisorAssignments and NotificationSettings for that user.  
- When a Thesis is deleted, cascade deletes to its SupervisorAssignments, MeetingNotes, and Deadline.  
- Prevent assigning the same User as supervisor multiple times to the same Thesis.  
- Supervisors and second examiners must exist in the User table before assignment.  
- NotificationSettings and Deadline records are singletons per User and Thesis, created only if absent.  
- Users may configure multiple ReminderPeriods for various reminder schedules.

```
This entity catalogue fully covers all domain objects, attributes, and relationships described in the input, aligned with the essential business rules and usage needs of the thesis management system.