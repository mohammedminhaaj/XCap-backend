# XCap

This README file will guide you through setting up the XCap project on your local machine. It includes steps for creating and activating a virtual environment, installing dependencies, creating migrations, creating superuser, running the Django development server, accessing the admin site, and starting the Celery worker

## Table of Contents

1. [Getting Started](#getting-started)
    1.1. [Clone The Repository](#clone-the-repository)
2. [Setting Up the Virtual Environment](#setting-up-the-virtual-environment)
    2.2. [Create The Virtual Environment](#create-the-virtual-environment)
3. [Installing Dependencies](#installing-dependencies)
4. [Additional Configuration](#additional-configuration)
    4.1. [Managing ENV file](#managing-env-file)
    4.2. [Configuring Redis](#configuring-redis-endpoint)
5. [Running Migrations](#running-migrations)
6. [Creating Superuser](#creating-superuser)
7. [Running the Development Server](#running-the-development-server)
8. [Accessing Django Admin](#accessing-django-admin)
9. [Running Celery Worker](#running-celery-worker)
10. [Additional Resources](#additional-resources)

## Getting Started

Before you begin, ensure you have the following software installed on your machine:

- Python
- pip (Python package installer)
- Redis (for Celery)
- Git

### Clone the Repository

Clone the repository using the following command:

` >> git clone https://github.com/mohammedminhaaj/XCap-backend `
` >> cd XCap-backend `

## Setting Up the Virtual Environment

A virtual environment isolates your Python environment for the project, ensuring that dependencies do not conflict with other projects.

### Create the Virtual Environment

Run the following command to create a virtual environment in the project directory:

` >> python -m venv venv `

This will create a directory named venv that contains the virtual environment.

### Activate the Virtual Environment

To activate the virtual environment, run the following command:

- On Windows
    ` >> venv\Scripts\activate `
- On Linux
    ` >> source venv/bin/activate `

Once activated, your command prompt should change to indicate that you are now working within the virtual environment.

## Installing Dependencies

With the virtual environment activated, install the necessary dependencies using the requirements.txt file:

` >> pip install -r requirements.txt `

This command will install all the Python packages required to run the project.

## Additional Configuration

### Managing ENV File

To manage sensitive information such as API keys or database credentials, we use an environment file (.env). Create a .env file in the root directory of your project and add the below key and value to run the development server without any issues.

`DJANGO_SECRET_KEY=secret123`

Although, the secret key isn't secret enough, it does the job of starting our development server without any errors. Using any key for testing purpose is fine as long as we are not deploying this application on production.

### Configuring Redis Endpoint

Once your redis server is up and running, make sure to run the below command to have a glimpse at the server endpoint:

` >> redis-cli `

This endpoint should match the endpoint defined in settings.py file.

```python

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"

```

This configuration is required for celery to successfully use the endpoint as a message broker.

## Running Migrations

Running migrations will create the necessary tables in your database (sqlite3) which are required to run the project. To do so, we need to run the following command:

` >> python manage.py migrate `

Make sure you are in the same directory as manage.py to run this command without any errors

## Creating Superuser

To access the Django admin interface, you'll need to create a superuser. Run the following command:

` >> python manage.py createsuperuser `

You'll be prompted to enter a username, email, and password for the superuser.

## Running the Development Server

In order to access the application and Django admin interface, we need to start the development server. To start the Django development server, ensure your virtual environment is activated and run:

` >> python manage.py runserver `

The server will start, and you can access the application at http://127.0.0.1:8000/ in your web browser.

## Accessing Django Admin

Once the server is running and a superuser has been created, you can access the Django admin interface by opening your web browser and navigating to http://127.0.0.1:8000/admin/. Log in with the superuser credentials which you created previously. After logging in, you should have access to the Django admin interface where you can manage your models, users, and more.

## Running Celery Worker

Celery is used for handling asynchronous tasks in this project. To start the Celery worker, use the following command:

` >> celery -A xcap worker -l INFO `

Make sure you are in the same location as your settings.py

This command will start the Celery worker, which will listen for and execute tasks defined in this project.


## Additional Resources

This project has been implemented alongside a front-end application that runs on ReactJS. You can access the front-end project through the following link:

[XCap-frontend](https://github.com/mohammedminhaaj/XCap-frontend)

This integration allows users to interact with the backend services provided by this Django application, facilitating a seamless experience.
