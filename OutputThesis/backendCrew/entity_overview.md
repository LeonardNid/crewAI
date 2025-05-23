```markdown
# entity_overview.md

## Entities and Relationships Catalogue for Thesis Management Application

---

## 1. User
- Description: Represents professors and system users who register and login via email; they supervise, examine, and manage theses with secure authentication and personalized notification and reminder preferences.
- Attributes:
  - User ID (unique identifier)
  - Email (used for registration and login)
  - Password (securely hashed)
  - Name (full name)
- Relations:
  - User 1-n SupervisorAssignment (a user can supervise multiple theses)
  - User 1-n Thesis as Second Examiner (one user can be assigned as second examiner for multiple theses)
  - User 1-1 NotificationSettings (each user has one notification settings record)
  - User 1-n MeetingNote as Creator (optional, for meeting note authorship tracking)
- Cascade behavior:
  - Deleting a User cascades to their SupervisorAssignments and NotificationSettings
  - Deleting a User requires defined handling of associated MeetingNotes (cascade or reassignment) to avoid data loss

---

## 2. Thesis
- Description: Represents an academic thesis encompassing type, student info, supervision, deadlines, evaluations, and associated meeting notes.
- Attributes:
  - Thesis ID (unique identifier)
  - Thesis Type (enumeration: Seminar, Bachelor, Master, PhD)
  - Title (string)
  - Description (detailed text)
  - Student Name (string)
  - Start of Supervision Date (date)
  - Official Registration Date (date)
  - Submission Date (date, optional)
  - Colloquium Date (date, optional)
  - Grade (final evaluation, optional)
- Relations:
  - Thesis 1-n SupervisorAssignment (supports multiple supervisors for a thesis)
  - Thesis 1-1 User as Second Examiner (one user assigned as second examiner per thesis)
  - Thesis 1-n MeetingNote (collection of meeting notes related to supervision)
  - Thesis 1-1 Deadline (one dedicated deadline entity per thesis with date and reminders)
- Cascade behavior:
  - Deleting a Thesis cascades deletions to SupervisorAssignments, MeetingNotes, and Deadline entities

---

## 3. SupervisorAssignment
- Description: Join entity associating Users (supervisors) to Theses, enabling multiple supervisors per thesis.
- Attributes:
  - SupervisorAssignment ID (unique identifier)
  - Thesis ID (foreign key)
  - User ID (foreign key)
  - Assigned Date (date when supervisor assignment was made, optional)
- Relations:
  - SupervisorAssignment n-1 User (references one supervisor)
  - SupervisorAssignment n-1 Thesis (references one thesis)
- Cascade behavior:
  - Deleting referenced User or Thesis cascades to delete SupervisorAssignment entries

---

## 4. MeetingNote
- Description: Captures detailed notes from meetings related to thesis supervision to assist progress tracking.
- Attributes:
  - MeetingNote ID (unique identifier)
  - Thesis ID (foreign key)
  - Date (date of meeting)
  - Summary/Description (text of meeting notes)
  - Creator User ID (foreign key to User, optional - tracks note creator)
- Relations:
  - MeetingNote n-1 Thesis (linked to a specific thesis)
  - MeetingNote n-1 User Creator (optional, to track author)
- Cascade behavior:
  - Deleting a Thesis deletes its MeetingNotes
  - Deleting a User requires resolution for associated MeetingNotes (e.g., reassignment or retention strategy)

---

## 5. NotificationSettings
- Description: Stores user-specific preferences regarding notifications and default reminder timing for deadlines.
- Attributes:
  - NotificationSettings ID (unique identifier)
  - User ID (foreign key)
  - Enable In-App Notifications (boolean)
  - Enable Email Notifications (boolean)
- Relations:
  - NotificationSettings 1-1 User (one notification settings per user)
- Cascade behavior:
  - Deleting a User cascades to deleting their NotificationSettings

---

## 6. ReminderPeriod
- Description: Defines individual reminder periods (days before deadline) associated either globally per user or overridden per thesis deadline.
- Attributes:
  - ReminderPeriod ID (unique identifier)
  - User ID (foreign key, nullable if global for NotificationSettings)
  - Thesis ID (foreign key, nullable for user-wide default)
  - Days Before Deadline (integer number of days before deadline when reminder should trigger)
- Relations:
  - ReminderPeriod many-1 User (for user-specific reminder periods)
  - ReminderPeriod many-1 Thesis (optional override specific to a thesis)
- Cascade behavior:
  - Deleting User or Thesis cascades to delete corresponding reminder periods

---

## 7. Deadline
- Description: Represents the official deadline date of a thesis, together with custom reminder periods overriding user defaults.
- Attributes:
  - Deadline ID (unique identifier)
  - Thesis ID (foreign key, unique)
  - Deadline Date (date)
- Relations:
  - Deadline 1-1 Thesis (each thesis has one deadline)
  - Deadline 1-n ReminderPeriod (optional per-thesis reminder overrides)
- Cascade behavior:
  - Deleting a Thesis cascades to delete its Deadline (and its related ReminderPeriods)

---

## Summary of Key Relationships

- User 1-n SupervisorAssignment (a user supervises many theses)
- Thesis 1-n SupervisorAssignment (a thesis can have multiple supervisors)
- SupervisorAssignment n-1 User (each assignment references one supervisor)
- SupervisorAssignment n-1 Thesis (each assignment references one thesis)
- Thesis 1-1 User as Second Examiner (one user assigned per thesis as second examiner)
- User 1-1 NotificationSettings (one notification setting record per user)
- User 1-n ReminderPeriod (user-level default reminder periods)
- Thesis 1-1 Deadline (each thesis has a unique deadline record)
- Deadline 1-n ReminderPeriod (deadline-specific reminder periods overriding user defaults)
- Thesis 1-n MeetingNote (a thesis can have multiple meeting notes)
- MeetingNote n-1 User Creator (optional note author tracking)

---

## Summary of Correspondence to Core Features and Use-Cases

This comprehensive entity model fully supports the following:

- User registration and authentication via email with secure password handling (User)
- Full CRUD operations for thesis records including metadata, student data, supervision timelines, grades, and second examiner (Thesis)
- Managing multiple supervisor assignments per thesis reliably via SupervisorAssignment, including batch assignment and updates
- Assigning and querying the second examiner per thesis (User relationship)
- Managing meeting notes per thesis with create, read, update, delete capabilities and optional author tracking (MeetingNote)
- Configuring and managing deadlines per thesis with customizable reminder periods that can override user defaults (Deadline, ReminderPeriod)
- User-configurable notification preferences for enabling/disabling in-app and email notifications (NotificationSettings)
- User and thesis based reminder periods for granular control of notification timing (ReminderPeriod)
- Filtering and sorting of theses on dashboard by thesis type, grade, supervisors (via SupervisorAssignment), second examiner, and deadline proximity using established relationships and attributes
- Maintaining referential integrity via cascading deletes and well-defined entity relationships across all entities to avoid orphan or inconsistent data

This model removes previously invalid or missing attributes such as thesis status and integrates all necessary scaffolding to implement every feature according to the detailed feature checklist, ensuring robustness and alignment with business needs.

```
This entity and relationship catalogue fully matches the clarified and corrected feature checklist and business requirements, enabling precise, testable implementation of the Thesis Management Application.