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
        "user": {
            "id": 2,
            "email": "daichekkal@gmail.com"
        },
        "name": "dxk cars",
        "phone_number": "123456",
        "bio": null,
        "license_doc": null,
        "photo": null
    }

### Create user (agency owner) + agency (profile)

Send **Post** request to:

**api**

    [BASE_URL]/api_agency/agencies/

**required params**

    {
        "user": {
            "email": "daichekkal@gmail.com"
            "password": "password_123",
            "password2": "password_123",
        },
        "name": "",
        "phone_number": "",
    }
