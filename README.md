# Internet Scale Applications Main Projects
Tech Micro-Consulting Service
===========================

Our site aims to connect projects with highly specialized professionals who could be hired for small periods of time. These professionals would be able to provide the technical expertise needed to overcome common pitfalls and setup struggles to help a project succeed in the future.

Members of the Team
--------------

  - David Stolz (dps7ud)
  - Brandon Whitfield (bjw4ph)

Project 5 Notes
-------------
- User Stories: User stories can be found in "UserStories_5.txt" in the docs directory.
- Profile Page: Used to see what reviews a user needs to create, as well as create a new listing. It can be reached from the top navbar, but the user must be logged in
- Review Creation: Reviews now able to be created from a modal on the profile page, by clicking the create review button next to a needed review on that page
- Task Creation: Reached through a button on the profile page, or through the navbar, still need to be authenticated to create a task
- Searching: General searching of all fields can be done through the nav bar, you can go to the search page to further narrow down the search to tasks, users, or reviews, and you can further narrow this down by going to advance searching in order to search by specific fields
- Additional Tests created for some helper endpoints in the models layers

Project 4 Notes
-------------
- User Stories: User stories can be found in "UserStories_4.txt" in the docs directory.
- Create New Listing: Button to reach this page can only be seen after you have logged in on main Task List page, reached by pressing 'Tasks' on the navbar
  -Example Login Credentials: Username: 'user1', Password: 'm'
- Logout Logic: Logout logic on the web app can be reached only when a user has been logged in, once this happens 'Login' on the navbar is replaced by 'Logout' which can be pressed to log the user our
- Testing: testAuth.py created to hold all of the testing for the new Authenticator table, and additional tests were added to testUtility.py, testTask.py, and testUser.py to test some additional helper endpoints added to the model layer

Project 3 Notes
-------------
- Testing: Please ensure the user 'www' is given access to database 'test_cs4501' in the same way as was done in project 1 before running the tests in the models layer
- User Stories: User stories can be found in "UserStories_3.pdf" in the docs directory.
  - Testing for User Story 1 can be primarily found in testUtility.py
  - Testing for User Story 2 can be found in testTask.py
  - Testing for User Story 3 can be found in testUser.py
  - Testing for User Story 4 can be found in testReview.py
  - Testing for User Story 5 completed by checking functionality on the web layer

Models Layer Endpoints
-------------

  - /api/v1/review/info/(review_id)/
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
      
- /api/v1/user/info/(user_id)/
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
- getUserRating/(user_id)
  - GET: Returns the average score for a user with id of user_id
    - Example Response:
    ```python
    { "score": 5.0}
    ```
- topUsers/
  - GET: Returns a list of 5 User model instances which correspond to the users with the highest average rating.

- recentListings/
  - GET: Returns a list of 5 Task model instances which corrsepond to the tasks which have been posted most recently

- Other Model Layer Helper functions (Only accept GET requests)
  - api/v1/taskSkills/(task_id) : Returns a list filled with TaskSkills objects for all of the skills needed for task with task_id
  - api/v1/taskOwners/(task_id) : Return a list of User models which correspond to the owners of the task with task_id
  - api/v1/taskWorkers/(task_id) : Return a list of User models which correspond to the workers on the task with task_id
  - api/v1/taskReviews/(task_id) : Return a list of Review models which correspond to reviews for the task with task_id
  - api/v1/userLanguages/(user_id) : Return a list of UserLanguages models which correspond to the languages known by the user with user_id
  - api/v1/userSkills/(user_id) : Return a list of UserSkills models which correspond to the skills of the user with user_id
  - api/v1/userOwnerTasks/(user_id) : Return a list of Task models which correspond to the task which the user with user_id owns
  - api/v1/userWorkerTasks/(user_id) : Return a list of Task models which correspond to the task which the user with user_id has worked on
  - api/v1/userReviews/(user_id) : Return a list of Review models which correspond to the reviews which the user with user_id has created
  - api/v1/userReviewed/(user_id) : Return a list of Review models which correspond to the reviews where the user with user_id is the subject
  
Experience Layer Endpoints
-------------
All endpoints on the experience layer only accepts GET requests at this point
- home/
  - Calls to Model Layer
    - topUsers/
    - recentListings/
  - Returns:  List containing [response from topUsers, response from recentListings, combination of any error string from the calls above]

- review/(review_id)
  - Calls to Model Layer
    1. api/v1/review/(review_id)/
    2. api/v1/user/(Review.postee_user)
    3. api/v1/user/(Review.poster_user)
    4. api/v1/task/info/(Review.task)
  - Returns: List containing [response from call a, response from call b, response from call c, response from call d, error strings]

- user/(user_id)
  - Calls to Model Layer
    1. api/v1/user/(user_id)
    2. api/v1/userLanguages/(user_id)
    3. api/v1/userSkills/(user_id)
    4. api/v1/userOwnerTasks/(user_id)
    5. api/v1/userWorkerTasks/(user_id)
    6. api/v1/userReviews/(user_id)
    7. api/v1/userReviewed/(user_id)
  - Returns: List containing [response from call a, response from call b, response from call c, response from call d, response from call e, response from call f, response from call g, error strings]

- task/(task_id)
  - Calls to Model Layer
    1. api/v1/task/info/(task_id)
    2. api/v1/taskOwners/(task_id)
    3. api/v1/taskWorkers/(task_id)
    4. api/v1/taskSkills/(task_id)
    5. api/v1/taskReviews/(task_id)
  - Returns: List containing [response from call a, response from call b, response from call c, response from call d, response from call e, error strings]

Web Layer Endpoints
-------------
All web layer endpoints correspond to the experience layer endpoints and calls that part of the API when invoked
