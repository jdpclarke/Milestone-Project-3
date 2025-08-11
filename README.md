# CheckMate - Milestone Project 3

**A comprehensive web platform providing user-friendly task and project management for individuals, designed to streamline workflows and achieve goals.**

![Responsive Mockup (TBC Placeholder)](assets/readme/mockup.png)

## 1. Overview

Are you struggling to keep track of multiple projects, countless tasks, and critical deadlines? "CheckMate" is a powerful and intuitive Task Management System designed to help individuals organise their work, streamline their workflows, and achieve their goals with strategic clarity. Inspired by the precision and planning of chess, CheckMate empowers users to move their tasks from "To Do" to "Completed" with confidence.

Navigating the complexities of modern workloads, whether personal or professional, often leads to disorganisation, missed deadlines, and a feeling of being overwhelmed. CheckMate is built to cut through this chaos, providing a centralised, straightforward solution for managing all aspects of task and project execution. This intelligent online tool empowers users to effortlessly create, assign, track, and complete tasks within a structured project environment, ensuring nothing falls through the cracks.

If you're an individual aiming to master your daily to-do list or a student juggling assignments, CheckMate offers a user-friendly platform to gain control over your work, fostering efficiency, accountability, and the ultimate satisfaction of a job well done.

## 2. Rationale

CheckMate is an online tool developed to provide a comprehensive and efficient means of managing tasks and projects. Its primary objective is to simplify workflow organisation, enhance productivity, and ensure successful completion of objectives for both individuals and collaborative teams.

The inspiration for CheckMate arose from observing the widespread challenge of effective task management. Many individuals and organisations struggle with scattered notes, forgotten deadlines, and unclear responsibilities, leading to inefficiencies, stress, and unfulfilled potential. This project aims to address these common pain points by offering a structured, intuitive, and readily accessible solution.

In today's fast-paced environment, the ability to effectively plan, execute, and monitor tasks is paramount. Whether it's daily chores, academic assignments, or complex professional endeavours, a robust system is crucial for success. However, existing solutions can often be overly complex, lack specific features, or fail to provide the clear oversight needed to bring tasks to their ultimate "checkmate."

The core problem that CheckMate seeks to resolve is the pervasive inefficiency and disorganisation associated with managing multiple tasks and projects without a centralised, coherent system. This can lead to wasted time, duplicated efforts, missed opportunities, and a general lack of clarity on progress.

CheckMate offers a user-friendly online platform where users can create projects, define tasks within those projects, set priorities and due dates, and track progress through various statuses. The tool will provide intuitive interfaces for task and project creation, modification (CRUD functionality), and dynamic filtering/sorting options to quickly find relevant information. Key features include secure user authentication, distinct project workspaces, and clear visual feedback on task status. This approach provides a strategic and accessible alternative to fragmented planning methods.

CheckMate offers several advantages over current, less integrated methods. It provides significant time-saving through centralised management and streamlined workflows. The structured approach reduces the risk of missed deadlines and forgotten tasks, ensuring greater reliability and accountability. Furthermore, the clear and accessible interface empowers users to better understand their workload and focus on what truly matters.

The initial scope of CheckMate focuses on providing core task and project management functionalities: user authentication, project creation/management, task CRUD operations (create, read, update, delete), due dates, priorities, status tracking, and basic filtering/sorting. Acknowledged limitations include the initial focus on fundamental features before expanding to more advanced collaboration tools or integrations. Potential future enhancements for CheckMate include collaboration with others, advanced reporting and analytics, integration with calendars or communication platforms, recurring tasks, sub-tasks, file attachments, and more granular notification settings for deadlines or changes.

In summary, CheckMate addresses a significant need by providing a user-friendly and accurate solution for managing tasks and projects. By simplifying this process, the tool has the potential to save time, reduce errors, improve focus, and ultimately contribute to the more efficient execution and successful completion of individual endeavours.

## 3. User Experience (UX)

### User Stories

#### Feature 1: Secure User Authentication & Profile Management

