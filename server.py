import socket
import json

# ---------DEFINE VARIABLES----------

# save all objects of clients
clients = []

# save username of client
usernames = []

# save ip of clients
addresses = []

# save port tpc of clients
ports_tcp = []

# save port udp of clients
ports_udp = []


# creation of server
def create_server():
    # ip and port to show the server
    host_server = socket.gethostbyname(socket.getfqdn())
    port_server = 55555

    # SOCK_STREAM = protocol tcp
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((host_server, port_server))
    server.listen()

    print(f"Server running on {host_server}:{port_server}")
    return server


def generate_list_of_clients():
    arr = []
    for index, user in enumerate(usernames):
        arr.append({
            "username": user,
            "ip": addresses[index][0],
            "port_tcp": ports_tcp[index],
            "port_udp": ports_udp[index]
        })

    print(arr)

    return json.dumps({
        "allclients": arr
    }, sort_keys=False, indent=2).encode("utf8")


def receive_connections(server):
    while True:
        # accept conexions of any client
        client, address = server.accept()

        # question the username of the client
        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")

        # port used to client server
        client.send("@port".encode("utf-8"))
        port = client.recv(1024).decode("utf-8").split(":")

        # save data of new client
        clients.append(client)
        usernames.append(username)
        addresses.append(address)
        ports_tcp.append(port[0])
        ports_udp.append(port[1])

        # send list of clients
        json_list = generate_list_of_clients()
        for client in clients:
            client.send(json_list)


receive_connections(create_server())