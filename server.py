#  hacer conexion a la base de datos para guardar clientes
import socket
import threading

host = '127.0.0.1'
port = 55555

# AF_INET = socket tipo internet
# SOCK_STREAM = protocolo tcp
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()

print(f"Server running on {host}:{port}")

clients = []
usernames = []


# Enviara mensaje a todos los clientes
def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)


def handleMessages(client):
    while True:
        try:
            # limite que esta funcion leera, 1024bytes
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            # utf-8 para la codificacion
            broadcast(f"CHAT: {username} se ha desconectado.".encode('utf-8'), client)

            # Elimino al cliente
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break



def receiveConnections():
    while True:
        # acepta conexiones de los clientes
        # retorna objeto conexion cliente y ip y port de la conexion del cliente
        client, address = server.accept()

        # el servidor requiere el username del cliente
        client.send("@username".encode("utf-8"))

        # decodifico el mensaje
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"El usuario: {username} esta conectado con {str(address)}")

        message = f"CHAT: {username} ingreso al chat".encode("utf-8")
        broadcast(message, client)
        client.send('Conectado al servidor'.encode("utf8"))

        # por cada cliente que se conecte se asignara un hilo para tener mensajes por separado
        thread = threading.Thread(target=handleMessages, args=(client,))
        thread.start()


receiveConnections()
