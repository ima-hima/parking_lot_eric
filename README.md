# Parking lot project

#### Design a parking lot API 

##### Constraints

1. There are three types of spots, motorcycle, car, and van.
1. A motorcycle can park in any of the spots.
1. A car can park in a car or van space.
1. A van can park in a van space or three contiguous car spaces.

##### Required API endpoints

1. `park`, which takes a vehicle type and returns
    • On success, an integer that represents the id of the parked car's spot (for later retrieval);
    • On failure (if not enough spaces are available) -1.
1. `unpark`, which takes an id number and returns
    • On success, True;
    • On failure (if the id is for some reason invalid), False.
1. `spots-remaining` returns an `int` representing the number of spaces remaining in the lot. (Would a tuple be better here?)
1. `used-by-vans` returns an integer representing the number of spots used by vans (both van spots and car spots).
1. `is-full` returns a boolean.

In addition, these endpoints are included, for help with testing.

1. `to-list`
1. `set-spot` allows the user to set a vehicle type for a specific space.

##### Design choices

1. I decided to use foreign tables to track the status of a given spot and to mark the type of spot it is. That better guarantees that accurate information is kept, rather than simply having a text field, which would have been simpler.
1. A van takes up three contiguous spaces. I elected to simply use the ids of the parking places to determine whether spaces are abutting. Rows can't be removed from the `parking`place` table, and `id`s are never changed, so that shouldn't be a problem.
1. A parking place can be in one of three possible status states, `Empty`, `Adjacent`, and `Full`. Both `Adjacent` and `Full` spaces are taken, but `Full` spaces have a vehicle directly in them, whereas `Adjacent` spots are in use by a vehicle in an adjacent spot. That ensures that a car or motorcycle can't be put in a spot taken by a van, and it also means 
1. A Python script has been included. I wrote that as a quick template, and for a non-web app it provides a better data structure, but I'm not familiar with a way to use a web framework like Django or Flask with such a simple data store, so I recreated its functionality in PostgreSQL.
1. Although Flask is lighter-weight and might have been a better choice, I used Django as I haven't used Flask in a while, and I recently built a project using Django REST Framework.
1. I proved a Docker image because I had one available that was good for this project.
1. Note that, when any given vehicle is parked a space is chosen at random, meaning that over time vans may become more difficult to park, as there might be three spaces available, but not contiguously. This could be fixed with a reshuffling function, but I decided that was beyond the scope of this project.
