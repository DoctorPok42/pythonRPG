import socket
import threading
import json
from time import sleep

from panel import Panels as p
from character import Character
from healthbar import Healthbar
from target import Target

class Client:
    def __init__(self, host: str, port: str, username: str, character) -> None:
        self._host: str = host
        self._port: str = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._waiting_list: list = []
        self._username: str = username
        self._character: Character = character
        self._targetUser = Target("", 0, 0)
        self.state: str = 'waiting'
        self.myTurn: bool = False
        self.panel = p("", "", (1, 3), "", "none")
        self.panel.create_panel()

    def connect(self):
        self._socket.connect((self._host, self._port))
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def join(self):
        self._socket.send(json.dumps({
            "action": "join",
            "username": self._username,
            "character": self._character.get_name(),
            "maxHealth": self._character.get_max_health(),
            "health": self._character.get_health(),
        }).encode())
        self.state = 'joined'

    def receive(self):
        try:
            data = self._socket.recv(1024)
            if not data:
                return
            data = json.loads(data.decode())

            if (data['action'] == 'challenge'):
                self.state = 'challenged'
                self.challenge_response(data['username'])

            elif (data['action'] == 'challenge_response'):
                if (data['response'] == 'y'):
                    self._targetUser.change_health(data['targetHealth'])
                    self._targetUser.change_max_health(data['targetMaxHealth'])
                    self.challenge_accepted(data['targetUser'], data['whoStarteFirst'])
                else:
                    self.state = 'joined'
                    print(f"{data['targetUser']} declined your challenge")
                    sleep(3)
                    self.getWaitingList()

            elif (data['action'] == 'waiting_list'):
                self.waiting_list = data['waiting_list']
                self.getWaitingList()

            elif (data['action'] == 'attack'):
                if (data['attack'] == "heal"):
                    self._targetUser._attack = ""
                    self._targetUser.change_health(self._targetUser.get_health() + data['points'])
                else:
                    self._targetUser._attack = data['attack']
                    self._character.defense(data['points'])
                self.response_attack()
                self.myTurn = True

            elif (data['action'] == 'response_attack'):
                self._targetUser.change_health(data['health'])

            elif (data['action'] == 'win'):
                self.state = 'win'
                self.panel.update_panel_title("Congratulations!")
                self.panel.update_panel_color("green bold")
                self.panel.update_panel_text("You won the game! 🎉")
                self.panel.update_panel_subtitle("")
                self.panel.clear_and_display_panel()
                self.close()

            elif (data['action'] == 'game_over'):
                self.state = 'game_over'
                self.panel.update_panel_title("Game over...")
                self.panel.update_panel_color("red bold")
                self.panel.update_panel_text("You lost the game! 😢")
                self.panel.update_panel_subtitle("")
                self.panel.clear_and_display_panel()
                self.close()

            else:
                pass

        except Exception as e:
            print(f"Error receiving data: {e}")

        except KeyboardInterrupt:
            self.close()

    def getWaitingList(self) -> list:

        if (len(self.waiting_list['username']) < 2):
            self.panel.update_panel_title("Waiting list")
            self.panel.update_panel_color("yellow bold")
            self.panel.update_panel_text("Waiting for other players...")
            self.panel.update_panel_subtitle("")
            self.panel.clear_and_display_panel()
        else:
            self.panel.update_panel_title("Waiting list")
            self.panel.update_panel_color("yellow bold")
            self.panel.update_panel_subtitle(self._username)
            self.panel.update_panel_text(
                "\n".join(f"{player} - ({self.waiting_list['character'][self.waiting_list['username'].index(player)]})" for player in self.waiting_list['username'] if player != self._username))
            self.panel.clear_and_display_panel()

            while (self.state == 'joined'):
                if (self.state == 'challenged'):
                    break
                else:
                    challenge = input("Who do you want to challenge? ")

                    if (challenge.lower() not in self.waiting_list['username'] and len(challenge) > 0):
                        print("User not in waiting list")
                        continue
                    if (challenge == self._username):
                        print("You can't challenge yourself")
                        continue
                    else:
                        self.challenge(challenge.lower())
                        break
        return self.waiting_list

    def challenge(self, targetUser: str) -> None:
        self._socket.send(json.dumps({
            "action": "challenge",
            "challenger": self._username,
            "targetUser": targetUser,
        }).encode())
        self.state = 'challenged'

    def challenge_response(self, targetUser: str) -> None:
        response = None
        response = input(f"{targetUser} challenged you!\nDo you accept? (y/n): ")

        while (response != 'y' and response != 'n'):
            response = input("Invalid response\nDo you accept? (y/n): ")

        self._socket.send(json.dumps({
            "action": "challenge_response",
            "username": self._username,
            "targetUser": targetUser,
            "response": response,
        }).encode())

        if (response == 'n'):
            self.state = 'joined'
            self.getWaitingList()
        else:
            self.state = 'accepted'

    def challenge_accepted(self, targetUser: str, whoStarteFirst: bool) -> None:
        self.targetUser = targetUser
        self._targetUser.change_name(targetUser)
        print("\033c", end="")
        self._character.show_healthbar()
        self._targetUser.show_healthbar()
        self.myTurn = whoStarteFirst
        self.state = 'accepted'

    def attack(self, attack: str) -> None:
        if (attack == "heal"):
            self._character.heal(self._character._list_of_attack[attack])
            self._character._healthbar.update_health(self._character.get_health())

        self._socket.send(json.dumps({
            "action": "attack",
            "username": self._username,
            "targetUser": self.targetUser,
            "attack": attack,
            "points": self._character.attack(attack),
        }).encode())

    def response_attack(self) -> None:
        self._socket.send(json.dumps({
            "action": "response_attack",
            "username": self._username,
            "targetUser": self.targetUser,
            "health": self._character.get_health(),
            "maxHealth": self._character.get_max_health(),
        }).encode())

    def close(self):
        self._socket.close()
        exit(0)
