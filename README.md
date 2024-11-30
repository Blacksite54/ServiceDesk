# ServiceDesk - Application for managing user requests

This project implements a simple service desk application using Django, DRF, PostgreSQL, Redis, and Celery.  It allows users to submit requests via email, assigns requests to support staff, and provides an API for managing requests.

## Project Description

ServiceDesk provides a backend system for handling user support requests.  Users can submit requests, receive automated responses, and communicate with support staff.  Support staff can manage requests through an API.  The system uses Celery for asynchronous task processing (sending emails) and Redis for task queueing.


## Technologies Used

* **Backend:** Django, Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Task Queue:** Celery
* **Cache/Queue Broker:** Redis
* **Email:**  (Configure your email settings)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Docker
* Docker Compose
* Python 3.9+
* A PostgreSQL user with write access.

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd servicedesk
Install dependencies:
   pip install -r requirements.txt

Create a .env file: This file should contain your environment variables. A sample .env file is provided. You will need to customize this to match your database credentials, email settings, and the SECRET_KEY.

DATABASE_URL=postgres://postgres:admin@postgres:5432/sakura
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_password
SECRET_KEY=your_secret_key
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
Run docker-compose:

docker-compose up -d --build
This command will build the Docker images and start all the containers (web server, database, Redis, Celery worker, and Celery beat).

Migrate Database: Wait for the containers to start up. Then open a separate terminal in the project directory and run:

docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

