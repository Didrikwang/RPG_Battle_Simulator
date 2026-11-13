# INF201 Deliverable 3: Mini-RPG Battle Simulator

An object-oriented battle simulator where two characters fight until one of them wins.
Characters can be warriors or mages, and can use weapons whose damage is determined by a dice roll.

**Authors:** Didrik and Theodor, NMBU, autumn 2026

## Project structure

| File | Contents |
|---|---|
| `dice.py` | `Dice`: an n-sided dice with `roll()` and `__call__` |
| `items.py` | `Weapon`: a weapon that rolls a `Dice` for damage |
| `character.py` | `Character`, plus the subclasses `Warrior` (armor) and `Mage` (mana and spells) |
| `battle.py` | `Battle`: turn-based combat manager |
| `deliverable_3.ipynb` | Presentation of each class and simulated battles |
| `requirements.txt` | Packages in the virtual environment |

## Setup

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook deliverable_3.ipynb
```

## Example

```python
from dice import Dice
from items import Weapon
from character import Warrior, Mage
from battle import Battle

conan = Warrior("Conan", weapon=Weapon("Sword", Dice(12)))
merlin = Mage("Merlin")
winner = Battle(conan, merlin).simulate_battle()
```

## Game rules

- Each round the hero attacks first, and the enemy strikes back if it is still alive.
- HP is always between 0 and `hp_max`. A character dies at 0 HP.
- A character with a weapon rolls the weapon's dice for damage instead of using base damage.
- **Warrior:** armor reduces all incoming damage.
- **Mage:** spends 10 mana to cast a spell for double base damage, otherwise attacks normally and regains 5 mana.
