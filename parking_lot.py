from random import randrange
from typing import List, Tuple
import pytest


class ParkingLot:
    """
    Represents a row of a parking lot. The individual spots are designated to
    hold one of a car, a motorcycle, or a van. A motorcycle may fit in any
    type of spot; a car may fit in a car or van spot, and a van may fit in
    a van spot or three contiguous car spots.

    Methods are provided to park vehicles, unpark vehicles, count remaining spaces,
    determine whether the lot is full, and count how much space vans are taking.
    """

    def __init__(self, count: int = 20):
        self.total_spots = count
        """
        Each of following will hold the ids of parking spots, so for instance
        a van spot will be in either `open_van_spots` or `full_van_spots`, and
        will move back and forth depending on whether it's in use or not.
        """
        self.open_car_spots: set[int] = set()
        self.full_car_spots: set[int] = set()
        self.open_van_spots: set[int] = set()
        self.full_van_spots: set[int] = set()
        self.open_motorcycle_spots: set[int] = set()
        self.full_motorcycle_spots: set[int] = set()
        self.vans_in_car_spots: set[int] = set()
        self.create_random_lot()

    def create_random_lot(self):
        """
        Create a lot with a random assortment of motorcycle, car, and van spots.
        """
        for i in range(self.total_spots):
            which = randrange(3)
            if which == 0:
                self.open_motorcycle_spots.add(i)
            elif which == 1:
                self.open_car_spots.add(i)
            else:
                self.open_van_spots.add(i)

    def to_list(self) -> List[str]:
        """
        Return list representation of the types of spaces in a parking lot and
        whether each is full. Each item is of form "car:full", "car:open", etc.
        If three car spots have a van in them they will all be represented as
        "car:full", not as "van:full".
        """
        res = ["car" for _ in range(self.total_spots)]
        for spot_set in [
            self.open_car_spots,
            self.full_car_spots,
            self.open_van_spots,
            self.full_van_spots,
            self.open_motorcycle_spots,
            self.full_motorcycle_spots,
            self.vans_in_car_spots,
        ]:
            for spot in spot_set:
                if spot_set is self.open_car_spots:
                    res[spot] = "car:open"
                elif spot_set is self.full_car_spots:
                    res[spot] = "car:full"
                elif spot_set is self.open_motorcycle_spots:
                    res[spot] = "motorcycle:open"
                elif spot_set is self.full_motorcycle_spots:
                    res[spot] = "motorcycle:full"
                elif spot_set is self.open_van_spots:
                    res[spot] = "van:open"
                elif spot_set is self.full_van_spots:
                    res[spot] = "van:full"
                elif spot_set is self.vans_in_car_spots:
                    res[spot] = "car:full"
                    res[spot - 1] = "car:full"
                    res[spot + 1] = "car:full"
        return res

    def set_spot(self, spot_number: int, vehicle_type: str) -> None:
        """
        For spot_number, set as a given vehicle type. This method is provided
        for testing, is not safe once any vehicles have been parked, and
        should only be used for test initialization.
        """

        # First, discard from all three sets, then add to correct set.
        self.open_motorcycle_spots.discard(spot_number)
        self.open_car_spots.discard(spot_number)
        self.open_van_spots.discard(spot_number)
        if vehicle_type == "motorcycle":
            self.open_motorcycle_spots.add(spot_number)
        elif vehicle_type == "car":
            self.open_car_spots.add(spot_number)
        else:
            self.open_van_spots.add(spot_number)

    def is_full(self) -> bool:
        """
        Return True if lot is full, False otherwise. Not this does not mean there
        is space for a van or a car, as for instance, only a single motorcycle
        spot might be available.
        """
        return (
            len(self.open_motorcycle_spots)
            + len(self.open_car_spots)
            + len(self.open_van_spots)
            == 0
        )

    def how_many_remain(self) -> Tuple[int, int, int]:
        """Return a tuple of remaining open spots: (motorcycle, car, van)."""
        return (
            len(self.open_motorcycle_spots),
            len(self.open_car_spots),
            len(self.open_van_spots),
        )

    def how_many_spot_are_vans(self) -> int:
        """Return the total number of spots used by vans."""
        return len(self.vans_in_car_spots) * 3 + len(self.full_van_spots)

    def park(self, type: str) -> int:
        """
        Attempt to park a vehicle (motorcycle, car, or van). If succesful, return
        spot number. Otherwise, return -1.
        """

        # Move a spot from an "open" set to a "full" set. For each incoming
        # vehicle type check for open spots in increasing order of size.

        # Note that, for any given vehicle to be parked, a spot is chosen at random,
        # meaning that vans may be more difficult to park. I believe that currently
        # Python sets are lrus, but choosing from an ordered list might be more
        # efficient.
        if self.is_full():
            return -1

        if type == "motorcycle":
            # Check first for motorcycle spots, then cars spots, then van spots.
            if self.open_motorcycle_spots:
                spot_number = self.open_motorcycle_spots.pop()
                self.full_motorcycle_spots.add(spot_number)
            elif self.open_car_spots:
                spot_number = self.open_car_spots.pop()
                self.full_car_spots.add(spot_number)
            else:
                spot_number = self.open_van_spots.pop()
                self.full_van_spots.add(spot_number)
            return spot_number
        elif type == "car":
            # Check first for car spots, then for van spots.
            if self.open_car_spots:
                spot_number = self.open_car_spots.pop()
                self.full_car_spots.add(spot_number)
            else:
                spot_number = self.open_van_spots.pop()
                self.full_van_spots.add(spot_number)
            return spot_number
        else:
            # It's a van. Look for van spots, if not available try for three
            # car spots.
            if self.open_van_spots:
                spot_number = self.open_van_spots.pop()
                self.full_van_spots.add(spot_number)
            elif len(self.open_car_spots) > 2:
                for spot_number in self.open_car_spots:
                    if (
                        spot_number - 1 in self.open_car_spots
                        and spot_number + 1 in self.open_car_spots
                    ):
                        self.vans_in_car_spots.add(spot_number)
                        for i in range(-1, 2):
                            # Not moving these to full car spots, so
                            # later retrieval will be safer.
                            self.open_car_spots.remove(spot_number + i)
                        break
            else:
                # There were no van spots and not enough car spots.
                return -1
        return spot_number

    def unpark(self, spot_number: int) -> bool:
        """
        Remove the vehicle from a spot. Return True if the spot was taken, False
        otherwise. Only a boolean is returned because the type of vehicle in a
        given spot has not been tracked.
        """
        if spot_number in self.full_motorcycle_spots:
            self.full_motorcycle_spots.remove(spot_number)
            self.open_motorcycle_spots.add(spot_number)
            return True
        if spot_number in self.full_car_spots:
            self.full_car_spots.remove(spot_number)
            self.open_car_spots.add(spot_number)
            return True
        if spot_number in self.full_van_spots:
            self.full_van_spots.remove(spot_number)
            self.open_van_spots.add(spot_number)
            return True
        if spot_number in self.vans_in_car_spots:
            self.vans_in_car_spots.remove(spot_number)
            for i in range(-1, 2):
                # These were only removed from open, not put anywhere else.
                self.open_car_spots.add(spot_number + i)
            return True
        return False


