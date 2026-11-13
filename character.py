# Characters for the object-oriented game simulator
# Based on game_simulator_v1.py by Turid Torheim, NMBU, 2026

from items import Weapon


class Character:
    """Represents a character in the RPG"""

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        damage: int = 10,
        weapon: Weapon | None = None,
    ) -> None:
        """
        Initialise the Character

        Args:
            name (str): The name of the character.
            hp_max (int): Max hit points (default = 100, must be > 0)
            damage (int): Base damage dealt when character attacks without a weapon (default = 10)
            weapon (Weapon | None): Optional equipped weapon (default = None)

        Raises:
            ValueError: If hp_max is not positive or damage is negative.
        """
        if hp_max <= 0:
            raise ValueError("hp_max must be greater than 0")
        if damage < 0:
            raise ValueError("damage cannot be negative")

        self.name = name
        self._hp = hp_max  # Protected attribute: only changed through take_damage() and heal()
        self._hp_max = hp_max  # Protected: max HP should not change after creation
        self.damage = damage
        self.weapon = weapon

    @property
    def hp(self) -> int:
        """Public read-only property to inspect HP without allowing direct, unsafe edits."""
        return self._hp

    
    @property
    def hp_max(self) -> int:
           """Public read-only property for max HP."""
           return self._hp_max

    @property
    def is_alive(self) -> bool:
        """Read-only property: True if the character has more than 0 HP."""
        return self._hp > 0

    def take_damage(self, amount: int) -> int:
        """
        Reduce own HP by amount. HP cannot go below 0.

        Args:
            amount (int): Incoming damage (must be >= 0)

        Returns:
            int: The HP actually lost.
        """
        if amount < 0:
            raise ValueError("Damage amount cannot be negative")
        hp_before = self._hp
        self._hp = max(self._hp - amount, 0)  # HP cannot end up lower than 0
        return hp_before - self._hp

    def heal(self, amount: int) -> int:
        """
        Increase own HP by amount. HP cannot exceed hp_max.
        A dead character (0 HP) cannot be healed.

        Args:
            amount (int): Amount to heal (must be >= 0)

        Returns:
            int: The HP actually restored.
        """
        if amount < 0:
            raise ValueError("Heal amount cannot be negative")
        if not self.is_alive:
            return 0
        hp_before = self._hp
        self._hp = min(self._hp + amount, self.hp_max)  # HP cannot end up higher than hp_max
        return self._hp - hp_before

    def roll_attack_damage(self) -> int:
        """Return weapon damage if a weapon is equipped, otherwise base damage."""
        if self.weapon is not None:
            return self.weapon.roll_damage()
        return self.damage

    def attack(self, target: "Character") -> int:
        """
        Attack target character. The target handles its own HP through take_damage().

        Returns:
            int: The HP the target actually lost.
        """
        return target.take_damage(self.roll_attack_damage())

    def introduce(self) -> None:
        """Prints a string that introduces the character"""
        print(f"Hi, my name is {self.name}!")

    def __repr__(self) -> str:
        """Representation of character object"""
        return (
            f"<{type(self).__name__} name={self.name} hp={self.hp} "
            f"damage={self.damage} weapon={self.weapon}>"
        )

    def __str__(self) -> str:
        """String representation of character object"""
        weapon_text = f" wielding {self.weapon}" if self.weapon else ""
        return (
            f"{type(self).__name__}: {self.name} with {self.hp}/{self.hp_max} HP "
            f"and {self.damage} base damage{weapon_text}"
        )


class Warrior(Character):
    """Defensive specialist: armor reduces all incoming damage."""

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        damage: int = 10,
        weapon: Weapon | None = None,
        armor: int = 5,
    ) -> None:
        """
        Initialise the Warrior

        Args:
            armor (int): Damage reduction applied to every hit (default = 5)
            Other arguments: see Character.
        """
        super().__init__(name=name, hp_max=hp_max, damage=damage, weapon=weapon)
        if armor < 0:
            raise ValueError("armor cannot be negative")
        self.armor = armor

    def take_damage(self, amount: int) -> int:
        """Reduce incoming damage by armor (never below 0) before applying it."""
        if amount < 0:
            raise ValueError("Damage amount cannot be negative")
        reduced_amount = max(amount - self.armor, 0)
        return super().take_damage(reduced_amount)

    def __str__(self) -> str:
        """String representation of warrior object"""
        return f"{super().__str__()}, armor {self.armor}"


class Mage(Character):
    """Resource-based attacker: spells cost mana and deal double damage."""

    SPELL_COST = 10
    MANA_REGEN = 5

    def __init__(
        self,
        name: str,
        hp_max: int = 100,
        damage: int = 10,
        weapon: Weapon | None = None,
        mana: int = 30,
        mana_max: int = 30,
    ) -> None:
        """
        Initialise the Mage

        Args:
            mana (int): Starting mana (default = 30)
            mana_max (int): Maximum mana (default = 30)
            Other arguments: see Character.
        """
        super().__init__(name=name, hp_max=hp_max, damage=damage, weapon=weapon)
        if mana_max < 0 or not 0 <= mana <= mana_max:
            raise ValueError("mana must be between 0 and mana_max")
        self._mana = mana  # Protected: only changed by the mage's own attacks
        self._mana_max = mana_max  # Protected: max mana should not change after creation

    @property
    def mana(self) -> int:
        """Public read-only property for current mana."""
        return self._mana

    @property
    def mana_max(self) -> int:
           """Public read-only property for max mana."""
           return self._mana_max

    def attack(self, target: Character) -> int:
        """
        Cast a spell if enough mana, otherwise fall back to a base attack.

        - Mana >= 10: spend 10 mana, deal double base damage (weapon is ignored).
        - Mana < 10: normal attack (uses weapon if equipped), then restore 5 mana.

        Returns:
            int: The HP the target actually lost.
        """
        if self._mana >= self.SPELL_COST:
            self._mana -= self.SPELL_COST
            return target.take_damage(2 * self.damage)

        damage_dealt = super().attack(target)
        self._mana = min(self._mana + self.MANA_REGEN, self.mana_max)
        return damage_dealt

    def __str__(self) -> str:
        """String representation of mage object"""
        return f"{super().__str__()}, {self.mana}/{self.mana_max} mana"
