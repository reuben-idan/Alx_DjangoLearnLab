# Django Learning Lab

A comprehensive Django development environment and learning project focused on mastering Django fundamentals through hands-on implementation.

## Project Overview

This repository contains a structured Django learning project that demonstrates core Django concepts including project setup, model creation, database operations, and admin interface customization.

## Project Structure

```
Alx_DjangoLearnLab/
├── LibraryProject/                 # Main Django project
│   ├── LibraryProject/            # Project configuration
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # URL configuration
│   │   └── wsgi.py               # WSGI application
│   ├── bookshelf/                # Django app
│   │   ├── models.py             # Book model definition
│   │   ├── admin.py              # Admin interface configuration
│   │   └── migrations/           # Database migrations
│   ├── manage.py                 # Django management script
│   └── README.md                 # Project documentation
├── create.md                      # CRUD Create operation
├── retrieve.md                    # CRUD Retrieve operation
├── update.md                      # CRUD Update operation
├── delete.md                      # CRUD Delete operation
└── CRUD_operations.md             # Complete CRUD documentation
```

## Features

### Task 0: Django Development Environment

- Complete Django project setup with LibraryProject
- Development server configuration
- Project structure exploration
- Basic project documentation

### Task 1: Django Models and CRUD Operations

- Custom Book model with specified attributes
- Complete CRUD operations implementation
- Django ORM usage demonstration
- Comprehensive operation documentation

### Task 2: Django Admin Interface

- Model registration with Django admin
- Customized admin interface with list display, filters, and search
- Enhanced data management capabilities
- Superuser account creation for admin access

## Technology Stack

- **Framework**: Django 5.2.3
- **Database**: SQLite3
- **Language**: Python 3.12
- **Development Server**: Django Development Server

## Installation and Setup

### Prerequisites

- Python 3.12 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/reuben-idan/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab
   ```

2. **Install Django**

   ```bash
   pip install django
   ```

3. **Navigate to project directory**

   ```bash
   cd LibraryProject
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start development server**

   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`
   - For admin interface: `http://127.0.0.1:8000/admin/`

## Book Model Specification

The Book model includes the following fields:

| Field            | Type         | Max Length | Description         |
| ---------------- | ------------ | ---------- | ------------------- |
| title            | CharField    | 200        | Book title          |
| author           | CharField    | 100        | Book author         |
| publication_year | IntegerField | -          | Year of publication |

## CRUD Operations

The project demonstrates complete CRUD operations for the Book model:

- **Create**: Add new book instances
- **Retrieve**: Query and display book information
- **Update**: Modify existing book records
- **Delete**: Remove book instances from database

Detailed operation examples are documented in individual markdown files and the comprehensive CRUD_operations.md file.

## Development Workflow

1. **Model Development**: Define models in `bookshelf/models.py`
2. **Migration Management**: Create and apply database migrations
3. **Shell Testing**: Use Django shell for model testing
4. **Admin Configuration**: Customize admin interface in `bookshelf/admin.py`
5. **Documentation**: Maintain comprehensive operation documentation

## File Documentation

- `create.md`: Book creation operation with expected output
- `retrieve.md`: Book retrieval operation with expected output
- `update.md`: Book update operation with expected output
- `delete.md`: Book deletion operation with expected output
- `CRUD_operations.md`: Complete CRUD operations reference
- `admin_setup.md`: Django admin interface configuration and usage

## Contributing

This project is designed for educational purposes and follows Django best practices. Contributions should maintain the learning-focused structure and comprehensive documentation standards.

## License

This project is created for educational purposes as part of the Django learning curriculum.

## Contact

For questions or feedback regarding this Django learning project, please refer to the project repository or contact the development team.

---

_Built with Django - A high-level Python web framework_
