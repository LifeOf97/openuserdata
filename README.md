[![CI Lint (flake8)](https://github.com/realestKMA/openuserdata/actions/workflows/lint.yml/badge.svg)](https://github.com/realestKMA/openuserdata/actions/workflows/lint.yml)
[![CI Test (pytest)](https://github.com/realestKMA/openuserdata/actions/workflows/test.yml/badge.svg)](https://github.com/realestKMA/openuserdata/actions/workflows/test.yml)


# Open Users Data
### Hello There,

Welcome to *Open users data*. This is a part of the Openuser REST API service. Open users data provides dummy user data over [REST]() API. It's main purpose is to provide an API endpoint where developers can practice [CRUD]() operations, Authentication/Authorization, and more over REST API.

## Features
#
- Retrieve all users in the system. **paginated**
  > NOTE: The result is paginated with a default of 50 users returned. this can be change using the **limit/offset** url query parameters to return more or less users, depending on your use case.
- Retrieve a particular user via *username*.
- Retrieve a subset of users via one of [this]() url query parameters.
- Retrieve all users belonging to a creators app instance in the system.
- Retrieve a particular user in a creators app instance via *username*.
- Create a new user in a creators app instance. **(Creators only)**
- Authenticate a user via [*Bearer Authentication*](). uses **JWT**
- Verify a Bearer token. **JWT**
- Refresh a token. **JWT**
- Authenticate a user via [*Session Authetication*]().
- Retrieve data of an authenticated user.
- Update data of an authenticated user.
  > NOTE: User password cannot be updated via REST API, it can only be updated via your creators dashboard. 
- Delete the authenticated user from the system.


## URL Endpoints, Request Methods & Response
#
You are to replace the word *version* with the api version you wish to utilize in the url.cAs of this moment only **v1** is available.

- URL:
  - https://openuserdata.com/
- Methods & Endpoints:

  - **GET**: api/*version*/users/

    Response: 200
    ```JSON
    {
        "count": int,
        "next": url|null,
        "previous": url|null,
        "results": [...]
    }
    ```

  - **GET**: api/*version*/users/*username*/

    The username should be a valid users username provided by you.

    Response:
    - Success: 200
     
      ```JSON
      {
        "uid": string,
        "username": string,
        "email": string|null,
        "first_name": string|null,
        "last_name": string|null,
        "other_name": string|null,
        "mugshot": url|null,
        "gender": string,
        "dob": string|null,
        "about": string|null
      }
      ```
    - Failure: 404
      
      ```JSON
      {
        "detail": "Not found."
      }
      ```

  - **GET**: api/*version*/*cid*/*app_name*/users/

    this is a creators endpoint. **cid** should be your creator id, **app_name** should be the app name you want to query. Make sure the app name belongs to the creator.

    Response: 
    - Success: 200

      ```JSON
      {
        "count": int,
        "next": url|null,
        "previous": url|null,
        "results": [...]
      }
      ```
    - Failure: 404

      ```JSON
      {
        "detail": "Not found."
      }
      ```
  - **POST**: api/*version*/*cid*/*app_name*/users/app/add/

    Response:
    - Success: 201

      ```JSON
      {
        "app_name": string,
        "uid": string,
        "cid": string,
        "aid": uuid,
        "username": string,
        "email": string|null,
        "first_name": string|null,
        "last_name": string|null,
        "other_name": string|null,
        "mugshot": string|null,
        "gender": string,
        "dob": string|null,
        "about": string|null
      }
      ```

    - Failure: 400
     ```JSON
     {
        "error": "You have reached your open users limit (25)"
     }
     ```
 

UPDATE: Setting up filter, search and order functionality on the users backend

(13-07-2022) Need to update my undergraduate project.
(20-08-2022) Back to clontinue