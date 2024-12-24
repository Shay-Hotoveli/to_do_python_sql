# Todo-Flask-MYSQL

## Project Description

This is a simple TODO application built using Flask and a MySQL database. 
It allows users to sign up, log in, and manage their personal tasks. 
Logged-in users can create, edit, and delete tasks, as well as mark tasks as complete. 
The application also includes an admin panel with features for user management, task overview, and system administration.

## Installation

1. **Prerequisites:**
    * Python 3.x (https://www.python.org/downloads/)
    * pip (usually comes bundled with Python)
2. **Install dependencies:**
    ```bash
    pip install Flask flask-mysql mysql-connector-python werkzeug python-dotenv
    ```
3. **Create a `.env` file** (refer to the `.env.example` for guidance) and populate it with your MySQL credentials:
    ```
    MYSQL_HOST=your_host 
    MYSQL_USER=your_user
    MYSQL_PASSWORD=your_password
    MYSQL_DATABASE=your_database
    ```

## Usage

1. Clone this repository:
    ```bash
    git clone https://github.com/Shay-Hotoveli/to_do_python_sql.git
    ```
2. Navigate to the project directory:
    ```bash
    cd to_do_python_sql
    ```
3. Create the necessary database tables:
    * **users:** (user_id, username, password, email, gender, role)
    * **tasks:** (task_id, task_header, task_description, user_id, creation_time, finish_time, is_complete)
    * (Refer to the `sql/create_tables.sql` file for the exact schema)
4. Run the development server:
    ```bash
    python app.py
    ```
5. Access the app in your web browser at http://localhost:5000/

## Features

* User Registration and Login
* Task Creation, Editing, and Deletion
* Task Completion Tracking
* Admin Panel:
    * User Management (view, create, update, delete)
    * Task Overview (view all tasks, filter by user)
    * System Administration 

## Database Setup

* Create a MySQL database.
* Execute the `sql/create_tables.sql` script to create the necessary tables within the database.
* Configure your MySQL credentials in the `.env` file.

## Contributing

Currently, no formal contribution guidelines are defined. However, feel free to explore and experiment with the code.