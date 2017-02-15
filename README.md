# Internet Scale Applications Main Projects
Tech Micro-Consulting Service
===========================

Our site aims to connect projects with highly specialized professionals who could be hired for small periods of time. These professionals would be able to provide the technical expertise needed to overcome common pitfalls and setup struggles to help a project succeed in the future.

Members of the Team
--------------

  - David Stolz (dps7ud)
  - Matthew Tillman (mst2jd)
  - Brandon Whitfield (bjw4ph)

API Service Endpoints
-------------

  - /api/v1/review/(review_id)/
    - Used to retrieve or update a review which is already created
    - GET: Returns information for the review with a primary key of review_id if it exists, and return an error otherwise
    - POST: Updates fields specified in the body of the request for the review with a primary key of review_id or creates a new instance in the database if that review doesn't exist
      - Body of Request: Required, should be in json form
  - /api/v1/review/create/
    - POST: Used to create a new database review entry, using the information specified in the body of request
      - Body of Request: Required, Should be in json format
