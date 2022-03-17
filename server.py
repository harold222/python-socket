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

    return json.dumps({ "allclients": arr }).encode("utf8")


def receive_connections(server):
    while True:
        # accept conexions of any client
        client, address = server.accept()
        try:
            # question the username of the client
            client.send("@data".encode("utf-8"))
            all_data = client.recv(1024)

            if all_data:
                all_data = all_data.decode("utf-8").split(":")
                clients.append(client)

                usernames.append(all_data[0])
                addresses.append(address)
                ports_tcp.append(all_data[1])
                ports_udp.append(all_data[2])

                # send list of clients
                if len(clients):
                    for client in clients:
                        client.send(generate_list_of_clients())
        except:
            client.close()


receive_connections(create_server())