from random import randrange
from typing import List, Tuple
import pytest


class ParkingLot:
    """
    Represents a row of a parking lot. The individual spaces are designated to
    hold one of a car, a motorcycle, or a van. A motorcycle may fit in any
    type of space; a car may fit in a car or van space, and a van may fit in
    a van space or three contiguous car spaces.

    Methods are provided to park vehicles, unpark vehicles, count remaining spaces,
    determine whether the lot is full, and count how much space vans are taking.
    """

    def __init__(self, count: int = 20):
        self.total_spaces = count
        """
        Each of following will hold the ids of parking spaces, so for instance
        a van space will be in either `open_van_spaces` or `full_van_spaces`, and
        will move back and forth depending on whether it's in use or not.
        """
        self.open_car_spaces: set[int] = set()
        self.full_car_spaces: set[int] = set()
        self.open_van_spaces: set[int] = set()
        self.full_van_spaces: set[int] = set()
        self.open_motorcycle_spaces: set[int] = set()
        self.full_motorcycle_spaces: set[int] = set()
        self.vans_in_car_spaces: set[int] = set()
        self.create_random_lot()

    def create_random_lot(self):
        """
        Create a lot with a random assortment of motorcycle, car, and van spaces.
        """
        for i in range(self.total_spaces):
            which = randrange(3)
            if which == 0:
                self.open_motorcycle_spaces.add(i)
            elif which == 1:
                self.open_car_spaces.add(i)
            else:
                self.open_van_spaces.add(i)

    def to_list(self) -> List[str]:
        """
        Return list representation of the types of spaces in a parking lot and
        whether each is full. Each item is of form "car:full", "car:open", etc.
        If three car spaces have a van in them they will all be represented as
        "car:full", not as "van:full".
        """
        res = ["car" for _ in range(self.total_spaces)]
        for space_set in [
            self.open_car_spaces,
            self.full_car_spaces,
            self.open_van_spaces,
            self.full_van_spaces,
            self.open_motorcycle_spaces,
            self.full_motorcycle_spaces,
            self.vans_in_car_spaces,
        ]:
            for space in space_set:
                if space_set is self.open_car_spaces:
                    res[space] = "car:open"
                elif space_set is self.full_car_spaces:
                    res[space] = "car:full"
                elif space_set is self.open_motorcycle_spaces:
                    res[space] = "motorcycle:open"
                elif space_set is self.full_motorcycle_spaces:
                    res[space] = "motorcycle:full"
                elif space_set is self.open_van_spaces:
                    res[space] = "van:open"
                elif space_set is self.full_van_spaces:
                    res[space] = "van:full"
                elif space_set is self.vans_in_car_spaces:
                    res[space] = "car:full"
                    res[space - 1] = "car:full"
                    res[space + 1] = "car:full"
        return res

    def set_space(self, space_number: int, vehicle_type: str) -> None:
        """
        For space_number, set as a given vehicle type. This method is provided
        for testing, is not safe once any vehicles have been parked, and
        should only be used for test initialization.
        """

        # First, discard from all three sets, then add to correct set.
        self.open_motorcycle_spaces.discard(space_number)
        self.open_car_spaces.discard(space_number)
        self.open_van_spaces.discard(space_number)
        if vehicle_type == "motorcycle":
            self.open_motorcycle_spaces.add(space_number)
        elif vehicle_type == "car":
            self.open_car_spaces.add(space_number)
        else:
            self.open_van_spaces.add(space_number)

    def is_full(self) -> bool:
        """
        Return True if lot is full, False otherwise. Not this does not mean there
        is space for a van or a car, as for instance, only a single motorcycle
        space might be available.
        """
        return (
            len(self.open_motorcycle_spaces)
            + len(self.open_car_spaces)
            + len(self.open_van_spaces)
            == 0
        )

    def how_many_remain(self) -> Tuple[int, int, int]:
        """Return a tuple of remaining open spaces: (motorcycle, car, van)."""
        return (
            len(self.open_motorcycle_spaces),
            len(self.open_car_spaces),
            len(self.open_van_spaces),
        )

    def how_many_space_are_vans(self) -> int:
        """Return the total number of spaces used by vans."""
        return len(self.vans_in_car_spaces) * 3 + len(self.full_van_spaces)

    def park(self, type: str) -> int:
        """
        Attempt to park a vehicle (motorcycle, car, or van). If succesful, return
        space number. Otherwise, return -1.
        """

        # Move a space from an "open" set to a "full" set. For each incoming
        # vehicle type check for open spaces in increasing order of size.

        # Note that, for any given vehicle to be parked, a space is chosen at random,
        # meaning that vans may be more difficult to park. I believe that currently
        # Python sets are lrus, but choosing from an ordered list might be more
        # efficient.
        if self.is_full():
            return -1

        if type == "motorcycle":
            # Check first for motorcycle spaces, then cars spaces, then van spaces.
            if self.open_motorcycle_spaces:
                space_number = self.open_motorcycle_spaces.pop()
                self.full_motorcycle_spaces.add(space_number)
            elif self.open_car_spaces:
                space_number = self.open_car_spaces.pop()
                self.full_car_spaces.add(space_number)
            else:
                space_number = self.open_van_spaces.pop()
                self.full_van_spaces.add(space_number)
            return space_number
        elif type == "car":
            # Check first for car spaces, then for van spaces.
            if self.open_car_spaces:
                space_number = self.open_car_spaces.pop()
                self.full_car_spaces.add(space_number)
            else:
                space_number = self.open_van_spaces.pop()
                self.full_van_spaces.add(space_number)
            return space_number
        else:
            # It's a van. Look for van spaces, if not available try for three
            # car spaces.
            if self.open_van_spaces:
                space_number = self.open_van_spaces.pop()
                self.full_van_spaces.add(space_number)
            elif len(self.open_car_spaces) > 2:
                for space_number in self.open_car_spaces:
                    if (
                        space_number - 1 in self.open_car_spaces
                        and space_number + 1 in self.open_car_spaces
                    ):
                        self.vans_in_car_spaces.add(space_number)
                        for i in range(-1, 2):
                            # Not moving these to full car spaces, so
                            # later retrieval will be safer.
                            self.open_car_spaces.remove(space_number + i)
                        break
            else:
                # There were no van spaces and not enough car spaces.
                return -1
        return space_number

    def unpark(self, space_number: int) -> bool:
        """
        Remove the vehicle from a space. Return True if the space was taken, False
        otherwise. Only a boolean is returned because the type of vehicle in a
        given space has not been tracked.
        """
        if space_number in self.full_motorcycle_spaces:
            self.full_motorcycle_spaces.remove(space_number)
            self.open_motorcycle_spaces.add(space_number)
            return True
        if space_number in self.full_car_spaces:
            self.full_car_spaces.remove(space_number)
            self.open_car_spaces.add(space_number)
            return True
        if space_number in self.full_van_spaces:
            self.full_van_spaces.remove(space_number)
            self.open_van_spaces.add(space_number)
            return True
        if space_number in self.vans_in_car_spaces:
            self.vans_in_car_spaces.remove(space_number)
            for i in range(-1, 2):
                # These were only removed from open, not put anywhere else.
                self.open_car_spaces.add(space_number + i)
            return True
        return False


