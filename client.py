import socket
import threading
import rsa
import utils

class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username
        self.public_key = ""
        self.private_key = ""
        self.serverkey = ""

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        # create key pairs

        self.public_key, self.private_key = rsa.generate_keypair()

        # recieve server's public key

        self.serverkey = self.s.recv(1024).decode().split()

        # send client's public key to the server

        self.s.send(" ".join(self.public_key).encode())


        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self):
        while True:
            data = self.s.recv(1024).decode()
            message = data[:64]
            msg_hash = data[-64:]

            decrypted_message = rsa.decrypt(message, self.private_key)

            if msg_hash != utils.calculate_hash(decrypted_message):
                print("Hash mismatch!")

            print("Encrypted:", message)
            print("Decrypted:", decrypted_message)

    def write_handler(self):
        while True:
            message = input()

            encrypted_message = rsa.encrypt(message, self.serverkey)

            self.s.send(encrypted_message.encode())

if __name__ == "__main__":
    username = input("Enter your username: ")
    cl = Client("127.0.0.1", 9001, username)
    cl.init_connection()
