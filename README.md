# Internet Scale Applications Main Projects
Tech Micro-Consulting Service
===========================

Our site aims to connect projects with highly specialized professionals who could be hired for small periods of time. These professionals would be able to provide the technical expertise needed to overcome common pitfalls and setup struggles to help a project succeed in the future.

Members of the Team
--------------

  - David Stolz (dps7ud)
  - Matthew Tillman (mst2jd)
  - Brandon Whitfield (bjw4ph)

Models Layer Endpoints
-------------

  - /api/v1/review/(review_id)/
    - Used to retrieve or update a review which is already created
    - GET: Returns information for the review with a primary key of review_id if it exists, and return an error otherwise
    - POST: Updates fields specified using form encoded key-value pairs in the POST body
      - Body of POST request example:
      ```python
      {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 4,
                "poster_user": 2,
                "postee_user": 3
       }
       ```
    - DELETE: Deletes task with id of review_id, and returns an error otherwise  
      

  - /api/v1/review/create/
    - POST: Used to create a new database review entry, using the information specified as a form encoded key-value pairs in the POST body
      - Body of POST request example:
      ```python
      {
                "title": "1",
                "body": "2",
                "score": 3,
                "task": 4,
                "poster_user": 2,
                "postee_user": 3
       }
       ```
      
- /api/v1/user/(user_id)/
    - Used to retrieve, update, and delete a user which is already created
    - GET: Returns information for the user with a primary key of user_id if it exists, and return an error otherwise
    - POST: Updates fields specified in the body of the request for the user with a primary key of user_id, and returns an error otherwise
      - Body of POST request example:
      ```python
      {
            "fname": "New",
            "lname": "Name",
            "email": "new@gmail.com",
            "bio": "I make changes",
            "pw": "secret",
            "location": "Virginia"
       }
       ```
      
    - DELETE: Delete user with the id user_id

- /api/v1/user/create/
  - POST: Used to create a new database user entry, using the information specified as a form encoded key-value pairs in the POST body
    - Body of POST request example:
    ```python
    {
          "fname": "New",
          "lname": "Name",
          "email": "new@gmail.com",
          "bio": "I make changes",
          "pw": "secret",
          "location": "Virginia"
     }
     ```

- api/v1/task/info/(task_id)/$
    - Used to retrieve, update, and delete task entries which are already created
    - GET: Returns fields of task model with a primary key of task_id if it exists in json format, and returns an error otherwise
    - POST: Updates fields specified in the body of the request for the task with a primary key of task_id, and returns an error otherwise
       - Body of POST request example:
       ```python
       {
          "pricing_info":0.0,
          "location":"where",
          "time_to_live":"2017-02-15", 
          "title":"A hard task", 
          "description":"It is super hard", 
          "post_date":"2017-02-15", 
          "status":"OPEN", 
          "time":"5",
          "remote":False, 
          "pricing_type":True,
      }
      ```
    - DELETE: Deletes task with id of task_id, and returns an error otherwise

- api/v1/task/create/
    - POST: Used to create a new database task entry, using the information specified as a form encoded key-value pairs in the POST body
      - Body of POST request example:
      ```python
       {
          "pricing_info":0.0,
          "location":"where",
          "time_to_live":"2017-02-15", 
          "title":"A hard task", 
          "description":"It is super hard", 
          "post_date":"2017-02-15", 
          "status":"OPEN", 
          "time":"5",
          "remote":False, 
          "pricing_type":True,
      }
      ```
