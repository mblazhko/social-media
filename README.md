# Social Media API

This is a Django-based content management project that allows users to create posts, upload images for the posts, and interact with posts through liking. The project includes custom user models, serializers, permission classes, and views to handle user registration, authentication, and profile management.

## Table of Contents
1. [Installation](#Installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)

## Installation

To set up the project, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/django-content-management.git
    cd django-content-management

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

4. Apply database migrations:
    ```bash
    python manage.py migrate

5. Run the development server:
    ```bash
    python manage.py runserver

## Usage

You can use test admin user made during migration:

   - Email ```test@admin.com```
   - Password ```testpass123```

## API Endpoints
The project exposes several API endpoints for user registration, authentication, and post management.

1. User Registration: POST /api/user/register/
2. User Login: POST /api/token/
3. User Logout: POST /api/token/logout
4. User Profile: GET/PUT/PATCH /api/user/me/
5. Post List: GET /api/posts/
6. Post Detail: GET /api/posts/{post_id}/
7. Post Creation: POST /api/posts/
8. Post Update: PUT/PATCH /api/posts/{post_id}/
9. Post Deletion: DELETE /api/posts/{post_id}/