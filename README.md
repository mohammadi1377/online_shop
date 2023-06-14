
# Online Jewelry Shop

This is an online jewelry shop built with Django and Django Rest Framework (DRF). It provides a RESTful API for managing jewelry products, cart, orders, user profiles, and authentication using JWT. The shop also integrates Redis and Celery for OTP generation and verification. The frontend is developed using Bootstrap, jQuery, and AJAX.

## Features

- User registration and authentication using JWT
- Login with OTP (One-Time Password)
- Jewelry product listing and details
- Cart functionality with DRF endpoints
- Order placement and management
- User profile management
- OTP generation and verification using Redis and Celery
- Responsive and user-friendly UI with Bootstrap, jQuery, and AJAX

## Requirements

- Python 3.10
- Django 3.x
- Django Rest Framework 3.x
- Redis
- Celery
- Bootstrap
- jQuery
- AJAX

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Change to the project directory:
   ```
   cd online-jewelry-shop
   ```

3. Create and activate a virtual environment (optional but recommended):
   ```
   python3 -m venv env
   source env/bin/activate
   ```

4. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up the database:
   ```
   python manage.py migrate
   ```

6. Start the Redis server:
   ```
   redis-server
   ```

7. Start Celery worker for OTP generation and verification:
   ```
   celery -A online_jewelry_shop worker -l info
   ```

8. Start the development server:
   ```
   python manage.py runserver
   ```

9. Access the application at `http://localhost:8000`.

## Configuration

- Database settings: The project is configured to use SQLite by default. If you wish to use a different database, update the `DATABASES` setting in the `settings.py` file.

- JWT authentication: The project uses JWT for user authentication. You can configure the JWT settings, such as expiration time, in the `settings.py` file.

- OTP configuration: The project integrates Redis and Celery for OTP generation and verification. You can customize the Redis and Celery settings in the `settings.py` file.

## API Documentation

The API endpoints and their usage are documented using the built-in DRF documentation. After starting the development server, you can access the API documentation at `http://localhost:8000/api/docs`.

## Frontend

The frontend of the online jewelry shop is built using Bootstrap, jQuery, and AJAX for a responsive and interactive user interface. The relevant static files are located in the `static` directory.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to modify and adapt this README file to suit your specific project requirements.
