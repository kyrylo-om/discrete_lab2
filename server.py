import socket
import threading
import rsa
import utils

class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.public_key = ""
        self.private_key = ""
        self.username_lookup = {}
        self.client_keys = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        self.public_key, self.private_key = rsa.generate_keypair(4)

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}', c)
            self.username_lookup[c] = username
            self.clients.append(c)

            # send server's public key

            c.send(" ".join(map(str, self.public_key)).encode())

            # receive client's public key

            clientkey_public = list(map(int, c.recv(1024).decode().split()))
            print(f"{username}'s public key:", list(clientkey_public))
            self.client_keys[c] = clientkey_public

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str, c):
        for client in self.clients:
            if client != c:
                # calculate hash
                msg_hash = utils.calculate_hash(msg)

                encrypted_message = rsa.encrypt(msg, self.client_keys[client])

                client.send((msg_hash + encrypted_message).encode())

    def handle_client(self, c: socket, addr): 
        while True:
            msg = c.recv(1024)
            decrypted_message = rsa.decrypt(msg, self.private_key)
            self.broadcast(decrypted_message, c)

if __name__ == "__main__":
    s = Server(9001)
    s.start()
