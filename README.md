# Blogging Platform API

## Description
A powerful Django REST API for a modern blogging platform. This API provides comprehensive endpoints for managing blog posts, user authentication, categories, and search functionality.

## Tech Stack
- Django 5.1.4
- Django REST Framework 3.15.2
- MySQL Database
- Django Filter 24.3
- Pillow 11.0.0

## Features
- User Authentication with Token-based system
- CRUD operations for blog posts
- Category management
- Search and filter functionality
- Admin-only operations
- Pagination support
- Ordering capabilities

## API Endpoints

### Authentication Endpoints
```
POST /accounts/user/register/     - Register a new user
POST /accounts/user/login/        - Login user and get token
POST /accounts/user/logout/       - Logout user (requires token)
GET  /accounts/user/list/         - List all users (admin only)
PUT  /accounts/user/update/{id}/  - Update user profile
```

### Blog Endpoints
```
GET    /blog/list/                - List all blog posts (with pagination)
GET    /blog/detail/{id}/         - Get specific blog post
POST   /blog/create/              - Create new blog post
PUT    /blog/update/{id}/         - Update blog post (owner only)
DELETE /blog/delete/{id}/         - Delete blog post (owner or admin)
```

### Category Endpoints
```
POST   /blog/category/create/     - Create new category (admin only)
```

### Search and Filter Endpoints
```
GET    /blog/search/              - Search blogs (query params: q)
GET    /blog/filter/              - Filter blogs
```

## Authentication
The API uses Token Authentication. Include the token in the Authorization header:
```
Authorization: Token your_token_here
```

## Request Examples

### Register a New User
```http
POST /accounts/user/register/
Content-Type: application/json

{
    "username": "user123",
    "email": "user@example.com",
    "password": "secure_password"
}
```

### Create a Blog Post
```http
POST /blog/create/
Authorization: Token your_token_here
Content-Type: application/json

{
    "Title": "My Blog Post",
    "Content": "Blog post content here",
    "Category": "Technology",
    "tags": ["python", "django"]
}
```

### Search Blogs
```http
GET /blog/search/?q=python
```

### Filter and Order Blogs
```http
GET /blog/list/?ordering=-Published_Date
GET /blog/list/?ordering=Category
```

## Installation

1. Clone the repository:
```bash
git clone <https://github.com/YahiaaFoudaa/Blogging_Platform_Api.git>
cd Blogging_Platform_Api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your database in settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## Error Handling
The API returns standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

