# Healthcare Backend API

A RESTful Healthcare Management Backend built using **Django, Django REST Framework, PostgreSQL, and JWT Authentication**.

This project provides APIs for user authentication, patient management, doctor management, and assigning doctors to patients. It includes authentication, authorization, input validation, and user-level data isolation.

## Features

- User registration and login.
- JWT-based authentication using SimpleJWT.
- Patient CRUD operations.
- Doctor CRUD operations.
- Assign doctors to patients.
- Retrieve doctors assigned to a particular patient.
- User-level patient ownership and access control.
- Duplicate patient-doctor assignment prevention.
- Input validation and error handling.
- Automated API testing.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend framework |
| Django REST Framework | REST API development |
| PostgreSQL | Relational database |
| SimpleJWT | JWT authentication |
| Psycopg | PostgreSQL database adapter |
| python-dotenv | Environment variable management |
| Django APITestCase | Automated API testing |

## Project Structure

```text
healthcare_backend/
│
├── accounts/
│   ├── tests/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── patients/
│   ├── tests/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── doctors/
│   ├── tests/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── mappings/
│   ├── tests/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── healthcare_backend/
│   ├── settings.py
│   └── urls.py
│
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Adityagupta-18/healthcare-backend-django
cd healthcare-backend
```

### 2. Create and activate a virtual environment

For Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named:

```text
healthcare_db
```

### 5. Configure environment variables

Create a `.env` file in the project root.

Example configuration:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your-postgresql-password
DB_HOST=localhost
DB_PORT=5432
```

Replace the placeholder values with your local configuration.

**Important:** Never commit your actual `.env` file or database credentials to GitHub.

### 6. Apply database migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser (optional)

```powershell
python manage.py createsuperuser
```

### 8. Start the development server

```powershell
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API Documentation

All API endpoints are prefixed with:

```text
/api/
```

### 1. Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Authenticate user and obtain JWT tokens |

**User Registration**

`POST /api/auth/register/`

Request body:

```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "Password@123"
}
```

**User Login**

`POST /api/auth/login/`

Request body:

```json
{
    "email": "john@example.com",
    "password": "Password@123"
}
```

The login response provides an access token and refresh token.

Use the access token for protected endpoints:

```http
Authorization: Bearer <access_token>
```

### 2. Patient Management APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List authenticated user's patients |
| GET | `/api/patients/<id>/` | Retrieve patient details |
| PUT | `/api/patients/<id>/` | Update patient |
| PATCH | `/api/patients/<id>/` | Partially update patient |
| DELETE | `/api/patients/<id>/` | Delete patient |

**Create Patient**

`POST /api/patients/`

Request body:

```json
{
    "name": "John Smith",
    "age": 30,
    "gender": "Male",
    "phone_number": "9876543210"
}
```

Patient ownership is automatically assigned to the authenticated user.

### 3. Doctor Management APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | Retrieve all doctors |
| GET | `/api/doctors/<id>/` | Retrieve doctor details |
| PUT | `/api/doctors/<id>/` | Update doctor |
| PATCH | `/api/doctors/<id>/` | Partially update doctor |
| DELETE | `/api/doctors/<id>/` | Delete doctor |

**Create Doctor**

`POST /api/doctors/`

Request body:

```json
{
    "name": "Dr. Sharma",
    "specialization": "Cardiology",
    "phone_number": "9876543210",
    "email": "doctor@example.com"
}
```

### 4. Patient–Doctor Mapping APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | Retrieve authenticated user's mappings |
| GET | `/api/mappings/<patient_id>/` | Retrieve doctors assigned to a patient |
| DELETE | `/api/mappings/<mapping_id>/` | Remove a patient-doctor mapping |

**Assign Doctor to Patient**

`POST /api/mappings/`

Request body:

```json
{
    "patient": 1,
    "doctor": 1
}
```

The mapping associates the selected patient with the selected doctor.

The API prevents duplicate assignments and verifies that the patient belongs to the authenticated user.

## Security and Authorization

The application implements the following security measures:

- JWT authentication for protected endpoints.
- Password hashing through Django's authentication system.
- Patient records are restricted to their respective owners.
- Users cannot retrieve, modify, or delete another user's patients.
- Users cannot assign doctors to another user's patients.
- Users cannot retrieve or delete another user's patient-doctor mappings.
- Doctor listing is available to authenticated users.
- Individual doctor operations follow creator-based access restrictions.
- Duplicate doctor assignments for the same patient are prevented through database constraints.

## Automated Testing

The project includes automated tests using Django's testing framework and Django REST Framework's `APITestCase`.

Tests cover:

- User registration and login.
- JWT authentication.
- Patient CRUD operations.
- Doctor CRUD operations.
- Patient-doctor mapping operations.
- Input validation and error handling.
- Authentication and authorization.
- User ownership and data isolation.
- Duplicate mapping prevention.

Run the complete test suite:

```powershell
python manage.py test -v 2
```

Run tests for an individual application:

```powershell
python manage.py test accounts -v 2
python manage.py test patients -v 2
python manage.py test doctors -v 2
python manage.py test mappings -v 2
```

## API Testing

The APIs can be tested using **Postman**.

For protected endpoints:

1. Register a user.
2. Log in to obtain the JWT access token.
3. Select Bearer Token in Postman's Authorization tab.
4. Enter the access token.
5. Send requests to the required API endpoints.

## License

This project was developed as part of a backend development assignment.
