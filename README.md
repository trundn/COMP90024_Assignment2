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

## Deployment

*  Navigate to the deployment folder by typing:
*  `cd deployment`
*  The instance key has been added to the deployment folder

#### Deploying Instances

*  Type the following command to deploy the instances
*  `./create_instances.sh`
*  Enter the Openstack Password as:
*  `NjljNWFmMDgwNTI5ZDc2`
*  Enter your root password of your localhost

#### Deploying CouchDB cluster

*  Type the following command to deploy the couchDB cluster
*  `./deploy_couchdb.sh`
*  You will be promoted to enter Openstack Password here you can just press enter
*  You will be promoted to enter the root password of your localhost but you simply press enter

These have been added incase future deployment through the localhost is added to this part

#### Deploying Harvesters

*  Type the following command to deploy the Harvesters
*  `./deploy_harvester.sh`
*  You will be promoted to enter Openstack Password here you can just press enter
*  You will be promoted to enter the root password of your localhost but you simply press enter

These have been added incase future deployment through the localhost is added to this part

#### Deploying Application

*  Type the following command to deploy the Application
*  `./deploy_app.sh`
*  You will be promoted to enter Openstack Password here you can just press enter
*  You will be promoted to enter the root password of your localhost but you simply press enter

These have been added incase future deployment through the localhost is added to this part