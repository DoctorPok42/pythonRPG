import os
from dotenv import load_dotenv
from rich import print

from panel import Panels
from engine import Engine
from character import getAllCharacters

load_dotenv()

config = {
    "SERVER_HOST": os.getenv("SERVER_HOST"),
    "SERVER_PORT": os.getenv("SERVER_PORT"),
}

if __name__ == '__main__':
    panel: Panels = Panels("Welcome to PythonRPG game!", "PythonRPG", (1, 3), "", "blue bold")
    panel.create_panel()
    panel.display_panel()
    username = ""
    characters = getAllCharacters()

    while True:
        username = input("To start, please enter a username: ")
        try:
            if (len(username) < 3):
                print("Your username must be at least 3 characters long")
            else:
                username = username.lower()
                break
        except Exception as e:
            print(f"Error: {e}")
            break
        except KeyboardInterrupt:
            exit(0)

    panel.clear_panel()
    panel.update_panel_subtitle(f"{username}")
    panel.clear_and_display_panel()
    print("Choose a character:\n")
    for character in characters:
        print(f"{character.get_name()} - {character.get_description()} ({character})")

    characterChoice = None

    while True:
        try:
            characterChoice = input("Enter a character name: ")
            if (characterChoice.lower() not in list(map(lambda c: (c.get_name()).lower(), characters))):
                print("This character does not exist")
            else:
                characterChoice = next((c for c in characters if c.get_name().lower() == characterChoice.lower()), None)
                break
        except Exception as e:
            print(f"Error: {e}")
            break
        except KeyboardInterrupt:
            exit(0)

    panel.clear_panel()
    panel.destroy_panel()

    engine: Engine = Engine(config, username, characterChoice)
    engine.start()
