# Parking lot project

Design a parking lot API with the following constraints:

1. There are three types of spots, motorcycle, car, and van.
1. A motorcycle can park in any of the spots.
1. A car can park in a car or van space.
1. A van can park in a van space or three contiguous car spaces.

The following API endpoints are required:

1. `/park`, which takes a vehicle type and returns one of
    • an `HTTP_200_OK` with an id on success;
    • `HTTP_??` on failure.
1. `/unpark`, which takes an id number and returns
    • `HTTP_200_OK` on success;
    • `HTTP_??` on failure.
1. `spots-remaining` returns `HTTP_200_OK` and an `int` representing the number of spaces remaining in the lot. (Would a tuple be better here?)
1. `taken-by-vans`  returns `HTTP_200_OK` and an `int` representing the number of spots used by vans (van spots and car spots).
1. `is_full` returns `HTTP_200_OK` and a boolean.

In addition, these endpoints are included, for help with testing.

1. to_list
1. create_random_lot
1. set_spot

### Notes:

A Python script has been included, which provides a better backend data structure, but 