def test_set_and_to_list():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_space(i, "car")
    lot.set_space(3, "motorcycle")
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
        lot.set_space(i, "car")
    lot.set_space(3, "motorcycle")
    # Check it works
    lot.park("motorcycle")
    assert lot.to_list() == [
        "car:open",
        "car:open",
        "car:open",
        "motorcycle:full",
        "car:open",
    ]
    # First, force into car space.
    lot.park("motorcycle")
    assert lot.to_list() == [
        "car:full",
        "car:open",
        "car:open",
        "motorcycle:full",
        "car:open",
    ]
    # Now, force into van space.
    lot.unpark(0)
    assert lot.to_list() == [
        "car:open",
        "car:open",
        "car:open",
        "motorcycle:full",
        "car:open",
    ]
    lot.set_space(0, "van")
    lot.set_space(1, "van")
    lot.set_space(4, "van")
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
        lot.set_space(i, "car")
    lot.set_space(3, "van")
    # Check it works
    lot.park("van")
    assert lot.to_list() == ["car:open", "car:open", "car:open", "van:full", "car:open"]
    # First, force into motorcycle space.
    lot.park("van")
    assert lot.to_list() == ["car:full", "car:full", "car:full", "van:full", "car:open"]


def test_unpark_van_taking_three_spaces():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_space(i, "car")
    # Check that parking a van works.
    van_space = lot.park("van")
    assert lot.to_list() == ["car:full", "car:full", "car:full", "car:open", "car:open"]
    # Now, unpark it.
    lot.unpark(van_space)
    assert lot.to_list() == ["car:open", "car:open", "car:open", "car:open", "car:open"]


def test_how_many_remain():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_space(i, "car")
    lot.set_space(3, "motorcycle")
    # Check it works
    lot.park("motorcycle")
    assert lot.how_many_remain() == (0, 4, 0)
    # First, force into car space.
    lot.park("motorcycle")
    assert lot.how_many_remain() == (0, 3, 0)  # Now, force into van space.
    lot.unpark(0)
    assert lot.how_many_remain() == (0, 4, 0)
    space = lot.park("van")
    assert lot.how_many_remain() == (0, 1, 0)
    lot.unpark(space)
    assert lot.how_many_remain() == (0, 4, 0)


def test_how_many_space_are_vans():
    lot = ParkingLot(5)
    for i in range(5):
        lot.set_space(i, "car")
    lot.set_space(3, "motorcycle")
    # Check it works
    lot.park("motorcycle")
    assert lot.how_many_space_are_vans() == 0
    # First, force into car space.
    lot.park("motorcycle")
    assert lot.how_many_space_are_vans() == 0
    lot.unpark(0)
    assert lot.how_many_space_are_vans() == 0
    lot.park("van")
    assert lot.how_many_space_are_vans() == 3
    lot.set_space(4, "van")
    lot.park("van")
    assert lot.how_many_space_are_vans() == 4