**As a "CheckMate" user,** I want to securely register an account, log in, and manage my profile details so that I can access my personalised tasks and projects and maintain my personal information.

**Acceptance Criteria:**

- A registration form is present, requiring a unique username, email, and password (with confirmation).
- Passwords are securely hashed and stored (not plain text).
- Users can log in using their username and password.
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

- Users can create new tasks, specifying a title, description, due date priority.
- All tasks are displayed in a clear, organised list or board view.
- Each task entry clearly shows its title, description, due date, priority, and current status.
- Users can click on a task to view its full details in a dedicated view or modal.
- Users can edit any field of an existing task.
- Users can change a task's status (e.g., 'To Do', 'In Progress', 'Completed').
- Users can delete tasks, with a confirmation prompt to prevent accidental deletion.

**Tasks:**

- Develop Flask routes and corresponding HTML templates for:
  - Displaying all tasks (e.g., /tasks or main dashboard).
  - Creating a new task (e.g., /tasks/new).
  - Viewing a single task (e.g., /tasks/\<id>).
  - Editing an existing task (e.g., /tasks/\<id>/edit).
  - Deleting a task (e.g., /tasks/\<id>/delete).
- Implement database CRUD operations for the tasks table.
- Create form handling for task creation and editing.

#### Feature 3: Project Organisation

**As a "CheckMate" user,** I want to create and manage projects, assign tasks within them, so that I can organise larger initiatives.

**Acceptance Criteria:**

- Users can create new projects with a name and description.
- Users can view a list of all projects they own.
- Each project view displays the tasks associated with it.
- Project owners can view and interact with tasks within that project.

**Tasks:**

- Develop Flask routes and templates for:
- Creating new projects (e.g., /projects/new).
- Listing projects (e.g., /projects).
- Viewing a single project and its tasks (e.g., /projects/\<id>).
- Implement database CRUD operations for the projects table.
- Develop logic to filter tasks by project_id.

#### Feature 4: Efficient Task Filtering & Sorting

**As a "CheckMate" user,** I want to easily sort tasks by various criteria (e.g., due date, priority, created) so that I can quickly find and prioritise relevant tasks. I want these to be separated by To-Do, In Progress and Completed to show progress.

**Acceptance Criteria:**

- A set of filter options is available (e.g., dropdowns, checkboxes, buttons) for:
  - Task status (To Do, In Progress, Completed).
  - Task priority (High, Medium, Low).
- Users can sort tasks by due date (ascending/descending), priority, or creation date.
- Applying filters or sorting immediately updates the displayed task list without a full page reload.

**Tasks:**

- Implement backend Flask routes that accept query parameters for filtering and sorting.
- Modify database queries to apply WHERE clauses for filters and ORDER BY clauses for sorting based on user input.
- Implement AJAX calls to the backend to fetch filtered/sorted data.
- Update the HTML DOM dynamically with the new task list.
- Implement CSS to visually indicate active filters.

### Design

- **Colour Scheme**

  As the project, CheckMate, is inspired by the strategic nature of chess and aims for clarity in task management, the colour scheme has been chosen to reflect a professional, clean, and organised aesthetic. We will primarily use a muted palette of dark greys and whites, reminiscent of a classic chessboard, with a subtle accent colour to highlight interactive elements and important information whilst providing a clear, indicative function.

  ![Colour palette for this project](assets/readme/colour-palette.png)

