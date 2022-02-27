import socket
import threading

username = input("Ingrese su usuario: ")

host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receiveMessages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            client.close()
            break

def writeMessages():
    while True:
        try:
            message = f"    {username}: {input('')}"
            client.send(message.encode('utf-8'))
        except:
            break


# creo dos hilos para cada funcion
receive_thread = threading.Thread(target=receiveMessages)
receive_thread.start()

write_thread = threading.Thread(target=writeMessages)
write_thread.start()
