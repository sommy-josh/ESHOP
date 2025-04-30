feature-rich E-Commerce RESTful API built with Django Rest Framework. This API supports user registration with JWT authentication, product management, shopping cart, order processing, and email notifications using Gmail SMTP. It uses PostgreSQL as the database and is tested with Postman.

Features

User Registration & Authentication (JWT)

Email confirmation on registration using Gmail SMTP

Product Catalog (Add, Update, List, Delete)

Shopping Cart Functionality

Order Creation & Tracking

PostgreSQL Database Integration

API Testing with Postman

Tech Stack
Backend Framework: Django, Django REST Framework

Authentication: JWT (JSON Web Tokens)

Email Service: Gmail SMTP

Database: PostgreSQL

Testing Tool: Postman

Getting Started
Prerequisites
Python 3.8+

PostgreSQL

Git

Installation
1.Clone the repository
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api

2.Create a virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
3.Install dependencies
pip install -r requirements.txt
4.Configure environment variables
Create a .env file in the root directory with the following:
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST_USER=your_gmail_address@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
