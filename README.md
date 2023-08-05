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

1. User Registration: POST /api/v1/user/register/
2. User Login: POST /api/token/
3. User Profile: GET/PUT/PATCH /api/v1/user/me/
4. Post List: GET /api/v1/posts/
5. Post Detail: GET /api/v1/posts/{post_id}/
6. Post Creation: POST /api/v1/posts/
7. Post Update: PUT/PATCH /api/v1/posts/{post_id}/
8. Post Deletion: DELETE /api/v1/posts/{post_id}/