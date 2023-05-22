Capstone Project - Sanctioned Companies
---------------	

## Overview

Capstone Project - Sanctioned Companies is an API that enables users to access information about Brazilian companies, with a particular emphasis on details regarding the companies' partners and any sanctions they may have received from the Brazilian Office of the Comptroller General (CGU). This information holds great significance for public organizations, as they are obligated to adhere to legislation that explicitly forbids entering into contracts with sanctioned companies or those where a partner possesses a sanctioned company.

Currently, this API offers basic functionality, allowing users to:

* Maintain a database of companies
* Maintain a database of partners
* Associate partners with their respective companies
* Maintain a record of sanctions

In the near future, the database will be populated with real data from official sources. Additionally, there are plans to implement more advanced search capabilities to enable users to perform complex queries. The API is in the following URK:

### Set up the Database

This project expect that you have Postgres running. Once you have it, create a `capstone_project` database:

```bash
sudo -u postgres bash -c "createdb capstone_project"
```

Populate the database using the `database.psql` file. From the `capstone_project` folder in terminal run:

```bash
sudo -u postgres bash -c "psql capstone_project < database.psql"
```

## Project Dependencies

In order to run the project, it is necessary to install Python 3.8.x or later. Next, some important dependencies will be listed, and an explanation of how to install the remaining dependencies and set up the development environment will be provided.

### Key Dependencies

