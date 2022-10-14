[![CI Lint (flake8)](https://github.com/realestKMA/openuserdata/actions/workflows/lint.yml/badge.svg)](https://github.com/realestKMA/openuserdata/actions/workflows/lint.yml)
[![CI Test (pytest)](https://github.com/realestKMA/openuserdata/actions/workflows/test.yml/badge.svg)](https://github.com/realestKMA/openuserdata/actions/workflows/test.yml)
[![CD Deploy (Azure)](https://github.com/realestKMA/openuserdata/actions/workflows/deploy.yml/badge.svg)](https://github.com/realestKMA/openuserdata/actions/workflows/deploy.yml)

### Tool set
![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=plastic&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=plastic&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=plastic&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=plastic&logo=redis&logoColor=white)
![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=plastic&logo=microsoftazure&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=plastic&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=plastic&logo=nginx&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=plastic&logo=rabbitmq&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%230db7ed.svg?style=plastic&logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=plastic&logo=docker&logoColor=white)


# Open Users Data
### Hello There.

Welcome to *Open user data*. This is a part of the Openuser REST API service. Open user data provides dummy user data over [REST API](https://www.redhat.com/en/topics/api/what-is-a-rest-api). It's main purpose is to provide an API endpoint where developers can practice [CRUD](https://www.sumologic.com/glossary/crud/) operations, Authentication/Authorization, and more over REST API.

## Features
- Retrieve all users in the system. **paginated**
  > NOTE: The result is paginated with a default of 50 users returned. this can be change using the **limit/offset** url query parameters to return more or less users, depending on your use case.
- Retrieve a particular user via *username*.
- Retrieve a subset of users via one of [this]() url query parameters.
- Retrieve all users belonging to a creators app instance in the system.
- Retrieve a particular user in a creators app instance via *username*.
- Create a new user in a creators app instance. **(Creators only)**
- [Token Base Authentication](https://www.authgear.com/post/session-vs-token-authentication). uses **JWT**
- Verify a Bearer token. **JWT**
- Refresh a token. **JWT**
- [Session Base Authetication](https://www.authgear.com/post/session-vs-token-authentication).
- Retrieve data of an authenticated user.
- Update data of an authenticated user.
  > NOTE: User password cannot be updated via REST API, it can only be updated via your creators dashboard. 
- Delete the authenticated user from the system.


## URL Endpoints, Request Methods & Response
You are to replace the word **version** with the api version you wish to utilize in the url.cAs of this moment only **v1** is available.

- URL:
  - https://openuserdata.com/
- Methods & Endpoints:

  - **GET**: api/:version/users/
    
    Retrieve all users in the system.

    Response: 200
    ```JSON
    {
        "count": "int",
        "next": "url|null",
        "previous": "url|null",
        "results": ["..."]
    }
    ```

  - **GET**: api/:version/users/:username/

    Get a specific user by their username. The username should be a valid user username provided by you.

    Response:
    - Success: 200
     
      ```JSON
      {
        "uid": "string",
        "username": "string",
        "email": "string|null",
        "first_name": "string|null",
        "last_name": "string|null",
        "other_name": "string|null",
        "mugshot": "url|null",
        "gender": "Male|Female|Undefined",
        "dob": "string|null",
        "about": "string|null"
      }
      ```
    - Failure(s): 404
      
      ```JSON
      {
        "detail": "Not found."
      }
      ```

  - **GET**: api/:version/:cid/:app_name/users/

    Retrieve all users belonging to a particular creator's app instance. **cid** should be your creator id, **app_name** should be the app name you want to query. Make sure the app name belongs to the creator.

    Response: 
    - Success: 200

      ```JSON
      {
        "count": "int",
        "next": "url|null",
        "previous": "url|null",
        "results": ["..."]
      }
      ```
    - Failure(s): 404

      ```JSON
      {
        "detail": "Not found."
      }
      ```
  - **POST**: api/:version/:cid/:app_name/users/app/add/

    Create a new user in a creator's app. Please note the following while creating a new user.
    - the username and email fields should be unique per user as this fields are used to authenticate a user. If an account with the provided username or email address already exist, a 404 response with the appropriate error message will be returned.
    - A password must be provided.
    - Creators have a maximum number of user that can be created per app.

    Request Body:
    > NOTE: Only the username & email fields are required, the rest are optional.
    ```JSON
    {
        "username": "string", //required
        "email": "string|null", //required
        "password": "string", //required
        "first_name": "string|null",
        "last_name": "string|null",
        "other_name": "string|null",
        "mugshot": "string|null",
        "gender": "Male|Female|Undefined",
        "dob": "string|null",
        "about": "string|null"
    }
    ```
    Response:

    - Success: 201
      ```JSON
      {
        "cid": "string",
        "app_name": "string",
        "uid": "string",
        "aid": "uuid",
        "username": "string",
        "email": "string|null",
        "first_name": "string|null",
        "last_name": "string|null",
        "other_name": "string|null",
        "mugshot": "string|null",
        "gender": "Male|Female|Undefined",
        "dob": "string|null",
        "about": "string|null"
      }
      ```

    - Failure(s): 400
      ```JSON
      {
        "error": "You have reached your open users limit (x)"
      }
      ```
      ```JSON
      {
        "username": ["This username is not available"],
      }
      ```
      ```JSON
      {
        "email": ["This email address belongs to another account"],
      }
      ```
      ```JSON
      {
        "password": ["This field is required."],
      }
      ```
    
  - **GET**: api/:version/:cid/:app_name/users/app/i/

    Retrieve the data of the currently authenticated user.

    Response:
    - Success: 200
      ```JSON
      {
        "cid": "string",
        "app_name": "string",
        "uid": "string",
        "aid": "uuid",
        "username": "string",
        "email": "string|null",
        "first_name": "string|null",
        "last_name": "string|null",
        "other_name": "string|null",
        "mugshot": "string|null",
        "gender": "Male|Female|Undefined",
        "dob": "string|null",
        "about": "string|null"
      }
      ```
    
    - Failure(s): 401
      ```JSON
      {
        "detail": "User not found",
        "code": "user_not_found"
      }
      ```

      ```JSON
      {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [
            {
                "token_class": "AccessToken",
                "token_type": "access",
                "message": "Token is invalid or expired"
            }
        ]
      }
      ```

  - **PUT**|**PATCH**: api/:version/:cid/:app_name/users/app/i/update/

    Update the data of the currently authenticated user. Supports both **PUT** & **PATCH** request methods.
    > NOTE: You cannot change the password of any user account via this methods, to do that you will need to login to your creators dashboard and update the password for all users in the specified app instance. You can pass only the fields you wish to update in the request body. The fields **app_name**, **cid**, **uid**, **aid**, **app_name** are read only and should not be provided, it will be ignored if found i the request body.

    Request Body:
    ```JSON
    {
        "username": "string",
        "email": "string|null",
        "first_name": "string|null",
        "last_name": "string|null",
        "other_name": "string|null",
        "mugshot": "string|null",
        "gender": "Male|Female|Undefined",
        "dob": "string|null",
        "about": "string|null"
    }
    ```

    Response:
    - Success: 202

      ```JSON
      {
        "cid": "string",
        "app_name": "string",
        "uid": "string",
        "aid": "uuid",
        "username": "string",
        "email": "string|null",
        "first_name": "string|null",
        "last_name": "string|null",
        "other_name": "string|null",
        "mugshot": "string|null",
        "gender": "Male|Female|Undefined",
        "dob": "string|null",
        "about": "string|null"
      }
      ```
    - Failure(s): 400

      ```JSON
      {
        "gender": ["\"Value\" is not a valid choice."]
      }
      ```
      ```JSON
      {
        "username": ["This username is not available"],
      }
      ```
      ```JSON
      {
        "email": ["This email address belongs to another account"],
      }
      ```

  - **DELETE**: api/:version/:cid/:app_name/users/app/i/delete/

    Delete the currently authenticated user from the system permanently.

    Response:

    - Success: 204

      ```JSON
      {
        "uid": "string",
        "username": "string",
        "app_name": "string",
        "email": "string",
        "detail": "Deleted successfuly"
      }
      ```

    - Failure(s): 401

      ```JSON
      {
        "detail": "User not found",
        "code": "user_not_found"
      }
      ```

      ```JSON
      {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [
            {
                "token_class": "AccessToken",
                "token_type": "access",
                "message": "Token is invalid or expired"
            }
        ]
      }
      ```

  - #### **POST**: api/:version/auth/login/token/

    Authenticate a user via **Token Authentication**. Note, the username field can take a valid username or email address.

    Request Body:

    ```JSON
    {
        "username": "string", //required
        "password": "string" // required
    }
    ```

    Response:

    - Success: 200

      ```JSON
      {
        "refresh": "string",
        "access": "string"
      }
      ```

    - Failure(s): 401, 400

      ```JSON
      {
        "detail": "No active account found with the given credentials"
      }
      ```

      ```JSON
      {
        "username": ["This field is required."]
      }
      ```

      ```JSON
      {
        "password": ["This field is required."]
      }
      ```

  - **POST**: api/:version/auth/refresh/token/

    Use the longer-lived refresh token to obtain another access token. The **refresh** token is gotten from the successful sign in via token response.

    Request Body:

    ```JSON
    {
        "refresh": "string" //required
    }
    ```

    Response: 200

    - Success: 200

      ```JSON
      {
        "access": "string"
      }
      ```

    - Failure(s): 400, 401

      ```JSON
      {
        "refresh": ["This field is required."]
      }
      ```

      ```JSON
      {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
      }
      ```
  
  - **POST**: api/:version/auth/verify/token/

    Verify the authenticity of a token.

    Request Body:

    ```JSON
    {
        "token": "string" // required
    }
    ```

    Response:

    - Success: 200

      ```JSON
      {}
      ```

    - Failure(s): 400, 401
      
      ```JSON
      {
        "token": ["This field is required."]
      }
      ```

      ```JSON
      {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
      }
      ```
  
  - **POST**: api/:version/auth/login/session/

    Authenticate a user via **Session Authentication**. Note, the username field can take a valid username or email address.
  
    Request Body:

    ```JSON
    {
        "username": "string", //required
        "password": "string" // required
    }
    ```

    Response: 

    - Success: 200

      ```JSON
      {
        "detail": "Logged in successfully"
      }
      ```

    - Failure(s): 400

      ```JSON
      {
        "detail": "wrong username/email or password"
      }
      ```

  - **POST**: api/:version/auth/logout/session/

    Logout a user session.
    > NOTE: You need to make sure you include a valid X-CSRFToken token for any "unsafe" HTTP method calls in the request header, such as **PUT**, **PATCH**, **POST** or **DELETE** requests.

    Response:

    - Success: 200

      ```JSON
      {
        "detail": "Logged out successfully"
      }
      ```

    - Failure(s): 401, 403

      ```JSON
      {
        "detail": "Authentication credentials were not provided."
      }
      ```

      ```JSON
      {
        "detail": "CSRF Failed: CSRF token missing."
      }
      ```

      ```JSON
      {
        "detail": "CSRF Failed: CSRF token from the 'X-Csrftoken' HTTP header incorrect."
      }
      ```

## About Authentication
Open user data provides both **Session Base** & **Token Base** authentication for you to use and learn. Any **user data** can be used to authenticate by users of open user data, however to update or delete an account you need to make request to the appropriate endpoint of the creator who owns this user you are authenticated as.

### **Token Based Authentication**

Open user data uses *JWT (JSON WEB TOKEN)* for it's token based authentication. Once you make a **POST** request with a valid username/email & password to this endpoint 

```BASH
POST: https://openuserdata.com/api/v1/auth/login/token/
```

a refresh and access token will be sent back as response. The **access** token should then be used to authenticate further requests to endpoints that requires authentication/authorization. This **access** token should be passed in the **Authorization** request header as a **Bearer** token:

```BASH
Authorization="Bearer access-token-hereXYZ"
```

Please note the following:

- The lifetime of an **access** token is 2 hours.
- The lifetime of an **refresh** token is 4 hours.
- The Authorization header keyword is **Bearer**.


### **Session Based Authentication**

Session based authentication keeps authentication details in the form of cookies. Once you make a **POST** request with a valid username/email & password to this endpoint

```BASH
POST: https://openuserdata.com/api/v1/auth/login/session/
```

a sessionid is then added to the response cookies which is then sent back and forth on every request so the server can verify the user making the request.

> NOTE: You need to make sure you include a valid X-CSRFToken token for any "unsafe" HTTP method calls in the request header, such as **PUT**, **PATCH**, **POST** or **DELETE** requests. The csrftoken is found in the cookies.


## About URL Query parameters

Open user data provides  the following features that requires url query params.

### Pagination
Open user data includes support for customizable pagination styles. With these, you can modify how result set are split into pages. Pagination links are provided as part of the content of the response.

Open user data uses the [LimitOffsetPagination](https://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination).

> Django-rest-framework: "This pagination style mirrors the syntax used when looking up multiple database records. The client includes both a "limit" and an "offset" query parameter. The limit indicates the maximum number of items to return, and is equivalent to the page_size in other styles. The offset indicates the starting position of the query in relation to the complete set of unpaginated items."

Request:

```BASH
GET https://openuserdata.com/api/v1/?limit=100&offset=400
```

Response:

```JSON
{
    "count": 10000,
    "next": "https://openuserdata.com/api/v1/?limit=100&offset=500",
    "previous": "https://openuserdata.com/api/v1/?limit=100&offset=300",
    "results": ["..."]
}
```

The default number of data retrurned is **50**, offcourse you can change this to suit your needs.


### Filtering
Usually the returned data from any successful request to the backend is the whole object in the database. Sometimes, you'll want to retrieve just a subset of data from the backend. Open user data provides just what you need.

  - Data Filtering

    You can filter based on the following parameters, `username`, `first_name`, `last_name`, `other_name`, `gender`, `dob`, `dob__year`, `dob__year__gt` and `dob__year__lt`. And they can also be appended to each other using the **& ampersand** sign. Note, values are **case insensitive**.

    ```BASH
    GET https://openuserdata.com/api/v1/user?username=john&dob__year_gt=2000
    ```

  - Data Searching

    You can search for a specific data passing any of this values to the search param `username`, `first_name`, `last_name` and `other_name` this values should be an exact match of the user you are searching for. Note, values are **case insensitive**. Open user data uses the keyword **q** for searching.

    ```BASH
    GET https://openuserdata.com/api/v1/user?q=john
    ```

  - Date Ordering

    You can specify in what order you want your returned data to be in. The only supported ordering values are. `username`, `email` and `dob`. Open user data uses the keyword **order** as the url param key to order data.

    ```BASH
    GET https://openuserdata.com/api/v1/user?order=john
    ```


## About Creators

Who are creators in Open user data? creators are users of open user data who have created an account in open user creators. Creators can create applications to hold a maximum number of users. This users can then be retrieved by any other user when making a request to the public users endpoint.

```BASH
GET https://openuserdata.com/api/v1/users/
GET https://openuserdata.com/api/v1/users/<username>/
```

Creators have application instances which users are created under that application. Creators have their specific enpoints to make request to, this endpoints can be shared with others.

```BASH
GET https://openuserdata.com/api/v1/<cid>/<app_name>/users/
GET https://openuserdata.com/api/v1/<cid>/<app_name>/users/<username>/
GET https://openuserdata.com/api/v1/<cid>/<app_name>/users/app/i/
POST https://openuserdata.com/api/v1/<cid>/<app_name>/users/app/add/
PUT https://openuserdata.com/api/v1/<cid>/<app_name>/users/app/i/update/
PATCH https://openuserdata.com/api/v1/<cid>/<app_name>/users/app/i/update/
DELETE https://openuserdata.com/api/v1/<cid>/<app_name>/users/app/i/delete/
```

But remember certain endpoints requires authentication.

As a creator:

- You get your own specific endpoint.
- You can increase & decrease bulk user at once.
- You can update the password of all users in an application.
  > NOTE: All users in an application must share the same password.

#
Will keep updating this README file as changes occures. Thank you.