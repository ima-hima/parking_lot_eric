oo# Parking lot project

#### Design a parking lot API 

##### Constraints

1. There are three types of spots, motorcycle, car, and van.
1. A motorcycle can park in any of the spots.
1. A car can park in a car or van space.
1. A van can park in a van space or three contiguous car spaces.

##### Required API endpoints

1. `park`, which takes a vehicle type and returns
    • on success, an integer that represents the id of the parked car's spot (for later retrieval);
    • on failure (if not enough spaces are available) -1.
1. `unpark`, which takes an id number and returns
    • on success, True;
    • on failure (if the id is for some reason invalid), False.
1. `free` returns an tuple of `int`s (car, motorcycle, van) representing the number of spaces remaining in the lot for each vehicle type.
1. `vans-usage` returns an integer representing the number of spots used by vans (both van spots and car spots).
1. `is-full` returns a boolean.

##### Notes and design choices

1. This project was written in very basic Django with a PostgreSQL data store. 
1. Due to time constraints, I was forced to make some adjustments.
    1. Originally, I had intended to use separate tables for `vehicle type` and `status`, which would better guarantee data integrity, but I decided that using a single table for this use case wasn't limiting and would be much simpler.
    1. I did not use DRF or Swagger, because the quantity of boilerplate code necessary was too much for such a simple project.
1. A van takes up three contiguous spaces. I elected to use the ids of the rows in the table to determine whether spaces are abutting. Rows can't be removed from the `parking_place` table, and `id`s are never changed. Again, for a large problem this might not be the best choice, but parking lots are small and concrete and time was limited.
1. A parking place can be in one of four possible status states, `Empty`, `Adjacent`,  `Full`, and `Van`. `Adjacent`, `Full`, and `Van` spaces are taken. `Full` is straightforward, but the fact that a van can take multiple car spaces posed a problem when unparking. Therefore spaces marked `Van` are car spaces that have a van in them, whereas `Adjacent` spaces are spaces taken by a van in an abutting `Car` space. That ensures that a car or motorcycle can't be put in a spot taken by a van, and it makes it clearer to determine when a van is unparked which spaces should be freed.
1. A Python script has been included. I wrote that as a quick template, and for a non-web app it provides a better data structure, but I'm not aware of a way to use a web framework like Django or Flask with such a simple data store, so I was forced to recreate its functionality using a database table.
1. Although Flask is lighter-weight and might have been a better choice, I used Django as I haven't used Flask in a while, and I recently built a project using Django REST Framework.
1. I provided a Docker image because I had one available that was good for this project.
1. Note that, when any given vehicle is parked a space is chosen at random, meaning that over time vans may become more difficult to park, as there might be three spaces available, but not contiguously. This could be fixed with a reshuffling function, but I decided that was beyond the scope of this project.

##### Running the project

1. `git clone https://github.com/ima-hima/parking_lot_eric.git`
2. A docker image is provided. To use the image, it will need to be built, and an initial database will need to be created:
    1. `docker build .`
    1. `docker compose run --rm app sh -c "python manage.py makemigrations`
    1. `docker compose run --rm app sh -c "python manage.py migrate`
1. On `docker compose up` a parking_place table will be created with five empty car spots in it to allow you to play a (little) bit with the API.  
1. To run the tests, `docker compose run --rm app sh -c "python manage.py test"`.
