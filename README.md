# CheckMate - Milestone Project 3

**A comprehensive web platform providing user-friendly task and project management for individuals and teams, designed to streamline workflows and achieve goals.**

![Responsive Mockup](assets/readme/mockup.png)

## 1. Overview

Are you struggling to keep track of multiple projects, countless tasks, and critical deadlines? "CheckMate" is a powerful and intuitive Task Management System designed to help individuals and teams organise their work, streamline their workflows, and achieve their goals with strategic clarity. Inspired by the precision and planning of chess, CheckMate empowers users to move their tasks from "To Do" to "Completed" with confidence.

Navigating the complexities of modern workloads, whether personal or professional, often leads to disorganisation, missed deadlines, and a feeling of being overwhelmed. CheckMate is built to cut through this chaos, providing a centralised, straightforward solution for managing all aspects of task and project execution. This intelligent online tool empowers users to effortlessly create, assign, track, and complete tasks within a structured project environment, ensuring nothing falls through the cracks.
platform
Whether you're an individual aiming to master your daily to-do list, a student juggling assignments, or a team collaborating on a complex project, CheckMate offers a user-friendly platform to gain control over your work, fostering efficiency, accountability, and the ultimate satisfaction of a job well done.

## 2. Rationale

CheckMate is an online tool developed to provide a comprehensive and efficient means of managing tasks and projects. Its primary objective is to simplify workflow organisation, enhance productivity, and ensure successful completion of objectives for both individuals and collaborative teams.

The inspiration for CheckMate arose from observing the widespread challenge of effective task management. Many individuals and organisations struggle with scattered notes, forgotten deadlines, and unclear responsibilities, leading to inefficiencies, stress, and unfulfilled potential. This project aims to address these common pain points by offering a structured, intuitive, and readily accessible solution.

In today's fast-paced environment, the ability to effectively plan, execute, and monitor tasks is paramount. Whether it's daily chores, academic assignments, or complex professional endeavours, a robust system is crucial for success. However, existing solutions can often be overly complex, lack specific features, or fail to provide the clear oversight needed to bring tasks to their ultimate "checkmate."

The core problem that CheckMate seeks to resolve is the pervasive inefficiency and disorganisation associated with managing multiple tasks and projects without a centralised, coherent system. This can lead to wasted time, duplicated efforts, missed opportunities, and a general lack of clarity on progress.

CheckMate offers a user-friendly online platform where users can create projects, define tasks within those projects, assign tasks to team members, set priorities and due dates, and track progress through various statuses. The tool will provide intuitive interfaces for task and project creation, modification (CRUD functionality), and dynamic filtering/sorting options to quickly find relevant information. Key features include secure user authentication, distinct project workspaces, and clear visual feedback on task status. This approach provides a strategic and accessible alternative to fragmented planning methods.

CheckMate offers several advantages over current, less integrated methods. It provides significant time-saving through centralised management and streamlined workflows. The structured approach reduces the risk of missed deadlines and forgotten tasks, ensuring greater reliability and accountability. Furthermore, the clear and accessible interface empowers users to better understand their workload and focus on what truly matters. For teams, it facilitates seamless collaboration and provides transparent oversight of collective progress, aiding in adherence to project goals.

The initial scope of CheckMate focuses on providing core task and project management functionalities: user authentication, project creation/management, task CRUD operations (create, read, update, delete), task assignment, due dates, priorities, status tracking, and basic filtering/sorting. Acknowledged limitations include the initial focus on fundamental features before expanding to more advanced collaboration tools or integrations. Potential future enhancements for CheckMate include advanced reporting and analytics, integration with calendars or communication platforms, recurring tasks, sub-tasks, file attachments, and more granular notification settings for deadlines or changes.

In summary, CheckMate addresses a significant need by providing a user-friendly and accurate solution for managing tasks and projects. By simplifying this process, the tool has the potential to save time, reduce errors, improve focus, and ultimately contribute to the more efficient execution and successful completion of individual and collaborative endeavours.

## 3. User Experience (UX)

### User Stories

#### Feature 1: Secure User Authentication & Profile Management

**As a "CheckMate" user,** I want to securely register an account, log in, and manage my profile details so that I can access my personalised tasks and projects and maintain my personal information.

**Acceptance Criteria:**