- [Flask](https://flask.palletsprojects.com/en/2.3.x/) a micro web framework used to create API's routes and handle requests.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the SQL toolkit and ORM used to interact with relational database.

- [Gunicorn](https://gunicorn.org/) is a Python WSGI HTTP Server for UNIX. As Flask's built-in server is not suitable for production, gunicorn is is used to deploy the aplication.

## Set up the Development Environment

1. To begin, please follow these instructions to install a virtual environment: [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

2. Activate the created virtual environment.

3. Edit the enviroment viriables in `bash.sh` according to your Auth0 and database configurations.

4. Set the rigth permission to the `bash.sh` file:

```bash
chmod +x bash.sh
```

5. Execute `bash.sh` file:

```bash
source ./bash.sh
```

6. Navigate to `.src` and install the project`s dependencies:

```bash
pip3 install -r requirements.txt
```

7. From within the `./capstone_project` folder, run:

```bash
export FLASK_APP=src;
```

8. To run the server, execute:

```bash
flask run --reload
```

## How to Deploy the Project on Render

First, it is necessary to create a Render acount on [this link](https://dashboard.render.com/register).

After that, in [Render Dashboard](https://dashboard.render.com/), set up a Database Service with Postgres by clicking on `New -> PostgreSQL`:

![Create Postgres service on Render.](https://lh3.googleusercontent.com/drive-viewer/AFGJ81qJdMeBON2elZsedFeRBfqYmHjL-3tkYE_4WlwlMHWhVCZH-Yy-KBrxsjw-RceVS2z1xHTJ0naqKyAmNjHtc2XK0xvM=s1600)

On the "New Postgres" page:

1. Provide a name for the service

![Provide service name.](https://lh3.googleusercontent.com/drive-viewer/AFGJ81oRX5L64GBHEPq0qJz7za2M_wG-h4-EmRbjLgNqrpkugxwyVZc2amTU6jlCxc-GvmPc52IK-XT7RLV9Bdg0DiL3Y-6KoA=s1600)

2. Select an `Free` instance 

3. Click on Create Database

![Create Database Service](https://lh3.googleusercontent.com/drive-viewer/AFGJ81r1iOQu2cpt5UhTbzJTtXVeGho_OPiwbAQMqYSsyLxST5vx8vkLMRYpMzNKrvaHwXmzxpDbRUnL34gc1B6nGWPMOyMe5g=s1600)

Next, go back to [Render Dashboard](https://dashboard.render.com/) and create a new Web Service by clicking on `New -> Web Service`.

![Create Web Service on Render.](https://lh3.googleusercontent.com/drive-viewer/AFGJ81r11V2hx-uyLeKbWMIH2X-ph8Ha09t4V50jEOr2O2kxwOMkgWHzT5PkHNQPpOLB2oP-XZS8b06P9gqwdmXygH6IvISZuQ=s2560) 

Provide the GitHub repo to the webservice:

![Provide Github repo.](https://lh3.googleusercontent.com/drive-viewer/AFGJ81qbOGgUjFJyq_Ituiz9ocsSdEW8FlOV_C-qmMPcvXpKqzPOoTaoCz5TCiaeOgiY0ynR6A1MBo65_4-DvtbpgWRtDMJX=s1600)

Provide de following informations: 

1. A name for the service

2. Select the branch `main`

3. Runtime `Python3`

4. Build Command `pip install -r requirements.txt`

5. Start Command `gunicorn wsgi:app`

![Info for web service creation.](https://lh3.googleusercontent.com/drive-viewer/AFGJ81qUjsHdmk6wzNHp_p4A1_5-rppS8kPkIoNG79BTDRWV2rmKvVgVQ6gq8iquyg-6ozmw9oVF5qRF6_GqH3A0w5lWkuz3Ag=s1600)

Before clicking in Create New Service it is is necessary to connect it to the Database Service. To do that, open a new browser's tab and go to the Database Service Info page an copy the External Database URL:

![Copy database external URL.](https://lh3.googleusercontent.com/drive-viewer/AFGJ81oB3R-Rsm5gE537IVpFVtytduYVUeDRXHiSLsPo04kW8TvAEauS-5M4K3d-in_i5iYRkIxfzCD8R6Xvqq9H05QEoOXNtw=s1600)

After that, go back to the Web Service creation and create the folowing environment variables in `Advanced`:

* SQLALCHEMY_DATABASE_URI: paste the database external URL

* SQLALCHEMY_TRACK_MODIFICATIONS: `False`

* AUTH0_DOMAIN: info from auth0 (`dev-g8ovzwsj4zhype80.us.auth0.com`)

* API_AUDIENCE: info from auth0 (`capstone_project`)

* ALGORITHMS: info from auth0 (`['RS256']`)

* PYTHON_VERSION: Render installs python 3.7 by default. As we need python 3.8.x or latest, set the value to `3.8.10`.

![Environment Variables.](https://lh3.googleusercontent.com/drive-viewer/AFGJ81o8wZw5Qrrdak-pFz305nVR5yz6kwMtcLrw6rMtdDOI8x0_l3rBtABhJ20xN88EXP-s-WuXkJrnlvIzswSz78-9set6ew=s1600)

Make sure you select a Free instance and click on `Create Web Service`.

![Create Web Service.](https://lh3.googleusercontent.com/drive-viewer/AFGJ81pKqOLr1kT3-h4lfRf7uPKYbYySG0_x5ynz48cDKjNi0WY5-Zdi4cAnw_EKpSFe0ZWwwxCZvK82AR2D4KE7qUlkLvxnuw=s1600)

After the creation, the aplication will be deployed. When the service is ready, the application can be oppened on the browser by clicking the app URL.

![App URL.](https://lh3.googleusercontent.com/drive-viewer/AFGJ81r7mV7-YbjdvA5G1PrP2gOIDR4xR0a2CEEva0tzhDRMg2Bh8lwFDhn4cpFrOmz2twj3haP4U9ITQo2NQjB939EDlHeyVQ=s1600)

## API

Base URL: `https://jvguinelli-service.onrender.com`

## Authentication

## Endpoints

### List Companies

Endpoint: `/companies`

Method: `GET`

Description: Retrieves a list of all companies in the database.

Request: 

```
GET /companies
```

Response:

```json
Status: 200 OK
Content-Type: application/json

{
  "success": True,
  "companies": [
    {
      "id": 1,
      "fiscal_number": "53846386956648",
      "name": "ACME CORP.", 
      "partners": [
        { 
          "id": 2,
          "document": "14235717343", 
          "name": "PEDRO COELHO"
        }, 
        {
          "document": "14432471734", 
          "id": 3, 
          "name": "MAYCK SILVA"
        }
      ],
      "sanctions": [
        {
          "id": 1,
          "organization": "CGU - CONTROLADORIA GERAL DA UNIAO"
        }
      ]
    }, 
    {
      "id": 2,
      "fiscal_number": "53846386956649",
      "name": "ABC INDUSTRY", 
      "partners": [
        { 
          "id": 2,
          "document": "14235717345", 
          "name": "PEDRO COELHO"
        }
      ],
      "sanctions": []
    }, 
  ]
}
```

### Create Company

Endpoint: `/companies`

Method: `POST`

Description: Create a new company in the database.

Request: 

```json
POST /companies
Content-Type: application/json

{
  "fiscal_number": "12345654321789",
  "name": "XYZ SA"
}
```

Response:

```json
Status: 201 CREATED
Content-Type: application/json

{
  "success": True,
  "created": 3
}
```

### Update Company

Endpoint: `/companies/{id}`

Method: `PATCH`

Description: Update information about a company in the database.

Request: 

```json
PATCH /companies/3
Content-Type: application/json

{
  "name": "XYZ CORP"
}
```

Response:

```json
Status: 200 OK
Content-Type: application/json

{
  "success": True,
  "updated": 3
}
```

### Delete Company

Endpoint: `/companies/{id}`

Method: `DELETE`

Description: Delete a company from the database.

Request: 

```json
DELETE /companies/3
```

Response:

```json
Status: 200 OK
Content-Type: application/json

{
  "success": True,
  "deleted": 3
}
```

### List Partners

Endpoint: `/partners`

Method: `GET`

Description: Retrieves a list of all partners in the database.

Request: 

```
GET /partners
```

Response:

```json
Status: 200 OK
Content-Type: application/json

{
  "success": True,
  "partners": [
    {
      "id": 2, 
      "document": "14235717343", 
      "name": "PEDRO COELHO", 
      "companies": [
        {
          "id": 1,
          "fiscal_number": "53846386956648",
          "name": "ACME CORP.",
          "sanctions": [
            {
              "id": 1,
              "organization": "CGU - CONTROLADORIA GERAL DA UNIAO"
            }
          ]
        }, 
        {
          "id": 2,
          "fiscal_number": "53846386956648",
          "name": "ABC INDUSTRY", 
          "sanctions": []
        }, 
      ]
    }, 
    {
      "id": 3, 
      "document": "14432471734", 
      "name": "MAYCK SILVA", 
      "companies": [
        {
          "id": 1,
          "fiscal_number": "53846386956648",
          "name": "ACME CORP.",
          "sanctions": [
            {
              "id": 1,
              "organization": "CGU - CONTROLADORIA GERAL DA UNIAO"
            }
          ]
        }
      ]
    }
  ]
} 
```

### Create Partner

Endpoint: `/partners`

Method: `POST`

Description: Create a new partner in the database.

Request: 

```json
POST /partners
Content-Type: application/json

{
  "document": "14352386732",
  "name": "JUAN LOPES"
}
```

Response:

```json
Status: 201 CREATED
Content-Type: application/json

{
  "success": True,
  "created": 3
}
```

### Update Partner

Endpoint: `/partners/{id}`

Method: `PATCH`

Description: Update information about a partner in the database.

Request: 

```json
PATCH /partners/3
Content-Type: application/json

{
  "document": "14352386302",
  "name": "JOSE LOPES"
}
```

Response:

```json
Status: 200 OK
Content-Type: application/json

{
  "success": True,
  "updated": 3
}
```

### Delete Partner

Endpoint: `/partners/{id}`

Method: `DELETE`

Description: Delete a Partner from the database.

Request: 

```json
DELETE /partners/3
```

Response:

```json
Status: 200 OK
Content-Type: application/json

{
  "success": True,
  "deleted": 3
}
```

### Associate a Partner with its Company

Endpoint: `/companies/{id}/partners/{id}`

Method: `PUT`

Description: Associate a partner with its company.

Request: 

```json
PUT /companies/3/partners/2
```

Response:

```json
Status: 200 OK
Content-Type: application/json

{
  "success": True
}
```

### Create Sanction

Endpoint: `/companies/{id}/sanctions`

Method: `POST`

Description: Create a new sanction for a company in the database.

Request: 

```json
POST /companies/1/sanctions
Content-Type: application/json

{
  "name": "CEIS - Cadastro de Empresas Inidôneas e Suspensas",
  "organization": "CGU - CONTROLADORIA GERAL DA UNIAO"
}
```

Response:

```json
Status: 201 CREATED
Content-Type: application/json

{
  "success": True,
  "created": 1
}
```

### Delete Sanction

Endpoint: `/sanctions/{id}`

Method: `DELETE`

Description: Delete a Sanction from the database.

Request: 

```json
DELETE /sanctions/1
```

Response:


```json
Status: 200 OK
Content-Type: application/json

{
  "success": True,
  "deleted": 1
}
```

## Error Handling

In case of errors, the API may return the following status codes:

* 400 Bad Request: 

```json
Status: 400 BAD REQUEST
Content-Type: application/json

{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```

* 401 Unauthorized: the "message" field precisely indicates the underlying cause of the error.

```json
Status: 401 UNAUTHORIZED
Content-Type: application/json

{
  "success": False,
  "error": "401",
  "message": "String indicating specific error"
}
```


* 403 Forbidden: the "message" field precisely indicates the underlying cause of the error.

```json
Status: 403 FORBIDDEN
Content-Type: application/json

{
  "success": False,
  "error": "403",
  "message": "String indicating specific error"
}
```

* 404 Not Found: 
```json
Status: 404 BAD REQUEST
Content-Type: application/json

{
  "success": False,
  "error": 404,
  "message": "not found"
}
```

* 405 Method Not Allowed: 
```json
Status: 405 METHOD NOT ALLOWED
Content-Type: application/json

{
  "success": False,
  "error": 405,
  "message": "method not allowed"
}
```

* 422 Unprocessable: 
```json
Status: 422 UNPROCESSABLE
Content-Type: application/json

{
  "success": False,
  "error": 422,
  "message": "unprocessable"
}
```

* 500 Internal Server Error: 
```json
Status: 500 INTERNAL SERVER ERROR
Content-Type: application/json

{
  "success": False,
  "error": 500,
  "message": "internal server error"
}
```

## Authentication and Authorization

Users of the API can have essentially two roles: `regular users` or `admins`. Admin users have the capability to perform all available operations in the API:

* `get:companies`	
* `post:companies`	
* `patch:companies`	
* `delete:companies`

* `get:partners`	
* `post:partners`	
* `patch:partners`	
* `delete:partners`

* `put:partners`

* `post:sanctions`
* `delete:sanctions`	

On the other hand, regular users can only perform listing operations:

* `get:companies`
* `get:partners`

## How to Authenticate

To authenticate, you need to access the following URL:

> https://dev-g8ovzwsj4zhype80.us.auth0.com/authorize?audience=capstone_project&response_type=token&client_id=eey3gtpCSFr6k1CjO7KrFTrovMogVTiJ&redirect_uri=https://jvguinelli-service.onrender.com/show_created_token

Login information were sent in the submission page.

* Admin User:

``` 
e-mail: admin_capstone@gmail.com
password: 123#capstone
```

* Regular User:

``` 
e-mail: regular_capstone@gmail.com
password: 123#capstone
```

Copy the token and use it to test the API.