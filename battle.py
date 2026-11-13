# Combat manager for the object-oriented game simulator

from character import Character


class Battle:
    """Manages turn-based combat between two characters."""

    def __init__(
        self,
        hero: Character,
        enemy: Character,
        max_rounds: int = 1000,
        verbose: bool = True,
    ) -> None:
        """
        Initialise the Battle

        Args:
            hero (Character): The character who attacks first each round.
            enemy (Character): The opposing character.
            max_rounds (int): Safety limit to stop battles where nobody can deal damage
                (e.g. two warriors whose armor blocks all damage). Default = 1000.
            verbose (bool): Print a log of each attack (default = True)

        Raises:
            ValueError: If either character is already dead, they are the same object,
            or max_rounds is less than 1.
        """
        if hero is enemy:
            raise ValueError("A character cannot battle itself")
        if not (hero.is_alive and enemy.is_alive):
            raise ValueError("Both characters must be alive to start a battle")
        if max_rounds < 1:
            raise ValueError("max_rounds must be at least 1")
        self.hero = hero
        self.enemy = enemy
        self.max_rounds = max_rounds
        self.verbose = verbose
        self.round_number = 0

    def _log(self, message: str) -> None:
        """Print message if verbose is enabled."""
        if self.verbose:
            print(message)

    def _perform_attack(self, attacker: Character, defender: Character) -> None:
        """Let attacker attack defender and log the result."""
        damage_dealt = attacker.attack(defender)
        self._log(
            f"  {attacker.name} hits {defender.name} for {damage_dealt} damage "
            f"-> {defender.name}: {defender.hp}/{defender.hp_max} HP"
        )

    def play_round(self) -> None:
        """Hero attacks enemy, and if enemy is still alive, enemy attacks hero."""
        self.round_number += 1
        self._log(f"Round {self.round_number}")
        self._perform_attack(self.hero, self.enemy)
        if self.enemy.is_alive:
            self._perform_attack(self.enemy, self.hero)

    @property
    def winner(self) -> Character | None:
        """The surviving character, or None if the battle is not decided."""
        if self.hero.is_alive and not self.enemy.is_alive:
            return self.hero
        if self.enemy.is_alive and not self.hero.is_alive:
            return self.enemy
        return None

    def simulate_battle(self) -> Character | None:
        """
        Run rounds until one character is no longer alive.

        Returns:
            Character | None: The winner, or None if max_rounds was reached (draw).
        """
        self._log(f"BATTLE: {self.hero.name} vs {self.enemy.name}")
        while self.hero.is_alive and self.enemy.is_alive:
            if self.round_number >= self.max_rounds:
                self._log(f"No winner after {self.max_rounds} rounds. It's a draw!")
                return None
            self.play_round()

        self._log(f"{self.winner.name} wins after {self.round_number} rounds!")
        return self.winner
