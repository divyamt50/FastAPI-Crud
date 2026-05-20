# FastAPI Blog API 🚀

A beginner-friendly blog API project built with FastAPI for learning modern Python backend development.

This project covers:

- FastAPI basics
- REST APIs
- Path & query parameters
- Pydantic models
- Request validation
- CRUD operations
- Dependency Injection
- SQLAlchemy ORM
- Authentication with JWT
- Database relationships
- Alembic migrations
- Async concepts
- API documentation

---

# 📚 Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Alembic
- SQLite / PostgreSQL
- JWT Authentication

---

# 📁 Project Structure

```bash
fastapi_blog/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── oauth2.py
│   ├── hashing.py
│   ├── token.py
│   ├── utils.py
│   │
│   ├── routers/
│   │   ├── post.py
│   │   ├── user.py
│   │   └── auth.py
│   │
│   └── repository/
│       ├── post.py
│       └── user.py
│
├── alembic/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/fastapi_blog.git
cd fastapi_blog
```

---

## 2. Create virtual environment

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Server

```bash
uvicorn app.main:app --reload
```

Server will start at:

```bash
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI automatically generates API docs.

## Swagger UI

```bash
http://127.0.0.1:8000/docs
```

## ReDoc

```bash
http://127.0.0.1:8000/redoc
```

---

# 🧠 Features

## ✅ User Authentication

- Register users
- Login users
- JWT Token Authentication
- Password hashing

---

## ✅ Blog Posts

- Create post
- Get all posts
- Get single post
- Update post
- Delete post

---

## ✅ Database

- SQLAlchemy ORM
- Relationships
- Alembic migrations

---

# 🧪 Example API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home route |
| POST | `/user` | Create user |
| POST | `/login` | Login user |
| GET | `/posts` | Get all posts |
| POST | `/posts` | Create post |
| GET | `/posts/{id}` | Get single post |
| PUT | `/posts/{id}` | Update post |
| DELETE | `/posts/{id}` | Delete post |

---

# 🔐 Authentication

This project uses JWT Authentication.

After login:

```json
{
  "access_token": "your_token_here",
  "token_type": "bearer"
}
```

Use token in Swagger Authorize button:

```bash
Bearer your_token_here
```

---

# 🛠 Example Request Body

## Create User

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

## Create Post

```json
{
  "title": "My First Post",
  "content": "Learning FastAPI is awesome!",
  "published": true
}
```

---

# 🌱 Learning Goals

This project is mainly built for learning:

- How FastAPI works internally
- API development best practices
- Backend architecture
- Authentication flow
- Database integration
- Clean code structure
- Async Python basics

---

# 🚀 Future Improvements

- Pagination
- Likes system
- Comments
- Docker setup
- Redis caching
- Unit testing
- CI/CD pipeline
- Deployment

---

# 🤝 Contributing

This project is for learning purposes, but contributions and suggestions are welcome.

---

# 📌 Useful Commands

## Run server

```bash
uvicorn app.main:app --reload
```

## Freeze dependencies

```bash
pip freeze > requirements.txt
```

## Create migration

```bash
alembic revision --autogenerate -m "message"
```

## Run migrations

```bash
alembic upgrade head
```

---

# 📷 FastAPI Docs Preview

- Swagger UI for testing APIs
- Automatic validation
- Interactive API documentation

---

# 📄 License

This project is open-source and available under the MIT License.

---

# ⭐ Learning Resources

- FastAPI Official Docs
- SQLAlchemy Docs
- Pydantic Docs
- Python AsyncIO Docs

---

Built with ❤️ while learning FastAPI.