- A registration form is present, requiring a unique username, email, and password (with confirmation).
- Passwords are securely hashed and stored (not plain text).
- Users can log in using their username/email and password.
- Successful login redirects to a user dashboard/main task view.
- Failed login attempts provide appropriate, non-revealing error messages.
- Users can view and update their first name, last name, and email on a profile page.
- Password change functionality is available, requiring current password verification.
- Session management ensures secure user experience (e.g., logout functionality, session expiration).

**Tasks:**

- Develop Flask routes for user registration, login, and logout.
- Implement a secure password hashing library.
- Create HTML forms for registration, login, and profile editing.
- Implement server-side validation for all form inputs (e.g., unique username/email, password strength, valid email format).
- Set up Flask-Login (or similar) for session management.
- Implement database interactions (INSERT for registration, SELECT for login, UPDATE for profile).
- Design a user profile page with editable fields.

#### Feature 2: Comprehensive Task Management (CRUD & Status Tracking)

**As a "CheckMate" user,** I want to create, view, edit, delete, and update the status of my tasks, so that I can effectively manage my workload and track progress.

**Acceptance Criteria:**

- Users can create new tasks, specifying a title, description, due date, priority, and optional project association.
- All tasks are displayed in a clear, organised list or board view.
- Each task entry clearly shows its title, due date, priority, and current status.
- Users can click on a task to view its full details in a dedicated view or modal.
- Users can edit any field of an existing task.
- Users can change a task's status (e.g., 'To Do', 'In Progress', 'Completed', 'Blocked').
- Users can delete tasks, with a confirmation prompt to prevent accidental deletion.
- Completed tasks are visually distinguishable (e.g., strikethrough, different background).

**Tasks:**

- Develop Flask routes and corresponding HTML templates for:
  - Displaying all tasks (e.g., /tasks or main dashboard).
  - Creating a new task (e.g., /tasks/new).
  - Viewing a single task (e.g., /tasks/\<id>).
  - Editing an existing task (e.g., /tasks/\<id>/edit).
  - Deleting a task (e.g., /tasks/\<id>/delete).
- Implement database CRUD operations for the tasks table.
- Create form handling for task creation and editing.
- Implement CSS for visual status indicators (colours, strikethrough).
- Add JavaScript for confirmation dialogues on deletion and potentially for dynamic status updates.

#### Feature 3: Project Organisation & Collaboration

**As a "CheckMate" user,** I want to create and manage projects, assign tasks within them, and invite other users to collaborate, so that I can organise larger initiatives and work effectively with a team.

**Acceptance Criteria:**

- Users can create new projects with a name and description.
- Users can view a list of all projects they own or are a member of.
- Each project view displays the tasks associated with it.
- Project owners can invite other registered users to become members of their projects.
- Project members can view and interact with tasks within that project based on their assigned role/permissions.
- Projects can be marked as 'Completed' or 'Archived'.

**Tasks:**

- Develop Flask routes and templates for:
- Creating new projects (e.g., /projects/new).
- Listing projects (e.g., /projects).
- Viewing a single project and its tasks (e.g., /projects/\<id>).
- Adding/removing project members.
- Implement database CRUD operations for the projects table.
- Implement database operations for project_members (inserting new members, removing members).
- Develop logic to filter tasks by project_id.
- Implement a search/selection mechanism for inviting users (e.g., by username or email).
- Define and enforce basic project roles/permissions (e.g., only owner can delete project, members can manage tasks).

#### Feature 4: Efficient Task Filtering & Sorting

**As a "CheckMate" user,** I want to easily filter and sort tasks by various criteria (e.g., due date, priority, status, assigned user, project) so that I can quickly find and prioritise relevant tasks.

**Acceptance Criteria:**

- A set of filter options is available (e.g., dropdowns, checkboxes) for:
  - Task status (To Do, In Progress, Completed, Blocked).
  - Task priority (High, Medium, Low).
  - Assigned user (if applicable).
  - Associated project.
- Users can sort tasks by due date (ascending/descending), priority, or creation date.
- Applying filters or sorting immediately updates the displayed task list without a full page reload.
- Multiple filters can be applied simultaneously.

**Tasks:**

- Implement backend Flask routes that accept query parameters for filtering and sorting.
- Modify database queries to apply WHERE clauses for filters and ORDER BY clauses for sorting based on user input.
- Develop frontend JavaScript to capture user selections from filter/sort controls.
- Implement AJAX calls to the backend to fetch filtered/sorted data.
- Update the HTML DOM dynamically with the new task list.
- Implement CSS to visually indicate active filters.
