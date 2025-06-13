# Todo Application

##Links 
 -http://159.223.28.82:3000/ front
 -http://159.223.28.82:8000/ back

A full-stack Todo application built with FastAPI, React, and PostgreSQL.

## Features

- User authentication with JWT
- Create, read, update, and delete tasks
- Secure API endpoints
- Docker and Docker Compose setup
- CI/CD with GitHub Actions

## Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.9+ (for local development)

## Getting Started

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Start the application using Docker Compose:

```bash
docker-compose up --build
```

The application will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Setup

### Backend

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the backend:

```bash
uvicorn backend.main:app --reload
```

### Frontend

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Run the frontend:

```bash
npm start
```

## API Endpoints

- POST `/api/register` - Register a new user
- POST `/api/token` - Login and get access token
- GET `/api/me` - Get current user info
- GET `/api/tasks` - Get all tasks for current user
- POST `/api/tasks` - Create a new task

## Environment Variables

Create a `.env` file in the root directory:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=todo_db
POSTGRES_HOST=localhost
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
