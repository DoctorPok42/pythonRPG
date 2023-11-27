from __future__ import annotations
from dice import Dice
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
        self._list_of_attack = {}

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

    def get_description(self):
        return self.description

    def get_list_of_attack(self):
        return self._list_of_attack

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
        missing_hp = self._max_health - self._current_health
        healthbar = f"{self._name} HP: {self._current_health}/{self._max_health} [green]{self._current_health * '█'}[/green][red]{missing_hp * '█'}[/red]"
        print(healthbar)

    def compute_damage(self, roll, target: Character, bonus=1):
        return (self._attack_value + roll, bonus)

    def attack(self, target: Character):
        if (not self.is_alive() or not target.is_alive()):
            return
        roll = self._dice.roll()
        damages,multiplier = self.compute_damage(roll, target)
        print(f"{self._name} attack {target.get_name()} with {damages} damages in your face ! "+ (f"(attack: {self._attack_value*multiplier} + roll: {roll*multiplier})" if multiplier>1  else f"(attack: {self._attack_value} + roll: {roll})"))
        target.defense(damages,self)

    def compute_defense(self, damages, roll, attacker: Character,bonus=1):
        return (damages - self._defense_value - roll, bonus)

    def defense(self, damages, attacker: Character):
        roll = self._dice.roll()
        wounds,multiplier = self.compute_defense(damages, roll,attacker)
        print(f"{self._name} take {wounds} wounds from {attacker.get_name()} in his face ! (damages: {damages} - defense: {self._defense_value} - roll: {roll})")
        self.decrease_health(wounds)


class Warrior(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Warrior!"
        self._list_of_attack = {"sword": 3, "axe": 5}

    def compute_damage(self, roll, target: Character):
        print("🪓 Bonus: Axe damage (+3) in your face !")
        return (super().compute_damage(roll, target)[0] + 3, 1)

class Mage(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Mage!"
        self._list_of_attack = {"fireball": 3, "thunder": 5}

    def compute_defense(self, damages, roll, attacker: Character):
        print("🛡️ Bonus: Magic armor (-3 wounds) !")
        return (super().compute_defense(damages, roll, attacker)[0] - 3, 1)

class Thief(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Thief!"
        self._list_of_attack = {"dagger": 3, "poison": 5}

    def compute_damage(self, roll, target: Character):
        print(f"🗡️ Bonus: Sneaky attack (ignore defense : +{target._defense_value} bonus) !")
        return (super().compute_damage(roll, target)[0] + target.get_defense_value(), 1)

class Archer(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Archer!"
        self._list_of_attack = {"bow": 3, "crossbow": 5}

    def compute_damage(self, roll, target: Character):
        dice = Dice(6).roll()
        damages,multiplier = super().compute_damage(roll, target,2)
        if dice == 6:
            print(f"🏹 Bonus: Double attack (Add Double attack : +{damages*2} bonus) !")
            return (damages, multiplier)
        else:
            return (damages,multiplier)

class Paladin(Character):
    def __init__(self, name: str, max_health: int, attack: int, defense: int, dice) -> None:
        super().__init__(name, max_health, attack, defense, dice)
        self.description = "I'm a Paladin!"
        self._list_of_attack = {"sword": 3, "heal": 5}

    def heal(self, heal_amount: int):
        self._current_health+= heal_amount
        if self._current_health > self._max_health:
            self._current_health = self._max_health
        print(f"{self._name} heal himself with {heal_amount} hp !")



def getAllCharacters() -> list:
    characters: list = []
    characters.append(Warrior("Warrior", 0, 0, 0, Dice(0)))
    characters.append(Mage("Mage", 0, 0, 0, Dice(0)))
    characters.append(Thief("Thief", 0, 0, 0, Dice(0)))
    characters.append(Archer("Archer", 0, 0, 0, Dice(0)))
    characters.append(Paladin("Paladin", 0, 0, 0, Dice(0)))
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
