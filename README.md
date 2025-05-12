# To-Do App (Flask + MySQL)

This is a simple To-Do web application built with Flask and MySQL.

## Features

- User registration and login
- Admin dashboard with user and task overview
- Create, update, delete tasks
- View completed and pending tasks

## Prerequisites

- Python 3.8+
- MySQL Server

## Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

2. **Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up the Database**

- Create a MySQL database.
- Run the SQL script in the `sql/create_tables.sql` file to create tables.

5. **Configure Environment Variables**

Create a `.env` file in the root directory and add your DB credentials:

```
DB_HOST=localhost
DB_USER=yourusername
DB_PASSWORD=yourpassword
DB_NAME=yourdatabasename
SECRET_KEY=your_secret_key
```

6. **Run the App**

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## Folder Structure

```
├── app/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── utils/
│   └── config.py
│   └──.env
├── tests/
├── sql/
│   └── create_tables.sql
├── .gitignore
├── requirements.txt
├── app.py
├── pytest.ini
└── README.md
```