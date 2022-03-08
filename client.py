import json
import socket
import threading
import json

# Save username
username = input("Ingrese su nombre de usuario: ")

# save all clients to connect
clients_to_connect = []

# ------------------------MOD SERVER-----------------------

def define_server_client():
    host_server = socket.gethostbyname(socket.getfqdn())
    port_server = 43434

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
            message = client.recv(1024)

            # verify if the client want to leave of the chat
            decoMessage = message.decode('utf-8').replace(" ", "").split(":")

            if len(decoMessage) > 1:
                # message to leave of the chat
                if decoMessage[1] == "salir":
                    disconnect_client(other_client)
                    break
                else:
                    print(message)
                    # publish messages
                    # broadcast(message, other_client)
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
        print(f"El usuario: {username_client} esta conectado.")

        clients_to_connect.append(other_client)

        # message = f"CHAT: {username_client} ingreso al chat".encode("utf-8")
        # broadcast(message, other_client)
        # other_client.send(f'Conectado al usuario {username}'.encode("utf8"))

        thread = threading.Thread(target=get_messages, args=(other_client,))
        thread.start()


# ----------------------FIN MOD SERVER-----------------------

# ---------------MOD CLIENT-----------------------

def generate_connections(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    if port == 43434:
        client.send(username.encode('utf-8'))
    return client


def bind_other_clients(ip, user_client):
    a = user_client

    new_client = generate_connections(ip, 43434)

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
            else:
                try:
                    object_json = json.loads(message)
                    clients = []
                    key = "allclients"

                    for val in object_json.keys():
                        if val == key:
                            clients = object_json[key]
                            break

                    if clients:
                        # for array all clients
                        obj_client = []
                        for data in clients:
                            # create thread for clients
                            ip_client = data['ip']
                            user_client = data['username']

                            bind_client = bind_other_clients(ip_client, user_client)
                            obj_client.append(bind_client)

                        write_thread = threading.Thread(target=write_messages_to_client, args=[obj_client])
                        write_thread.start()

                except ValueError as e:
                    # show all messages from the server
                    print(message)
        except:
            # if exist error close connection of socket
            print("aca")
            client.close()
            break


client = generate_connections('192.168.1.53', 55555)

# create threads for functions
receive_thread = threading.Thread(target=receive_messages_server, args=[client])
receive_thread.start()

# create server
server_client = define_server_client()
get_connections(server_client)
