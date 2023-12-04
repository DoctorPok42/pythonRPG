from __future__ import annotations
from dice import Dice
from healthbar import Healthbar
from rich import print

class Character:

    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        self._name = name
        self.description = ""
        self._max_health = max_health
        self._current_health = max_health
        self._attack_value = attack
        self._defense_value = defense
        self._dice = dice
        self._healthbar = Healthbar(self._name, self._max_health, self._current_health)
        self._healthbar.create_healthbar()
        self._list_of_attack = {}

    def __str__(self):
        return f"attack: {self._attack_value} and defense: {self._defense_value}"

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name
        self._healthbar.update_name(name)

    def get_description(self):
        return self.description

    def get_list_of_attack(self):
        return self._list_of_attack

    def get_health(self):
        return self._current_health

    def get_max_health(self):
        return self._max_health

    def get_defense_value(self):
        return self._defense_value

    def is_alive(self):
        return self._current_health > 0

    def regenerate(self, amount):
        if (self._current_health + amount > self._max_health):
            amount = self._max_health - self._current_health
        self._current_health += amount

    def decrease_health(self, amount):
        if (self._current_health - amount < 0):
            amount = self._current_health
        self._current_health -= amount
        self.show_healthbar()

    def show_healthbar(self) -> None:
        self._healthbar.update_health(self._current_health)
        self._healthbar.display_healthbar()

    def compute_damage(self, attackName: str, roll: int) -> int:
        return (self._list_of_attack[attackName] + roll)

    def attack(self, attack: str) -> int:
        if (not self.is_alive()):
            return
        roll = self._dice.roll()
        damages = self.compute_damage(attack, roll)
        return damages

    def compute_defense(self, damages: int, roll: int) -> int:
        return (damages - self._defense_value - roll)

    def defense(self, damages: int) -> None:
        roll = self._dice.roll()
        wounds = self.compute_defense(damages, roll)
        self.decrease_health(wounds)


class Warrior(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Warrior!"
        self._list_of_attack = {"sword": 7, "axe": 10}

    def compute_damage(self, attackName: str, roll: int) -> int:
        return super().compute_damage(attackName, roll)+3 if roll==3 else super().compute_damage(attackName, roll)

class Mage(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Mage!"
        self._list_of_attack = {"fireball": 12, "thunder": 14}

    def compute_defense(self, damages, roll):
        return super().compute_defense(damages, roll)//2 if roll==4 else super().compute_defense(damages, roll)

class Thief(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Thief!"
        self._list_of_attack = {"dagger": 11, "poison": 12}

class Archer(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Archer!"
        self._list_of_attack = {"bow": 14, "crossbow": 17}

    def compute_damage(self, attackName: str, roll: int) -> int:
        if roll == 4:
            return (super().compute_damage(attackName, roll)*2)
        elif roll == 1:
            return (super().compute_damage(attackName, roll)//2)
        else:
            return super().compute_damage(attackName, roll)

class Paladin(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Paladin!"
        self._list_of_attack = {"sword": 18, "heal": 10}

    def heal(self, heal_amount: int):
        self._current_health += heal_amount
        if self._current_health > self._max_health:
            self._current_health = self._max_health

    def compute_defense(self, damages: int, roll: int) -> int:
        if roll==5:
            return (super().compute_defense(damages, roll)//3)
        else:
            return super().compute_defense(damages, roll)

def getAllCharacters() -> list:
    characters: list = []
    characters.append(Warrior("Warrior", 35, 15, 5, Dice(3)))
    characters.append(Mage("Mage", 25, 10, 3, Dice(4)))
    characters.append(Thief("Thief", 28, 12, 4, Dice(6)))
    characters.append(Archer("Archer", 22, 12, 5, Dice(4)))
    characters.append(Paladin("Paladin", 30, 15, 5, Dice(5)))
    return characters

if __name__ == "__main__":
    a_dice = Dice(6)

    character1 = Warrior("Gerard", 20, 8, 3, Dice(6))
    character2 = Thief("Lisa", 20, 8, 3, Dice(6))
    print(character1)
    print(character2)

    while(character1.is_alive() and character2.is_alive()):
        character1.attack(character2)
        character2.attack(character1)
