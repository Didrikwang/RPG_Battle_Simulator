# Items for the object-oriented game simulator

from dice import Dice


class Weapon:
    """Represents a weapon whose damage is determined by a dice roll."""

    def __init__(self, name: str, damage_dice: Dice) -> None:
        """
        Initialise the Weapon

        Args:
            name (str): The name of the weapon.
            damage_dice (Dice): The dice rolled to determine damage.
        """
        self.name = name
        self.damage_dice = damage_dice

    def roll_damage(self) -> int:
        """Roll the weapon's damage dice and return the damage."""
        return self.damage_dice.roll()

    def __repr__(self) -> str:
        """Representation of weapon object"""
        return f"Weapon(name={self.name!r}, damage_dice={self.damage_dice!r})"

    def __str__(self) -> str:
        """String representation of weapon object"""
        return f"{self.name} (d{self.damage_dice.sides})"
