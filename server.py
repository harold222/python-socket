import socket
import json


class GenerateServer:
    def __init__(self, port):
        self.port = port
        self.host = socket.gethostbyname(socket.getfqdn())
        self.server = None
        self.clients = []
        self.usernames = []
        self.addresses = []
        self.ports_tcp = []
        self.ports_udp = []

    def print_server(self):
        print(f"Server running on {self.host}:{self.port}")

    # creation of server
    def create_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.print_server()
        self.receive_connections()

    def generate_list_of_clients(self):
        arr = []
        for index, user in enumerate(self.usernames):
            arr.append({
                "username": user,
                "ip": self.addresses[index][0],
                "port_tcp": self.ports_tcp[index],
                "port_udp": self.ports_udp[index]
            })

        print(arr)

        return json.dumps({"allclients": arr}).encode("utf8")

    def receive_connections(self):
        while True:
            # accept conexions of any client
            if self.server is not None:
                client, address = self.server.accept()
                try:
                    # question the username of the client
                    client.send("@data".encode("utf-8"))
                    all_data = client.recv(1024)

                    if all_data:
                        all_data = all_data.decode("utf-8").split(":")

                        self.clients.append(client)
                        self.usernames.append(all_data[0])
                        self.addresses.append(address)
                        self.ports_tcp.append(all_data[1])
                        self.ports_udp.append(all_data[2])

                        # send list of clients
                        if len(self.clients) > 0:
                            for client in self.clients:
                                client.send(self.generate_list_of_clients())
                except:
                    client.close()


server = GenerateServer(55555)
server.create_server()