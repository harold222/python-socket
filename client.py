import json
import socket
import threading
import json

# Save username
username = input("Ingrese su nombre de usuario: ")

def generateConnection():
    # define ip and port
    hostServer = '127.0.0.1'
    portServer = 55555

    # connection by protocol TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hostServer, portServer))
    return client


def receiveMessages(client):
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
                        print("a")
                        # json with the all clients
                        # generar conexion con los otros clientes con la respuesta dada

                    # for key, value in clients['allclients'].items():
                    #     print
                    #     key, value

                except ValueError as e:
                    # show all messages the server
                    print(message)
        except:
            # if exist error close connection of socket
            client.close()
            break

def writeMessages(client):
    while True:
        try:
            message = f"    {username}: {input('')}"
            client.send(message.encode('utf-8'))
        except:
            break


client = generateConnection()

# create threads for functions
receive_thread = threading.Thread(target=receiveMessages, args=[client])
receive_thread.start()

write_thread = threading.Thread(target=writeMessages, args=[client])
write_thread.start()
