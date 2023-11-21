from character import Warrior,Mage,Thief,Dice, Character
from dice import Dice
import random
from rich import print
import time

def main():
    warrior = Warrior("Joel", 20, 8, 3, Dice(6))
    mage = Mage("Lucas", 20, 8, 3, Dice(6))
    thief = Thief("Bastien", 20, 8, 3, Dice(6))

    chars: list[Character]=[warrior,mage,thief]
    stats={}

    char1= random.choice(chars)
    chars.remove(char1)
    char2= random.choice(chars)
    chars.remove(char2)

    print(char1)
    print(char2)

    stats[char1.get_name()]=0
    stats[char2.get_name()]=0

    print(stats)

    for i in range(100):
        print(f"Round n°{i+1}")
        char1.regenerate()
        char2.regenerate()
        while char1.is_alive() and char2.is_alive():
            char1.attack(char2)
            char2.attack(char1)
            # time.sleep(1)
        if char1.is_alive():
            stats[char1.get_name()]+=1
        else:
            stats[char2.get_name()]+=1

    print(stats)


if __name__ == "__main__":
    main()