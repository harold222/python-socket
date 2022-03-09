import socket
import threading
import json

# ---------DEFINE VARIABLES----------

# save all objects of clients
clients = []

# save username of client
usernames = []

# save ip and port of clients
addresses = []


# creation of server
def define_server():
    # ip and port to show the server

    host_server = socket.gethostbyname(socket.getfqdn())
    port_server = 55555

    # SOCK_STREAM = protocol tcp
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((host_server, port_server))
    server.listen()

    print(f"Server running on {host_server}:{port_server}")
    return server


def generate_list_of_clients(client):
    arr = []
    index = clients.index(client)
    current_user = usernames[index]

    for index, user in enumerate(usernames):
        if user != current_user:
            arr.append({
                "username": user,
                "ip": addresses[index][0]
            })

    print(arr)

    return json.dumps({
        "allclients": arr
    }, sort_keys=False, indent=2).encode("utf8")


# def handleMessages(client):
#     while True:
#         try:
#             # max 1024bytes
#             message = client.recv(1024)
#
#             # verify if the client want to leave of the chat
#             decoMessage = message.decode('utf-8').replace(" ", "").split(":")
#
#             if len(decoMessage) > 1:
#                 # message to leave of the chat
#                 if decoMessage[1] == "salir":
#                     disconnect_client(client)
#                     break
#                 else:
#                     # publish messages
#                     broadcast(message, client)
#         except:
#             disconnect_client(client)
#             break


def disconnect_client(client):
    index = clients.index(client)
    username = usernames[index]

    print(f"CHAT: {username} se ha desconectado.")

    # remove client
    clients.remove(client)
    usernames.remove(username)
    addresses.remove(addresses[index])
    client.close()


def receive_connections(server):
    while True:
        # accept conexions of any client
        client, address = server.accept()

        # question the username of the client
        client.send("@username".encode("utf-8"))

        # get the username
        username = client.recv(1024).decode('utf-8')

        # save data of new client
        clients.append(client)
        usernames.append(username)
        addresses.append(address)

        # send list of clients
        a = generate_list_of_clients(client)
        client.sendall(a)


receive_connections(define_server())