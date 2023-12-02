from client import Client

class Engine:
    def __init__(self, config: dict = {}, username: str = "", character = "") -> None:
        self._config = config
        self._user: Client = Client(config["SERVER_HOST"], int(config["SERVER_PORT"]), username, character)
        self._user.connect()
        self._user.join()
        self._character = character
        self._character.set_name(username)
        self._list_of_attack: dict = character.get_list_of_attack()

        self._user.panel.clear_panel()

    def start(self):
        if (self._user is None):
            return
        while True:
            try:
                self._user.receive()

                if (self._user.state == 'accepted' and self._user.myTurn):
                    self._user.panel.clear_panel()
                    self._character.show_healthbar()
                    self._user._targetUser.show_healthbar()
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
                        while (attack not in self._list_of_attack):
                            print("Attack not in list")
                            attack = input("Choose an attack: ")
                    else:
                        self._user.attack(attack)
                        self._user.myTurn = False

            except Exception as e:
                print(f"Error receiving data: {e}")
                break

            except KeyboardInterrupt:
                break

        self._user.close()

    def close(self):
        self._user.close()
