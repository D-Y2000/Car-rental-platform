# Car-rental-platform

A Platform that allow individuals to rent cars from multiple agencies

# API

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
