# Dice class for the object-oriented game simulator

import random


class Dice:
    """Represents an n-sided dice used to add randomness to the game."""

    def __init__(self, sides: int = 6) -> None:
        """
        Initialise the Dice

        Args:
            sides (int): Number of sides on the dice (default = 6, must be >= 2)

        Raises:
            ValueError: If sides is not an integer >= 2.
        """
        if not isinstance(sides, int) or sides < 2:
            raise ValueError("A dice must have an integer number of sides >= 2")
        self._sides = sides  # Protected: the number of sides should not change after creation

    @property
    def sides(self) -> int:
        """Public read-only property for the number of sides."""
        return self._sides

    def roll(self) -> int:
        """Roll the dice and return a value between 1 and sides (inclusive)."""
        return random.randint(1, self.sides)

    def __call__(self) -> int:
        """Allow the dice object to be called like a function: d20() rolls the dice."""
        return self.roll()

    def __repr__(self) -> str:
        """Representation of dice object"""
        return f"Dice(sides={self.sides})"
