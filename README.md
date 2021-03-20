# Django_Rest_Api

Example project of API interacting with MongoDB. 

API was created using Django which is runned by uWSGI.
UWSGI application server is shared with Nginx.

All components run on separate Docker conainters

# Running application

Application runs on heroku at https://example-car-rest-api.herokuapp.com/

Application launching is like any other using docker compose, just build and 'up' the containers.

To run unit tests locally no Django framework is required. Just cd to rest_api and run
python3 -m main.tests

# Endpoints
* POST /cars insert new car in the database:
	* JSON Body example: {	"make": "Ford", "model": "Mustang"}
* GET /cars fetch all cars from the database.
* DELETE /cars/{car_id}/ delete car from the database.
* POST /rate rate a car in range 1 to 5:
	* JSON Body example: {	"car_id": 1, "rating": 3}
* GET /popular fetch all cars from the database sorted
ascending by the number of rates.