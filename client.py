import random
import socket
import threading
import json
import copy

# Save username
username = input("Ingrese su nombre de usuario: ")

# save all clients to connect
clients_to_connect = []

# random port to server of my client
random_port = random.randint(10000, 55554)

# save object json with all clients
last_object_json = []

# key to identify json object
key = "allclients"


# ------------------------MOD SERVER-----------------------

def define_server_client():
    host_server = socket.gethostbyname(socket.getfqdn())
    # port_server = 43434
    port_server = random_port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((host_server, port_server))
    server.listen()

    print("-------------------------------------------------------")
    print(f"Client Server is running on {host_server}:{port_server}")
    print("-------------------------------------------------------")
    return server


# send messages to al clients
def broadcast(message, _client):
    for client in clients_to_connect:
        if client != _client:
            client.send(message)


def get_messages(other_client):
    while True:
        try:
            message = other_client.recv(1024).decode('utf-8')

            print(message)

            # decoMessage = decoMessage.replace(" ", "").split(":")

            # if len(decoMessage) > 1:
            #     # message to leave of the chat
            #     if decoMessage[1] == "salir":
            #         disconnect_client(other_client)
            #         break
            #     else:
            #         print(message)
            #         # publish messages
            #         # broadcast(message, other_client)
        except:
            disconnect_client(other_client)
            break


def disconnect_client(other_client):
    clients_to_connect.remove(other_client)
    other_client.close()


def get_connections(server):
    while True:
        other_client, address = server.accept()

        username_client = other_client.recv(1024).decode('utf-8')
        print(f"El usuario {username_client} esta conectado.")

        clients_to_connect.append(other_client)

        # message = f"CHAT: {username_client} ingreso al chat".encode("utf-8")
        # broadcast(message, other_client)
        # other_client.send(f'Conectado al usuario {username}'.encode("utf8"))

        thread = threading.Thread(target=get_messages, args=(other_client,))
        thread.start()


# ----------------------FIN MOD SERVER-----------------------

# ---------------MOD CLIENT-----------------------

def generate_connections(host, port):
    clientWithServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientWithServer.connect((host, port))

    if port != 55555:
        clientWithServer.send(username.encode('utf-8'))
    return clientWithServer


def bind_other_clients(ip, port):
    new_client = generate_connections(ip, port)

    thread_per_client = threading.Thread(target=receive_messages_client, args=[new_client])
    thread_per_client.start()

    return new_client


def receive_messages_client(new_client):
    while True:
        try:
            message = new_client.recv(1024).decode('utf-8')
            print(message)
        except:
            new_client.close()
            break


def write_messages_to_client(all_clients):
    while True:
        try:
            message = f"    {username}: {input('')}"
            for value in all_clients:
                value.send(message.encode('utf-8'))
        except:
            break

def receive_messages_server(client):
    while True:
        try:
            # messages to server and decode
            message = client.recv(1024).decode('utf-8')

            # server ask the username to client
            if message == "@username":
                # send save username to server
                client.send(username.encode("utf-8"))
            elif message == "@port":
                # send random port to server
                client.send(f"{random_port}".encode("utf-8"))
            else:
                try:
                    object_json = json.loads(message)

                    for val in object_json.keys():
                        if val == key:
                            # shallow copy
                            copy_json = copy.copy(last_object_json)
                            # filter current ip and port of this server
                            for client_server in object_json[key]:
                                if len(copy_json) > 0:
                                    for last_client_server in copy_json:
                                        # clients different of my client
                                        if last_client_server['username'] != client_server['username'] & client_server['username'] != username:
                                            a = 1
                                            last_object_json.append({
                                                "username": client_server['username'],
                                                "ip": client_server['ip'],
                                                "port": client_server['port'],
                                                "isConnected": "false"
                                            })
                                else:
                                    # is empty object json
                                    if client_server['username'] != username:
                                        last_object_json.append({
                                            "username": client_server['username'],
                                            "ip": client_server['ip'],
                                            "port": client_server['port'],
                                            "isConnected": "false"
                                        })

                    if len(last_object_json) > 0:
                        obj_client = []
                        # copy_json = copy.copy(last_object_json)
                        for data in last_object_json:
                            if data["isConnected"] == "false":
                                # create thread for clients
                                ip_client = data['ip']
                                port_client = int(data['port'])

                                bind_client = bind_other_clients(ip_client, port_client)
                                obj_client.append(bind_client)
                                data["isConnected"] = "true"

                            write_thread = threading.Thread(target=write_messages_to_client, args=[obj_client])
                            write_thread.start()

                        print("clients to connect: ", last_object_json)

                except ValueError as e:
                    # show all messages from the server
                    print(message)
        except:
            # if exist error close connection of socket
            print("aca")
            client.close()
            break

hostServer = '192.168.1.53'
# hostServer = '172.18.0.2'

client = generate_connections(hostServer, 55555)

# create threads for functions
receive_thread = threading.Thread(target=receive_messages_server, args=[client])
receive_thread.start()

# create server
server_client = define_server_client()
get_connections(server_client)