- **Typography**

  To complement the theme of strategic clarity and professionalism, two distinct yet complementary Google Font families have been selected for CheckMate:

  The ["Inter"](https://fonts.google.com/specimen/Inter) font family has been selected as the main font used throughout the whole project, with a generic sans-serif as the fallback font in any case that the font isn't being imported into the project correctly. Inter is a variable font designed specifically for user interfaces, ensuring high legibility and clarity on all screen sizes. Its clean lines and robust character set make it ideal for detailed task lists and extensive project descriptions. The variable nature of Inter also allows for precise control over its weight and other properties, ensuring optimal readability across different contexts within the application.

  The ["Roboto Slab"](https://fonts.google.com/specimen/Roboto+Slab) font family has been selected as the heading element font. Roboto Slab is a static font, providing a strong, geometric, and structured feel that perfectly aligns with the organised nature of CheckMate. Its distinct slab serifs give headings a clear presence and gravitas without being overly decorative, reinforcing the sense of precision and strategic planning inherent in the application's purpose. This contrast between the clean sans-serif body and the robust slab-serif headings contributes to a professional and easy-to-navigate user experience.

### Imagery

This website utilises a variety of images to enhance the user experience and convey information effectively. The images serve several purposes:

- **Branding:** The logo (`assets/images/logo.png`, `assets/images/logo-with-text.png`) is used in places like the navigation bar and at login/registration to reinforce brand identity and provide a consistent visual element throughout the site.

- **Favicon:** A favicon (`assets/favicon/apple-icon.png`, `assets/favicon/favicon-32x32.png`, `assets/favicon/favicon-16x16.png`) is included to provide a visual cue for the website in browser tabs and bookmarks. This also provides a first look in to the brand of the website.

All images used on the website are optimised for web performance to ensure fast loading times and a smooth user experience. Alternative text (alt text) is provided for all images to ensure accessibility for users with visual impairments and to improve SEO. The alt text descriptions are concise and descriptive, accurately conveying the content and purpose of each image.

### Wireframes

## 3. Features

- **Secure User Authentication and Profile Management:**
  - Provides secure registration and login functionalities, allowing users personalised access to their tasks and projects.
  - Enables users to manage their profile details, including first name, last name, and email.
  - Facilitates secure password changes to maintain account integrity.

- **Comprehensive Task Organisation and Tracking:**
  - Allows users to create, view, edit, and delete tasks with details such as title, description, due date, priority, and associated project.
  - Enables users to update the status of tasks (e.g., 'To Do', 'In Progress', 'Completed') for clear progress tracking.
  - Provides visual indicators for task status and completion, making it easy to see progress at a glance.

- **Efficient Task Filtering and Prioritisation:**
  - Offers dynamic layout to filter projects in to their statuses.
  - Includes sorting capabilities to organise tasks by due date, priority, or creation date for efficient prioritisation.
  - Ensures immediate and dynamic updates to the displayed task list upon applying sorting.

- **Intuitive User Interface and Feedback:**
  - Implements clear and immediate validation for all input fields, providing consolidated alerts for missing mandatory information or invalid data.
  - Presents a clean, well-organised layout for all task and project information, enhancing usability.

- **Responsive and Accessible Design:**
  - The application layout seamlessly adjusts to various screen sizes aWnd orientations, guaranteeing optimal usability across desktops, laptops, tablets, and mobile phones.
  - All interactive elements and content displays are designed to be functionally accessible and clearly visible on diverse devices.
  - Adheres to standard web development practices to ensure basic accessibility (e.g., clear labels, sufficient colour contrast, keyboard navigability for interactive components).
  - Maintains a clear separation of HTML structure, CSS styling, and Python logic in distinct files for improved maintainability and organisation.

## 4. Technology Used

CheckMate, a comprehensive web platform for personal project and task management, was developed using a full-stack approach with a focus on efficiency, security, and a user-friendly interface. The application’s structure leverages a blend of backend frameworks and frontend libraries to deliver a seamless user experience.

- **Python & Flask:** The application's backend is built on Python using the Flask micro-framework. Flask is responsible for all server-side logic, including handling HTTP requests, routing to the correct pages, processing form data, and managing the application's core business logic for projects and tasks.

- **Flask-Login:** This Flask extension provides robust user session management. It handles user authentication, including logging in, logging out, and protecting specific routes to ensure only authenticated users can access them.

- **SQLAlchemy & Flask-SQLAlchemy:** All persistent data—including user profiles, projects, and tasks—is stored in a PostgreSQL relational database. SQLAlchemy serves as the Object-Relational Mapper (ORM), allowing the application to interact with the database using Python objects instead of raw SQL. Flask-SQLAlchemy integrates this ORM into the Flask application seamlessly.

- **Werkzeug:** As the underlying library for Flask, Werkzeug handles crucial utilities like password hashing to ensure passwords are not stored in plain text.

- **psycopg2-binary:** This is the PostgreSQL database adapter that allows the Python backend to connect to and communicate with the database.

- **python-dotenv:** This library is used for managing environment variables. It loads configuration values, such as the database URI and secret key, from a file, which is a standard practice for separating configuration from code and enhancing security.

- **Jinja:** The application's frontend templates are rendered using the Jinja templating engine. Jinja allows for the dynamic generation of HTML content by inserting data from the Python backend, enabling user-specific pages and content.

- **HTML5:** HTML5 is the foundational markup language used to structure the application's web pages. Semantic HTML elements are employed to create a logical, accessible, and maintainable document structure.

- **CSS3:** CSS3 is used for all custom styling, including defining the application's color palette, typography, and specific visual design elements.

- **Bootstrap 5:** The entire frontend is built on the Bootstrap 5 framework. This provides a responsive, mobile-first design, ensuring that the application's layout, components, and usability remain consistent across various device sizes and screen orientations.

- **Font Awesome:** Font Awesome icons are integrated throughout the user interface to improve visual clarity and user experience. Icons are used on buttons and in navigation to provide intuitive visual cues for different actions and content.

- **Heroku:** The application is configured for deployment on the Heroku cloud platform.

- **Gunicorn:** Gunicorn is specified as the production-ready WSGI HTTP Server. It is responsible for running the Flask application in a robust, multi-process environment.

- **requirements.txt:** This file lists all the Python dependencies required for the application to run. When deployed, this file is used to automatically install the necessary libraries, ensuring the production environment matches the development environment.

- **CDN (Content Delivery Network):** External libraries, such as Bootstrap's CSS, are loaded from a CDN. This optimises loading times by utilizing geographically distributed servers to deliver content efficiently.

## 5. Installation

To set up and run the CheckMate application locally, follow these steps.

### PreRequisites

You will need the following installed on your sysem:

- Git
- Python 3.8+
- pip (Python's package installer)
- PostgreSQL (with a user and a database created)

### Steps

1. **Clone the Repository**
    - Open your terminal or command prompt.
    - Navigate to the directory where you want to store the project.
    - Execute the following command:

        ```bash
        git clone https://github.com/jdpclarke/Milestone-Project-3.git
        ```

2. **Navigate to the Project Directory:**
    - Use the `cd` (change directory) command to enter the cloned project folder:

        ```bash
        cd Milestone-Project-3
        ```

3. **Set up a Virtual Environment**
    - It is highly recommended to use a virtual environment to manage project dependencies. This isolates the project's packages from your system's global Python installation.

        ```bash
        # Create a virtual environment
        python3 -m venv venv

        # Activate the virtual environment
        # On macOS and Linux:
        source venv/bin/activate
        # On Windows:
        venv\Scripts\activate
        ```

4. **Install Dependencies**
    - With your virtual environment activated, install all the required Python packages from the `requirements.txt` file.

        ```bash
        pip install -r requirements.txt
        ```

5. **Configure the Database**
    - Create a PostgreSQL database and a user for the application.
    - Create a new file named `.env` in the root directory of the project.
    - Add the following lines to your `.env` file, replacing the placeholder values with your own database credentials and a secure secret key:

        ```bash
        DATABASE_URL=postgresql://user:password@localhost:5432/dbname
        SECRET_KEY=your_secure_secret_key_here
        ```

    - Initialize the database tables by running the `db_init.py` script. This will create all the necessary tables for the `User`, `Project`, and `Task` models.

        ```bash
        python3 db_init.py
        ```

6. **Run the Application**
    - Now you can start the Flask development server.

        ```bash
        python3 app.py
        ```

    - The application should now be running. Open your web browser and navigate to `http://127.0.0.1:5000` to view the website.

**Note:**

- CheckMate is a dynamic web application and requires the development server to be running to function. You cannot open the HTML files directly in your browser.
- To stop the server, press Ctrl + C in your terminal.
- The .env file is crucial for storing your database credentials and secret key securely. Do not commit this file to your public repository.
- If you make changes to the database models (models.py), you will need to re-run python3 db_init.py to update your database schema.

## 6. Usage

CheckMate is a straightforward project management tool designed to help you organize your personal projects and tasks. This guide will walk you through the key features and how to use them effectively.

**1. Getting Started, (Registration & Login):**

- **Register:** If you are a new user, click the "Register" button on the home page. Fill out the form with your personal details, a unique username, and a password to create your account.
- **Login:** If you already have an account, click "Login". Enter your username and password to access your dashboard.

**2. Managing Projects:**

The dashboard is the central hub for all your projects.

- **View Projects:** Upon logging in, you will see a list of all your existing projects, each displayed in its own card. Each card shows the project name, description, and creation date.
- **Add a New Project:** Click the "Add New Project" button on the dashboard. You will be taken to a form where you can enter a name and a description for your new project. Click "Add Project" to save it.
- **View Project Details:** Click the "View Details" button on any project card to see a list of all the tasks associated with that specific project.
- **Edit a Project:** From the project details page, click "Edit Project" to change the project's name or description.
- **Delete a Project:** From the project details page, click "Delete Project" to permanently remove the project and all of its associated tasks. A confirmation dialog will appear to prevent accidental deletion.

**3. Managing Tasks:**

Tasks are the individual to-do items within a project.

- **View Projects:** Upon logging in, you will see a list of all your existing projects, each displayed in its own card. Each card shows the project name, description, and creation date.
- **Add a New Project:** Click the "Add New Project" button on the dashboard. You will be taken to a form where you can enter a name and a description for your new project. Click "Add Project" to save it.
- **View Project Details:** Click the "View Details" button on any project card to see a list of all the tasks associated with that specific project.
- **Edit a Project:** From the project details page, click "Edit Project" to change the project's name or description.
- **Delete a Project:** From the project details page, click "Delete Project" to permanently remove the project and all of its associated tasks. A confirmation dialog will appear to prevent accidental deletion.

**4. Editing Your Profile:**

You can manage your personal information from your profile page.

- **Access Profile:** Click your username in the navigation bar to go to your profile.
- **Edit Profile:** On the profile page, click "Edit Profile" to update your first name, last name, username, or email address.
- **Change Password:** On the profile page, click "Change Password" to update your account password. You will need to enter your current password before setting a new one.

## 7. Testing

**1. Comprehensive Manual Testing:**

The CheckMate application was thoroughly tested across a variety of browsers and devices to ensure functionality, responsiveness, and accurate data handling for user authentication and project management.

**Browsers and Devices Tested:**

- **Chrome (Version 140.0.7339.5 (Official Build) (64-bit)):** Used as the primary testing browser.
- **Chrome Developer Tools:** Employed to simulate various screen sizes and mobile devices, including:
  - Common mobile device resolutions (e.g., iPhone, Android).
  - Tablet screen sizes.
  - Various desktop viewport widths.

**Testing Conducted:**

- **User Authentication & Profile Management Testing:**
  - Valid Data Inputs: Tested registration, login, and profile editing with valid user data.
  - Edge Cases for Credentials: Tested login with incorrect passwords and non-existent usernames.
  - Validation Errors: Confirmed that registration and profile editing correctly prevent the use of duplicate usernames and email addresses.
  - Session Management: Verified that logging out correctly ends the user session and redirects to the home page.
  - Password Changes: Tested the password change functionality, ensuring the user must provide the correct current password and that the new password and confirmation match.

- **Project Management Testing:**
  - Create & View: Confirmed that new projects can be added from the dashboard and are displayed correctly.
  - Project Details: Verified that navigating to a project's details page displays the correct information and lists its tasks.
  - Edit & Delete: Ensured that projects can be edited and deleted, and that the deletion process includes a confirmation prompt.

- **Task Management Testing:**
  - Create Task: Confirmed that new tasks can be added to a project with all details (title, description, due date, status, priority) successfully saved.
  - Edit & Delete: Verified that tasks can be edited and deleted individually from the project details page, each with a confirmation prompt.
  - Data Integrity: Checked that deleting a project correctly removes all associated tasks.

- **Responsiveness & Layout Testing:**
  - Viewport Adaptation: Tested the application's layout across various screen sizes using Chrome Developer Tools, ensuring elements rearrange and resize gracefully.
  - Readability on Mobile: Verified that all text and form inputs remain readable and usable on smaller screens without excessive scrolling or truncation.
  - Button Accessibility: Ensured all buttons and interactive elements are visible and easily tappable on all device sizes.
  - Navigation Menu: Confirmed the navigation bar collapses into a hamburger menu on smaller screens and functions correctly.

- **Accessibility Testing:**
  - Keyboard Navigation: Mapped the precise focus order of all interactive elements using the Tab key, ensuring a logical and intuitive sequence throughout the application.
  - Labels and Descriptions: Confirmed all form input fields have clear and descriptive labels (`<label>` tags), which is essential for screen reader users.

**Bug Evaluation and Fixes:**

- **Bug 1: Incorrect Delete Confirmation:**
  - Description: The delete buttons for projects and tasks used a JavaScript `confirm()` dialog.
  - Fix: Acknowledged the use of `confirm()` in the current code but noted that a custom modal dialog would provide a better user experience and should be considered for a future update. The current functionality was verified to work correctly.

- **Bug 2: Missing Due Date for Tasks:**
  - Description: If a task was created without a due date, the p`roject_details.html` template would encounter an error when trying to display it.
  - Fix: Added a conditional check (`if task.due_date else 'N/A'`) in the `project_details.html` template to gracefully handle and display `N/A` for tasks without a due date.

**Unfixed Bugs:**

At the present time, all found bugs have been fixed.

**Screenshots and User Story Fulfillment:**

- **Screenshot 1: Dashboard with Projects**
  [Screenshot of the CheckMate dashboard showing multiple project cards](assets/readme/usf-1.png)
  - **User Story Fulfilled:** "As a user, I want to see an overview of all my projects so I can easily choose which one to work on."
  - **Explanation:** This screenshot highlights the main dashboard, showcasing the user-friendly interface with project cards that provide a quick overview of all ongoing projects. It demonstrates how users can easily get started with their work.

- **Screenshot 2: Project Details with Tasks**
  [Screenshot of a project's details page, displaying the project description and a list of its tasks](assets/readme/usf-2.png)
  - **User Story Fulfilled:** "As a user, I want to view all the tasks for a specific project so I can track my progress and see what needs to be done."
  - **Explanation:** This screenshot shows the project details view, which organises and displays all tasks belonging to a single project. It clearly shows the task's title, priority, and due date, fulfilling the need for detailed progress tracking.

- **Screenshot 3: Add New Task Form**
  [Screenshot of the form to add a new task to a project](assets/readme/usf-3.png)
  - **User Story Fulfilled:** "As a user, I want to easily add new tasks to a project so I can detail the work that needs to be done."
  - **Explanation:** This screenshot illustrates the dedicated form for creating a new task, with all the necessary fields for a title, description, due date, status, and priority.

- **Screenshot 4: User Profile Page**
  [Screenshot of the User Profile page displaying personal details and action buttons](assets/readme/usf-4.png)
  - **User Story Fulfilled:** "As a user, I want to view and manage my personal information so I can keep my profile up to date."
  - **Explanation:** This screenshot shows the user's personal profile page, which displays their account information and provides prominent buttons to edit their profile details or change their password, giving them full control over their account.

- **Screenshot 5: Delete Confirmation**
  [Screenshot showing a browser's `confirm()` dialog when a user attempts to delete a project](assets/readme/usf-5.png)
  - **User Story Fulfilled:** "As a user, I want to be prompted for confirmation before deleting a project or task to prevent accidental data loss."
  - **Explanation:** This screenshot captures the confirmation dialog that appears when a user clicks the delete button, proving that the application has a safeguard in place to prevent accidental deletion of important data.

**2. Automated Testing:**

- **HTML and CSS Validation (W3C):**
  - To properly validate the HTML generated by Flask templates, the final rendered HTML from the browser must be used, as the W3C Markup Validation Service cannot process the Jinja2 template syntax directly. The process involves running the application, viewing the page source in a browser, and then pasting the generated code into the [W3C Markup Validation Service](https://validator.w3.org/). The CSS file can be validated directly using the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/).

  - The validation process ensures that the final code delivered to the user's browser is compliant with web standards and is free from syntax errors. Any identified errors were corrected to improve the tool's overall quality and consistency.

  - W3C Markup Validation highlights info messages relating to "Trailing slash on void elements has no effect and interacts badly with unquoted attribute values." These often occur due to auto-formatters; attempts to remove them may result in the formatter re-introducing them.

  - W3C CSS Validation highlights background-color and border-color warning for the .btn-primary CSS class. This is an intentional design choice to create a simple, unified look for the primary action buttons. The border is explicitly set to match the background color, and this warning can be safely ignored.

- **Performance, Best Practices, and SEO Testing (Lighthouse):** [Lighthouse Testing Results](assets/readme/lighthouse-results.pdf)
  - Lighthouse, within the Chrome Developer Tools, was used to evaluate the CheckMates's performance, best practices, and SEO. This testing provided insights into areas for optimization, such as script optimization and page load speed. The results of the Lighthouse testing would be used to make targeted improvements to the tool's performance and search engine visibility. While the mobile analysis typically provides a strong score, the desktop version highlights opportunities for further enhancement.

  - **Lighthouse Performance Analysis:**

    A Lighthouse audit was conducted, revealing a strong performance score of 98 and excellent Accessbility, Best Practices and SEO all at 100.

    Lighthouse suggested:
    - Preconnect to required origins
    - Serving images in next-gen formats.
    - Properly sizing and efficiently encoding images.
    - Eliminating render-blocking resources.

    These optimisations would enhance performance and improve user experience.
  
  - **Overall:**

      CheckMate performs well across automated audits, achieving strong scores in performance, accessibility, best practices, and SEO. The application is fast and responsive with excellent FCP, TBT, and CLS scores. Optimising image assets and managing render-blocking resources could further enhance the user experience and load times. Addressing these areas will ensure CheckMate continues to provide a high-quality, performant, and reliable service.

## 8. Deployment

This project was deployed using the Heroku platform, a Platform as a Service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

**Heroku Deployment:**

To deploy this project to Heroku, the following steps were taken:

1. **Create a Heroku Account and App:** A new account was created on `https://www.heroku.com`, and a new app was created through the dashboard.
2. **Install Heroku CLI:** The Heroku Command Line Interface (CLI) was installed to enable interaction with Heroku from the terminal.
3. **Log in to Heroku CLI:** The command `heroku login` was used to authenticate the CLI with the Heroku account.
4. **Link the Heroku App to the Local Repository:** The local Git repository was linked to the Heroku app using `heroku git:remote -a your-app-name`.
5. **Create a Procfile:** A `Procfile` was created in the root directory to tell Heroku how to run the web application. The file contains the line web: `gunicorn --bind 0.0.0.0:$PORT app:app`.
6. **Set Environment Variables:** The `SECRET_KEY` and `DATABASE_URL` environment variables were set in Heroku's config vars.
7. **Push to Heroku:** The code was deployed by pushing the `main` branch to Heroku using `git push heroku main`.
8. **Initialise the Database:** After deployment, the database was initialized by running `heroku run python db_init.py` to create the necessary tables.

**GitHub Pages Deployment:**

The project was deployed to GitHub Pages using the following steps:

1. **Log in to GitHub and locate the GitHub Repository:** Navigate to the project's repository on GitHub: [https://github.com/jdpclarke/Milestone-Project-3.git](https://github.com/jdpclarke/Milestone-Project-3.git)
2. **Access Repository Settings:** At the top of the repository (not the top of the page), locate the "Settings" button on the menu.
3. **Navigate to GitHub Pages Section:** Scroll down the Settings page until you find the "Pages" section.
4. **Select Deployment Branch:** Under "Source," click the dropdown menu and select the branch you wish to deploy (usually "main" or "master").
5. **GitHub Pages Deployment:** The page will automatically refresh, and GitHub Pages will deploy the site from the selected branch.
6. **Access the Deployed Site:** Scroll back down the page to the "Pages" section to find the published site link.

**Forking the GitHub Repository:**

To create a copy of this repository on your own GitHub account, allowing you to view and modify the code without affecting the original, follow these steps:

1. **Log in to GitHub and locate the GitHub Repository:** Navigate to the project's repository on GitHub: [https://github.com/jdpclarke/Milestone-Project-3.git](https://github.com/jdpclarke/Milestone-Project-3.git)
2. **Fork the Repository:** At the top of the repository (not the top of the page), just above the "Settings" button, locate the "Fork" button and click it.
3. **Your Forked Copy:** You will now have a copy of the original repository in your GitHub account.

**Making a Local Clone:**

To download a local copy of this repository to your computer, follow these steps:

1. **Log in to GitHub and locate the GitHub Repository:** Navigate to the project's repository on GitHub: [https://github.com/jdpclarke/Milestone-Project-3.git](https://github.com/jdpclarke/Milestone-Project-3.git)
2. **Clone or Download:** Under the repository name, click "Code."
3. **Copy HTTPS Link:** Under "Clone with HTTPS," copy the provided link.
4. **Open Git Bash (or your terminal):** Open your Git Bash terminal (or your preferred terminal).
5. **Change Directory:** Change the current working directory to the location where you want the cloned directory to be created using the `cd` command.
6. **Clone the Repository:** Type `git clone` and then paste the URL you copied in Step 3. Press Enter.

    ```bash
    git clone [https://github.com/jdpclarke/Milestone-Project-3.git](https://github.com/jdpclarke/Milestone-Project-3.git)
    ```

7. **Local Clone Created:** Your local clone will be created in the specified directory.

## 9. Credits

This CheckMate project was developed using a combination of publicly available resources, open-source libraries, and original content. Here is a more detailed breakdown of the credits:

**Technologies and Libraries:**

- Flask: The backend web framework for handling routing, requests, and templates.
- Flask-SQLAlchemy: An ORM (Object-Relational Mapper) used to interact with the PostgreSQL database.
- Flask-Login: Provides user session management, authentication, and login protection for routes.
- Werkzeug: A WSGI utility library used by Flask for security, including password hashing.
- Bootstrap 5: The front-end framework for responsive design and UI components.
- Font Awesome: Provides the icons used throughout the application.
- Gunicorn: A Python WSGI HTTP server used for deploying the application on Heroku.
- psycopg2-binary: A PostgreSQL database adapter for Python.
- python-dotenv: Used to manage environment variables for local development.

**Assets:**

- Logo: The CheckMate logo was created using an online logo maker.
- Favicons: Favicons were generated using an online favicon generator.

**Acknowledgements:**

- Code Institute: The developer acknowledges the support and guidance provided by Code Institute throughout the project's development.
- Community: The developer acknowledges the contributions of the open-source community for providing the tools, libraries, and resources used in this project.

## 10. Future Improvements

CheckMate is a foundational tool, and several enhancements can be implemented to further improve its functionality and user experience.

1. **Kanban Board View:** Implement a drag-and-drop Kanban board view on the dashboard and project details page to provide a more intuitive and visual way to manage tasks.
2. **User Collaboration:** Add the ability for users to share projects with other registered users, allowing for real-time collaboration.
3. **Task Management Features:** Add more advanced task features such as sub-tasks, comments, and file attachments.
4. **Notifications:** Implement a notification system to alert users of upcoming deadlines or task updates.
5. **Enhanced Profile:** Add more user profile features, such as a profile picture and the ability to customize dashboard layouts.
6. **API Integration:** Create an API to allow CheckMate to integrate with other third-party services.
