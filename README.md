# FastAPI Base

A robust FastAPI application template with authentication, database integration, and CRUD operations for a book management system.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy ORM**: Database abstraction layer with PostgreSQL support
- **JWT Authentication**: Secure token-based authentication system
- **Pydantic Models**: Data validation and serialization
- **Docker Support**: Containerized application with Docker Compose
- **CORS Middleware**: Cross-origin resource sharing support
- **Database Migrations**: Alembic for database schema management
- **Voting System**: User voting functionality for books
- **Health Check Endpoint**: Application health monitoring

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL
- Docker & Docker Compose (optional)

## 🛠️ Installation

### Option 1: Local Development

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd FastAPI_Base
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   cd server
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the `server` directory:

   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

   Generate a secret key:

   ```bash
   openssl rand -hex 32
   ```

5. **Set up PostgreSQL database**

   - Create a PostgreSQL database
   - Update the `DATABASE_URL` in your `.env` file

6. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

### Option 2: Docker Deployment

1. **Navigate to the server directory**

   ```bash
   cd server
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

The application will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:

- **Interactive API Documentation**: `http://localhost:8000/docs`
- **Alternative API Documentation**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

## 🗄️ Database Models

### User Model

- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password`: Hashed password
- `created_at`: Timestamp

### Book Model

- `id`: Primary key
- `title`: Book title
- `author`: Book author
- `price`: Book price
- `owner_id`: Foreign key to User
- `created_at`: Timestamp

### Vote Model

- `user_id`: Foreign key to User (composite primary key)
- `book_id`: Foreign key to Book (composite primary key)

## 🔐 Authentication

The application uses JWT (JSON Web Tokens) for authentication:

1. **Register**: Create a new user account
2. **Login**: Authenticate and receive access token
3. **Protected Routes**: Use the access token in the Authorization header

### Example Authentication Flow

```bash
# Register a new user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com", "password": "password123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "password123"}'

# Use the returned access token for authenticated requests
curl -X GET "http://localhost:8000/books/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📖 API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user

### Users

- `GET /users/` - Get all users (admin only)
- `GET /users/{user_id}` - Get specific user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Books

- `GET /books/` - Get all books
- `GET /books/{book_id}` - Get specific book
- `POST /books/` - Create new book (authenticated)
- `PUT /books/{book_id}` - Update book (owner only)
- `DELETE /books/{book_id}` - Delete book (owner only)

### Votes

- `POST /votes/` - Vote on a book (authenticated)
- `GET /books/{book_id}/votes` - Get votes for a book

## 🏗️ Project Structure

```
FastAPI_Base/
├── server/
│   ├── main.py              # FastAPI application entry point
│   ├── db.py                # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── settings.py          # Application settings
│   ├── deps.py              # Dependency injection
│   ├── oath2.py             # OAuth2 password bearer
│   ├── utils.py             # Utility functions
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   ├── docker-compose.yml   # Docker Compose setup
│   └── routes/
│       ├── auth.py          # Authentication routes
│       ├── books_crud.py    # Book CRUD operations
│       ├── users_crud.py    # User CRUD operations
│       └── votes.py         # Voting routes
└── .venv/                   # Virtual environment
```

## 🔧 Configuration

### Environment Variables

| Variable                      | Description                  | Default  |
| ----------------------------- | ---------------------------- | -------- |
| `DATABASE_URL`                | PostgreSQL connection string | Required |
| `SECRET_KEY`                  | JWT secret key               | Required |
| `ALGORITHM`                   | JWT algorithm                | `HS256`  |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time        | `30`     |

### Database Configuration

The application uses PostgreSQL with the following default settings:

- **Host**: `localhost` (or `db` in Docker)
- **Port**: `5432`
- **Database**: `mydatabase`
- **Username**: `user`
- **Password**: `password`

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use secure environment variables in production
2. **Database**: Use a managed PostgreSQL service
3. **HTTPS**: Configure SSL/TLS certificates
4. **CORS**: Update CORS settings for production domains
5. **Logging**: Implement proper logging configuration
6. **Monitoring**: Add health checks and monitoring

### Docker Production Build

```bash
# Build production image
docker build -t fastapi-base:production .

# Run with production settings
docker run -p 8000:8000 \
  -e DATABASE_URL=your-production-db-url \
  -e SECRET_KEY=your-production-secret \
  fastapi-base:production
```
