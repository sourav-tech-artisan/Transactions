# Problem
Develop a transaction service that allows users to create, read and update a transaction. A transaction has attributes such as transaction id, amount, transaction type and parent id. A transaction can have multiple children transactions. The service should be able to return the total amount of a transaction including all its children transactions.
The service should also be able to return a specific type of transactions. For example, all transactions of type "deposit" or "withdrawal". 

## Framework
Django serves as the core framework for building the transaction service. It provides a robust foundation for creating web applications with a clean and maintainable codebase. The service is structured using Django models, views, and serializers to define the data schema, request handling logic, and data serialization respectively. The Django ORM facilitates database operations and ensures data integrity by enforcing constraints and relationships between models.

# Directory Structure
```
.
├── pyproject.toml            # Poetry file specifying Python dependencies
├── README.md                 # Markdown file containing project documentation
├── manage.py                 # Django management script for running administrative tasks
├── docker                    # Directory containing Docker configuration files
│   ├── docker-compose.yml    # Docker Compose file for defining multi-container Docker applications
├── app                       # Django root application directory
│   ├── __init__.py           # Initialization file for the dental package
│   ├── asgi.py               # ASGI configuration for the Django application
│   ├── settings.py           # Django settings file for application configuration
│   ├── urls.py               # Django URL configuration file
│   └── wsgi.py               # WSGI configuration for the Django application
│   ├── apps          # Package containing application dependencies
│   │   ├── base              # base app for common functionalities
│   │   ├── transactions      # transactions app for transaction functionalities
```

# Running the project

To run the project locally -

```
1. Install poetry
2. Run `poetry install` to install dependencies
3. Run `poetry run python manage.py runserver` to start the Django development server
```

## Run Unit Tests for transaction app
```
poetry run python manage.py test app/apps/transactions/tests
```

