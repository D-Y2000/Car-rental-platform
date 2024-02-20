# Car-rental-platform

A Platform that allow individuals to rent cars from multiple agencies

## Instalation

### setup envirnement

    # clone project
    git clone https://github.com/D-Y2000/Car-rental-platform.git
    cd project

    # create envirnement
    py -m venv env

    # activate env
    env\Script\activate

    # install requirements
    pip install requirements.txt

    # setup db
    py manage.py makemirations
    py manage.py migrate

    # create admin user (superuser)
    py manage.py createsuperuser

    # run localhost
    py manage.py runserver

## About API

### GET all agencies

Send **GET** request to:

**api**

    [BASE_URL]/api_agency/agencies/

**result**

    {
        "id": 1,
        "user": {
            "id": 2,
            "email": ""
        },
        "name": "",
        "phone_number": "",
        "bio": "",
        "license_doc": "",
        "photo": "",
        "email": "",
        "location": "",
        "address": "",
        "website": "",
        "is_validated": false,
        "created_at": ""
    }

### Create user (agency owner) + agency (profile)

Send **Post** request to:

**api**

    [BASE_URL]/api_agency/agencies/

**required params**

    {
        "user": {
            "email": "email@example.com"
            "password": "........."
            "password2": "........."
        },
        "name": "Name",
        "phone_number": "00000000",
        "bio": "Hello, Wolrd",
        "license_doc": ImageURL,
        "photo": ImageURL,
        "email": "company@contact.com",
        "location": "Algeria",
        "address": "Alger",
        "website": "www.company.com"
    }
### Login user 
**api**

    [BASE_URL]/api_agency/login/
**required params**
    {
        "username":"adr@gmail.com",
        "password":"password"   
    }
### List and create branch for the agency
**api**
    [BASE_URL]/api_agency/branches/
**required params**
    Token in request header
    {
        "name":"Branch name"
    }
### Edit agency Infos
**api**

    [BASE_URL]/api_agency/agencies/<int:pk>(agency_id)/
**required params**
    Token in request header
    {
        "name": "Agency name",
        "phone_number": "phone number"
    }
### Update branch
**api**

    [BASE_URL]/api_agency/branches/<int:pk>(branch_id)/

**required params**
    Token in request header
    {
    "name":" Branch"
}

### logout user 
**api**

    [BASE_URL]/api_agency/logout/


**required params**
    Token in request header
    
