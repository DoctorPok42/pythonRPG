import socket
import threading
import argparse
import json
import os
from random import randint
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=8080, help='Port to listen on')

args = parser.parse_args()

SERVER_IP = os.getenv("SERVER_HOST")
SERVER_PORT = args.port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

server_socket.listen()

print('The server is listening on {}:{}'.format(SERVER_IP, SERVER_PORT))

waiting_players = []
playersInGame = []

def check_if_target(username):
    return next((p for p in playersInGame if p['username'] == username), None)

def handle_client(client_socket, addr):
    print('Connection established with {}'.format(addr))

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            data = json.loads(data.decode())

            if (data['action'] == 'join'):
                print('{} joined the waiting list'.format(data['username']))
                dataUser = {
                    "username": data['username'],
                    "character": data['character'],
                    "socket": client_socket,
                    "addr": addr,
                    "health": data['health'],
                    "maxHealth": data['maxHealth'],
                }
                waiting_players.append(dataUser)
                send_waiting_list()

            if (data['action'] == 'challenge'):
                print('Challenge from {} to {}'.format(data['challenger'], data['targetUser']))
                challenged_player = next((p for p in waiting_players if p['username'] == data['targetUser']), None)
                if (challenged_player):
                    challenged_player['socket'].send(json.dumps({
                        "action": "challenge",
                        "username": data['challenger'],
                    }).encode())

            if (data['action'] == 'challenge_response'):
                challenger = next((p for p in waiting_players if p['username'] == data['targetUser']), None)
                whoStarteFirst = randint(0, 1)
                if (data['response'] == 'y' and challenger):
                    player = next((p for p in waiting_players if p['username'] == data['username']), None)
                    player['targetUser'] = data['targetUser']
                    challenger['targetUser'] = data['username']
                    playersInGame.append(player)
                    playersInGame.append(challenger)

                    waiting_players.remove(next((p for p in waiting_players if p['username'] == data['username']), None))
                    waiting_players.remove(next((p for p in waiting_players if p['username'] == data['targetUser']), None))
                    send_waiting_list()

                    client_socket.send(json.dumps({
                        "action": "challenge_response",
                        "targetUser": data['targetUser'],
                        "response": data['response'],
                        "whoStarteFirst": whoStarteFirst,
                        "targetHealth": challenger['health'],
                        "targetMaxHealth": challenger['maxHealth'],
                    }).encode())
                    print('Challenge accepted between {} and {}'.format(data['targetUser'], data['username']))
                else:
                    print('Challenge rejected between {} and {}'.format(data['targetUser'], data['username']))

                challenger['socket'].send(json.dumps({
                    "action": "challenge_response",
                    "targetUser": data['username'],
                    "response": data['response'],
                    "whoStarteFirst": not whoStarteFirst,
                    "targetHealth": player['health'],
                    "targetMaxHealth": player['maxHealth'],
                }).encode())

            if (data['action'] == 'attack'):
                print('{} attacked {} with {} ({})'.format(data['username'], data['targetUser'], data['attack'], data['points']))
                attacked_player = next((p for p in playersInGame if p['username'] == data['targetUser']), None)
                if (attacked_player):
                    attacked_player['socket'].send(json.dumps({
                        "action": "attack",
                        "username": data['username'],
                        "attack": data['attack'],
                        "points": data['points'],
                    }).encode())

            if (data['action'] == 'response_attack'):
                target_player = next((p for p in playersInGame if p['username'] == data['targetUser']), None)
                player = next((p for p in playersInGame if p['username'] == data['username']), None)
                player['health'] = data['health']
                if (player['health'] <= 0):
                    player['socket'].send(json.dumps({
                        "action": "game_over",
                        "username": data['username'],
                    }).encode())
                    target_player['socket'].send(json.dumps({
                        "action": "win",
                        "username": data['targetUser'],
                    }).encode())
                    playersInGame.remove(player)
                    playersInGame.remove(target_player)
                    print('{} won between {} and {}'.format(data['targetUser'], data['targetUser'], data['username']))
                else:
                    target_player['socket'].send(json.dumps({
                        "action": "response_attack",
                        "username": data['username'],
                        "health": data['health'],
                        "maxHealth": data['maxHealth'],
                    }).encode())

        except Exception as e:
            print('Error communicating with {}: {}'.format(addr, e))
            break

    print('Connection closed with {}'.format(addr))
    if (next((p for p in waiting_players if p['socket'] == client_socket), None)):
        waiting_players.remove(next((p for p in waiting_players if p['socket'] == client_socket), None))
        send_waiting_list()
    if (next((p for p in playersInGame if p['socket'] == client_socket), None)):
        playersInGame.remove(next((p for p in playersInGame if p['socket'] == client_socket), None))

    if (len(waiting_players) == 0 and len(playersInGame) == 0):
        print('\033cThe server is listening on {}:{}'.format(SERVER_IP, SERVER_PORT))

    client_socket.close()

def send_waiting_list():
    for player_socket in waiting_players:
        try:
            player_socket['socket'].send(json.dumps({
                "action": "waiting_list",
                "waiting_list": {
                    "username": list(map(lambda p: p.get('username'), waiting_players)),
                    "character": list(map(lambda p: p.get('character'), waiting_players)),
                }
            }).encode())
        except Exception as e:
            print('Error sending the waiting list to a client: {}'.format(e))

while True:
    try:
        client_socket, addr = server_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()


    except Exception as e:
        print('Error when connecting a client: {}'.format(e))

    except KeyboardInterrupt:
        print('\nClosing the server...')
        break

server_socket.close()
