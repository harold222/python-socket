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
def defineServer():
    # ip and port to show the server
    hostServer = '127.0.0.1'
    portServer = 55555

    # SOCK_STREAM = protocol tcp
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((hostServer, portServer))
    server.listen()

    print(f"Server running on {hostServer}:{portServer}")
    return server


# send messages to al clients
def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def generateListOfClients():
    arr = []
    for index, user in enumerate(usernames):
        data = {
            "username": user,
            "ip": addresses[index][0],
            "port": addresses[index][1]
        }
        # data = user, addresses[index][0], addresses[index][1]
        arr.append(data)
    return arr

# allDataClients.insert(username, host, port)
# print(allDataClient)

def handleMessages(client):
    while True:
        try:
            # max 1024bytes
            message = client.recv(1024)

            # verify if the client want to leave of the chat
            decoMessage = message.decode('utf-8').replace(" ", "").split(":")

            if len(decoMessage) > 1:
                # message to leave of the chat
                if decoMessage[1] == "salir":
                    disconnectClient(client)
                    break
                else:
                    # publish messages
                    broadcast(message, client)
        except:
            disconnectClient(client)
            break


def disconnectClient(client):
    index = clients.index(client)
    username = usernames[index]

    message = f"CHAT: {username} se ha desconectado."
    broadcast(message.encode('utf-8'), client)
    print(message)

    # Elimino al cliente
    clients.remove(client)
    usernames.remove(username)
    client.close()


def receiveConnections(server):
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

        # show the new client of all client
        message = f"CHAT: {username} ingreso al chat".encode("utf-8")
        broadcast(message, client)

        # send list of clients
        client.sendall(json.dumps({
            "allclients": generateListOfClients()
        }, sort_keys=False, indent=2).encode("utf8"))

        # for each client a thread is assigned
        thread = threading.Thread(target=handleMessages, args=(client,))
        thread.start()


receiveConnections(defineServer())
