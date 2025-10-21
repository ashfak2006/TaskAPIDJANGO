# Task Management App

A simple web-based application for managing tasks. This project is built using Django and designed to be run with Docker.

## Features

- Create, read, update, and delete tasks.
- User authentication (login, logout).
- Assign tasks to users.
- Mark tasks as complete.

## Technologies Used

- **Backend**: Python 3.12, Django
- **Database**: SQLite (default for development, can be configured for PostgreSQL/MySQL)
- **Containerization**: Docker

## Setup Instructions

Follow these steps to get the Task Management App up and running on your local machine.

### Prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/your-username/TaskManagmentApp.git
cd TaskManagmentApp/Backend/taskapi
```

### 2. Build and Run with Docker

Navigate to the directory containing the `Dockerfile` (e.g., `Backend/taskapi`) and build the Docker image, then run the container:

```bash
docker build -t task-management-app .
docker run -p 8000:8000 --name task-app-container task-management-app
```

### 3. Apply Database Migrations

Once the container is running, you need to apply the database migrations. Open a new terminal and execute the following commands:

```bash
docker exec -it task-app-container python manage.py migrate
```

### 4. Create a Superuser (Optional)

To access the Django admin panel, you'll need to create a superuser:

```bash
docker exec -it task-app-container python manage.py createsuperuser
```
Follow the prompts to set up your superuser credentials.

## Usage

After completing the setup, the application should be accessible in your web browser at:

```
http://localhost:8000/
```

You can access the Django admin panel at `http://localhost:8000/admin/` using the superuser credentials you created.

## Contributing

Contributions are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
