import json
import socket
import threading
import json


host = socket.getfqdn()
addr = socket.gethostbyname(host)

print(host + " and " + addr)

# Save username
username = input("Ingrese su nombre de usuario: ")



def define_server():
    host_server = '127.0.0.1'
    port_server = 55555

    # SOCK_STREAM = protocol tcp
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((host_server, port_server))
    server.listen()

    print(f"Server running on {host_server}:{port_server}")
    return server


def generate_connections(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client


def bind_other_clients(ip, port, username):
    new_client = generate_connections(ip, port)

    thread_per_client = threading.Thread(target=receive_messages_client, args=[new_client])
    thread_per_client.start()


def receive_messages_client(client):
    print("s")


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
                        for data in clients:
                            # create thread for clients
                            bind_other_clients(data['ip'], data['port'], data['username'])

                except ValueError as e:
                    # show all messages from the server
                    print(message)
        except:
            # if exist error close connection of socket
            print("aca")
            client.close()
            break

# def writeMessages(client):
#     while True:
#         try:
#             message = f"    {username}: {input('')}"
#             client.send(message.encode('utf-8'))
#         except:
#             break


client = generate_connections('192.168.1.53', 55555)

# create threads for functions
receive_thread = threading.Thread(target=receive_messages_server, args=[client])
receive_thread.start()

# define_server()

# write_thread = threading.Thread(target=writeMessages, args=[client])
# write_thread.start()
