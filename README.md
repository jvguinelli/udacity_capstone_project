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
pip install -r requirements.txt
```

7. From within the `./capstone_project` folder, run:

```bash
export FLASK_APP=src;
```

8. To run the server, execute:

```bash
flask run --reload
```

## API

Base URL: `https://jvguinelli-service.onrender.com`

## Authentication

## Endpoints

### List Companies

Endpoint: `/companies`

Method: `GET`

Description: Retrieves a list of all all companies in the database.

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
      "fiscal_number": "53846386956648",
      "name": "ABC INDUSTRY", 
      "partners": [
        { 
          "id": 2,
          "document": "14235717343", 
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

Description: Retrieves a list of all all partners in the database.

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

Description: Update information about a company in the database.

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