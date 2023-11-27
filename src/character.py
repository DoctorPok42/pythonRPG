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

    def __str__(self):
        return f"attack: {self._attack_value} and defense: {self._defense_value}"

    def is_alive(self):
        # return bool(self._current_health)
        return self._current_health > 0

    def regenerate(self):
        self._current_health = self._max_health

    def decrease_health(self, amount):
        if (self._current_health - amount < 0):
            amount = self._current_health
        self._current_health -= amount
        self.show_healthbar()

    def show_healthbar(self):
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
        self._list_of_attack = {"sword": 5, "axe": 8}

class Mage(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Mage!"
        self._list_of_attack = {"fireball": 10, "thunder": 12}

    def compute_defense(self, damages, roll):
        return (super().compute_defense(damages, roll))

class Thief(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Thief!"
        self._list_of_attack = {"dagger": 9, "poison": 10}

    # def compute_damage(self, roll, target: Character):
    #     print(f"🗡️ Bonus: Sneaky attack (ignore defense : +{target._defense_value} bonus) !")
    #     return (super().compute_damage(roll, target)[0] + target.get_defense_value(), 1)

class Archer(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Archer!"
        self._list_of_attack = {"bow": 12, "crossbow": 15}

    # def compute_damage(self, roll, target: Character):
    #     dice = Dice(6).roll()
    #     damages,multiplier = super().compute_damage(roll, target,2)
    #     if dice == 6:
    #         print(f"🏹 Bonus: Double attack (Add Double attack : +{damages*2} bonus) !")
    #         return (damages, multiplier)
    #     else:
    #         return (damages,multiplier)

class Paladin(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Paladin!"
        self._list_of_attack = {"sword": 15, "heal": 10}

    def heal(self, heal_amount: int):
        self._current_health+= heal_amount
        if self._current_health > self._max_health:
            self._current_health = self._max_health
        print(f"{self._name} heal himself with {heal_amount} hp !")

def getAllCharacters() -> list:
    characters: list = [
        Warrior("Gerard", 20, 8, 3, Dice(6)),
        Mage("Lisa", 20, 8, 3, Dice(6)),
        Thief("Thief", 20, 8, 3, Dice(6)),
        Archer("Archer", 20, 8, 3, Dice(6)),
        Paladin("Paladin", 20, 8, 3, Dice(6)),
    ]
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
