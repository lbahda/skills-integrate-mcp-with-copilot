# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- View activity participants without logging in
- Register and unregister students as an authenticated teacher

## Getting Started

1. Install the dependencies from the repository root:

   ```
   pip install -r requirements.txt
   ```

2. Create a teacher account. The password must be at least 12 characters; only a salted hash is stored:

   ```
   cd src
   python create_teacher.py
   ```

   The generated `src/teachers.json` file is local and ignored by Git. Run the command again to add another account or update a password.

3. Start the application from `src/`:

   ```
   uvicorn app:app --reload
   ```

4. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

Teacher credentials are held in browser memory until logout or page reload. HTTP Basic authentication must be used over HTTPS when the app is deployed beyond local development.

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| GET    | `/auth/verify`                                                    | Verify teacher credentials                                          |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Register a student (teacher authentication required)                |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (teacher authentication required)           |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