def test_set_and_to_list():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_spot(i, "car")
    lot.set_spot(3, "motorcycle")
    # Check it works
    assert lot.to_list() == [
        "car:open",
        "car:open",
        "car:open",
        "motorcycle:open",
        "car:open",
    ]


def test_park_motorcycle():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_spot(i, "car")
    lot.set_spot(3, "motorcycle")
    # Check it works
    lot.park("motorcycle")
    assert lot.to_list() == [
        "car:open",
        "car:open",
        "car:open",
        "motorcycle:full",
        "car:open",
    ]
    # First, force into car spot.
    lot.park("motorcycle")
    assert lot.to_list() == [
        "car:full",
        "car:open",
        "car:open",
        "motorcycle:full",
        "car:open",
    ]
    # Now, force into van spot.
    lot.unpark(0)
    assert lot.to_list() == [
        "car:open",
        "car:open",
        "car:open",
        "motorcycle:full",
        "car:open",
    ]
    lot.set_spot(0, "van")
    lot.set_spot(1, "van")
    lot.set_spot(4, "van")
    assert lot.to_list() == [
        "van:open",
        "van:open",
        "car:open",
        "motorcycle:full",
        "van:open",
    ]
    lot.park("motorcycle")
    lot.park("motorcycle")
    assert lot.to_list() == [
        "van:full",
        "van:open",
        "car:full",
        "motorcycle:full",
        "van:open",
    ]


def test_park_van():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_spot(i, "car")
    lot.set_spot(3, "van")
    # Check it works
    lot.park("van")
    assert lot.to_list() == ["car:open", "car:open", "car:open", "van:full", "car:open"]
    # First, force into motorcycle spot.
    lot.park("van")
    assert lot.to_list() == ["car:full", "car:full", "car:full", "van:full", "car:open"]


def test_unpark_van_taking_three_spots():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_spot(i, "car")
    # Check that parking a van works.
    van_spot = lot.park("van")
    assert lot.to_list() == ["car:full", "car:full", "car:full", "car:open", "car:open"]
    # Now, unpark it.
    lot.unpark(van_spot)
    assert lot.to_list() == ["car:open", "car:open", "car:open", "car:open", "car:open"]


def test_how_many_remain():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_spot(i, "car")
    lot.set_spot(3, "motorcycle")
    # Check it works
    lot.park("motorcycle")
    assert lot.how_many_remain() == (0, 4, 0)
    # First, force into car spot.
    lot.park("motorcycle")
    assert lot.how_many_remain() == (0, 3, 0)  # Now, force into van spot.
    lot.unpark(0)
    assert lot.how_many_remain() == (0, 4, 0)
    spot = lot.park("van")
    assert lot.how_many_remain() == (0, 1, 0)
    lot.unpark(spot)
    assert lot.how_many_remain() == (0, 4, 0)


def test_how_many_spot_are_vans():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_spot(i, "car")
    lot.set_spot(3, "motorcycle")
    # Check it works
    lot.park("motorcycle")
    assert lot.how_many_spot_are_vans() == 0
    # First, force into car spot.
    lot.park("motorcycle")
    assert lot.how_many_spot_are_vans() == 0
    lot.unpark(0)
    assert lot.how_many_spot_are_vans() == 0
    lot.park("van")
    assert lot.how_many_spot_are_vans() == 3
    lot.set_spot(4, "van")
    lot.park("van")
    assert lot.how_many_spot_are_vans() == 4
