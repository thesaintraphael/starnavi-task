# Starnavi task

## API Documentation

    / - Swagger UI for API docs
    /swagger/api.json - JSON format of docs. Install or import to Postman
    /redoc- Read only doc.


## Run Locally
     1. Create a virtual environment and activate it: 
            python -m venv venv
            venv\Scripts\activate
     
     2. Install requirements: 
            pip install -r requirements.txt

     3. Create .env file and and env variables to it.
        Email credentials are required to sign up and verify account, you can 
        add your own credentials to .env or you use test account I 
        created. (credentials are in core/credentials.py)

     
     3. Migrate db: 
            py manage.py migrate

     4. Run: 
            py manage.py runserver


## Executing Tests
    python manage.py test