# COMP90024_Assignment2

## Installing Backend

#### Create a virtual environment to isolate our package dependencies locally
* `python3.7 -m venv env`
* `source env/bin/activate`  # On Windows use `env\Scripts\activate`

#### Install Django and Django REST framework into the virtual environment
* `pip install django`
* `pip install djangorestframework`

#### Install dependencies
* `pip install couchdb`
* `pip install Shapely`
* `pip install django-cors-headers`

Config the couchdb endpoint in file backend/settings.py (line 128, 129, 130)

#### Run server
* `cd backend`
* `python manage.py runserver`

## Installing Frontend

*  Install yarn globally by `npm install yarn -g`
* `cd gui`
* `yarn install`
* `yarn start`

Config the backend endpoint in file backendUrl.js (line 1)