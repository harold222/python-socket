import random
import socket
import threading
import json
import copy


def generate_ports_to_tcp_udp(specific_port = 0):
    if specific_port == 0:
        return random.randint(10000, 55554)
    else:
        generate_random = 0
        found_port = False
        # generate differents ports for the connections
        while not found_port:
            generate_random = generate_ports_to_tcp_udp()
            if generate_random != specific_port:
                found_port = True
        return generate_random


# Save username
username = input("Ingrese su nombre de usuario: ")

# save all clients tcp to connect
clients_to_connect_tcp = []

# random port to server of my client tcp
random_port_tcp = generate_ports_to_tcp_udp()

# random port to server of my client udp
random_port_udp = generate_ports_to_tcp_udp(random_port_tcp)

# save object json with all clients
last_object_json = []

# key to identify json object
key = "allclients"

# get ip of my server by name pc
host_server = socket.gethostbyname(socket.getfqdn())


# ------------------------MOD SERVER-----------------------

def define_server_client_tcp():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host_server, random_port_tcp))
    server.listen()

    print("-------------------------------------------------------")
    print(f"Client Server TCP is running on {host_server}:{random_port_tcp}")
    return server


def define_server_client_upd():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)

    server.bind((host_server, random_port_udp))

    # don't need "listen" because UDP generate a socket without connection
    print(f"Client Server UDP is running on {host_server}:{random_port_udp}")
    print("-------------------------------------------------------")

    return server


# send messages to al clients
def broadcast(message, _client):
    for objclient in clients_to_connect_tcp:
        if objclient != _client:
            objclient.send(message)


def get_messages_tcp(other_client):
    while True:
        try:
            print(other_client.recv(1024).decode('utf-8'))
        except:
            disconnect_client(other_client)
            break


def disconnect_client(other_client):
    clients_to_connect_tcp.remove(other_client)
    other_client.close()


def get_connections_tcp(server_tcp):
    while True:
        other_client, address = server_tcp.accept()

        username_client = other_client.recv(1024).decode('utf-8')
        print(f"El usuario {username_client} esta conectado.")

        clients_to_connect_tcp.append(other_client)
        thread = threading.Thread(target=get_messages_tcp, args=(other_client,))
        thread.start()


def get_connections_udp(server_udp):
    while True:
        try:
            message, address = server_udp.recvfrom(8192)
            print("Received File:", message.strip())
            f = open(message.strip(), 'wb')

            while (message):
                f.write(message)
                server_udp.settimeout(2)
                data, addr = server_udp.recvfrom(8192)
            # print("UDP: ", message.decode("utf-8"))
        except:
            print("Error: any client in UDP")

# ----------------------FIN MOD SERVER-----------------------


# ---------------MOD CLIENT-----------------------

def generate_connections_tcp(host, port):
    client_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_with_server.connect((host, port))

    if port != 55555:
        client_with_server.send(username.encode('utf-8'))
    return client_with_server


def generate_connections_udp():
    client_with_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # don't need "connect" in UDP
    return client_with_server


def bind_other_clients_tcp(ip, port):
    new_client = generate_connections_tcp(ip, port)

    thread_per_client = threading.Thread(target=receive_messages_client_tcp, args=[new_client])
    thread_per_client.start()

    return new_client


def receive_messages_client_tcp(new_client_tcp):
    while True:
        try:
            print(new_client_tcp.recv(1024).decode('utf-8'))
        except:
            new_client_tcp.close()
            break


def write_messages_to_client(all_clients):
    while True:
        try:
            message = f"    {username}: {input('')}"
            input_message = message.split(":")

            if "audio" in input_message[1]:
                client_socket = generate_connections_udp()

                f = open(f"audios/{input_message[2]}", "rb")
                file_data = f.read(8192)

                for data in last_object_json:
                    if data["isConnected"] == "true":
                        while file_data:
                            client_socket.sendto(file_data, (data["ip"], int(data["port_udp"])))
                            file_data = f.read(8192)
                f.close()

            else:
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
                client.send(f"{random_port_tcp}:{random_port_udp}".encode("utf-8"))
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
                                        if client_server['username'] != username:
                                            if last_client_server['username'] != client_server['username']:
                                                last_object_json.append({
                                                    "username": client_server['username'],
                                                    "ip": client_server['ip'],
                                                    "port_tcp": client_server['port_tcp'],
                                                    "port_udp": client_server['port_udp'],
                                                    "isConnected": "false"
                                                })
                                else:
                                    # is empty array
                                    if client_server['username'] != username:
                                        last_object_json.append({
                                            "username": client_server['username'],
                                            "ip": client_server['ip'],
                                            "port_tcp": client_server['port_tcp'],
                                            "port_udp": client_server['port_udp'],
                                            "isConnected": "false"
                                        })

                    if len(last_object_json) > 0:
                        obj_client = []
                        for data in last_object_json:
                            if data["isConnected"] == "false":
                                print("client to connect: ", data)
                                # create thread for clients
                                ip_client = data['ip']
                                port_client = int(data['port_tcp'])

                                bind_client = bind_other_clients_tcp(ip_client, port_client)
                                obj_client.append(bind_client)
                                data["isConnected"] = "true"

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


client = generate_connections_tcp('192.168.128.1', 55555)

# create threads for receive messages to clients
receive_thread = threading.Thread(target=receive_messages_server, args=[client])
receive_thread.start()

# create thread for write messages to servers
write_thread = threading.Thread(target=write_messages_to_client, args=[clients_to_connect_tcp])
write_thread.start()

# create thread for server tcp and receive connections
server_tcp = define_server_client_tcp()
thread_server_tcp = threading.Thread(target=get_connections_tcp, args=[server_tcp])
thread_server_tcp.start()

# create server udp and receive connections
server_udp = define_server_client_upd()
thread_server_udp = threading.Thread(target=get_connections_udp, args=[server_udp])
thread_server_udp.start()
