import socket
import logging
from threading import Thread

logging.getLogger().setLevel(logging.INFO)


class Server:
    server_clients = []

    # Create a TCP socket over IPv4.
    def __init__(self, HOST: str, PORT: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(20)
        logging.info('Server waiting for connection....')

    # Listen for connections on the main thread. When a connection
    # is received, create a new thread to handle it and add the client
    # to the list of clients.
    def listen(self):
        while True:
            client_socket, client_address = self.socket.accept()
            logging.info("Connection from: " + str(client_address))

            # The first message will be the username
            client_name = client_socket.recv(1024).decode()
            client_full_name = client_name + \
                " (IP: " + client_address[0] + \
                ", port: " + str(client_address[1]) + ")"
            client = {
                'client_name': client_name,
                'client_address': client_address,
                'client_socket': client_socket,
                'client_full_name': client_full_name
            }

            # Broadcast that the new client has connected
            self.broadcast_message(
                client_name, client_full_name + " has joined the session!")

            Server.server_clients.append(client)
            logging.info(f'Clients list updated to {self.server_clients}')
            Thread(target=self.handle_new_client, args=(client,)).start()

    def handle_new_client(self, client: dict):
        client_name = client['client_name']
        client_socket = client['client_socket']
        client_full_name = client['client_full_name']
        while True:
            # Listen out for messages and broadcast the message to all clients.
            client_message = client_socket.recv(1024).decode()
            # If the message is quit, remove the client from the list of clients and
            # close down the socket.
            if client_message.strip().endswith("quit"):
                self.broadcast_message(
                    client_name, client_full_name + " has left the session!")
                Server.server_clients.remove(client)
                logging.info(f'Clients list updated to {self.server_clients}')
                client_socket.close()
                break
            else:
                # Send the message to all other clients
                full_client_message = client_full_name + ": \n " + client_message
                self.broadcast_message(client_full_name, full_client_message)

    # Loop through the clients and send the message down each socket.
    # Skip the socket if it's the same client.
    def broadcast_message(self, sender_name: str, message: str):
        for client in self.server_clients:
            client_socket = client['client_socket']
            client_full_name = client['client_full_name']
            if client_full_name != sender_name:
                client_socket.send(message.encode())
            else:
                own_message = message.replace(sender_name, "You", 1)
                client_socket.send(own_message.encode())


if __name__ == '__main__':
    server = Server('127.0.0.1', 1337)
    server.listen()
