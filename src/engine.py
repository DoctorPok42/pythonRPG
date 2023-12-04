import datetime
import threading

from client import Client
from character import Character

class Engine:
    def __init__(self, config: dict = {}, username: str = "", character = "") -> None:
        self._config = config
        self._user: Client = Client(config["SERVER_HOST"], int(config["SERVER_PORT"]), username, character)
        self._user.connect()
        self._user.join()
        self._character: Character  = character
        self._character.set_name(username)
        self._list_of_attack: dict = character.get_list_of_attack()
        self._user.panel.clear_panel()
        self._last_attack = datetime.datetime.now()

    def regenerate_health(self):
        while (self._user.state == "accepted" and
               not self._user.myTurn and
               self._user._character.get_health() < self._user._character.get_max_health()):
            if (datetime.datetime.now() - self._last_attack).total_seconds() > 10:
                self._character.regenerate(int(self._character.get_max_health() / 5))
                self._last_attack = datetime.datetime.now()
                self._character._healthbar.update_color("green")
                self._user.panel.clear_panel()
                self._character.show_healthbar()
                self._user._targetUser.show_healthbar()
                if (self._user._character.get_health() < self._user._character.get_max_health()):
                    self._user.panel.update_panel_color("purple bold")
                    self._user.panel.update_panel_text("You regenerated 5% of your health")
                else:
                    self._user.panel.update_panel_color("red bold")
                    self._user.panel.update_panel_text("")
                self._user.panel.update_panel_subtitle("Opponent's turn")
                self._user.panel.update_panel_title("Waiting for opponent's attack...")
                self._user.panel.display_panel()
                self._last_attack = datetime.datetime.now() - datetime.timedelta(seconds=3)

    def start(self):
        if (self._user is None):
            return
        while True:
            try:
                self._user.receive()

                if (self._user.state == 'accepted' and self._user.myTurn):
                    self._user.panel.clear_panel()
                    self._character._healthbar.update_color("red")
                    self._character.show_healthbar()
                    self._user._targetUser.show_healthbar()
                    print(f"{self._user._targetUser.get_name()} attack you with {self._user._targetUser._attack}") if self._user._targetUser._attack != "" else None
                    self._user.panel.update_panel_color("red bold")
                    self._user.panel.update_panel_subtitle("Your turn")
                    self._user.panel.update_panel_title("Choose an attack")
                    self._user.panel.update_panel_text(
                        "\n".join(f"{attack} ({self._list_of_attack[attack]}dmg)" for attack in self._list_of_attack))
                    self._user.panel.display_panel()

                    attack = input("Choose an attack: ")
                    if (attack == 'exit'):
                        self._user.close()
                        break
                    if (attack not in self._list_of_attack and len(attack) > 0):
                        while (attack not in self._list_of_attack and len(attack) > 0):
                            print("Attack not in list")
                            attack = input("Choose an attack: ")
                    else:
                        self._user.attack(attack)
                        self._last_attack = datetime.datetime.now()
                        self._user.myTurn = False

                elif (self._user.state == 'accepted' and not self._user.myTurn):
                    self._user.panel.clear_panel()
                    self._character.show_healthbar()
                    self._user._targetUser.show_healthbar()
                    self._user.panel.update_panel_color("red bold")
                    self._user.panel.update_panel_subtitle("Opponent's turn")
                    self._user.panel.update_panel_title("Waiting for opponent's attack...")
                    self._user.panel.update_panel_text("")
                    self._user.panel.display_panel()

                    check_for_regenerate_health = threading.Thread(target=self.regenerate_health)
                    check_for_regenerate_health.start()

            except Exception as e:
                print(f"Error receiving data: {e}")
                break

            except KeyboardInterrupt:
                break

        self._user.close()

    def close(self):
        self._user.close()
