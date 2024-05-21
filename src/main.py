import socket
import asyncio
import datetime
import configparser
import threading
from logger import Logger
from redis_uploader import RedisUploader

class Server:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.redis_uploader = RedisUploader()
        self.server_port = self.config.getint('Server', 'port')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setblocking(False)
        self.server_socket.bind(('0.0.0.0', self.server_port))
        self.server_socket.listen()
        print(f"Server listening on port {self.server_port}")
        self.clients = []
        self.lock = threading.Lock()
        self.logger = Logger()

    async def handle_client(self, client_socket):
        try:
            while True:
                try:
                    data = await asyncio.to_thread(client_socket.recv, 2048)
                    if not data:
                        print("No data received, sleeping for 1 minute.")
                        await asyncio.sleep(60)  # Sleep for 1 minute if no data is received
                        continue

                    acknowledgment = b'\x01'
                    await asyncio.to_thread(client_socket.sendall, acknowledgment)
                    inserted_time = datetime.datetime.now()
                    hex_data = data.hex()
                    print(f"Received data: {hex_data}")

                    self.redis_uploader.upload_record("Teltonika", hex_data)
                    self.logger.log("RawData", f"RawData: {hex_data}", log_level="INFO")

                except BlockingIOError:
                    await asyncio.sleep(0.1)  # Give time for the socket to be ready again

        except Exception as e:
            self.logger.log("HandleClientError", f"Error handling Device: {e}", log_level="INFO")
            print(f"Error: {e}")

    async def client_acceptance(self):
        loop = asyncio.get_event_loop()
        while True:
            client_socket, client_address = await loop.sock_accept(self.server_socket)
            print(f"Accepted connection from {client_address}")
            with self.lock:
                self.clients.append((client_socket, client_address))
                asyncio.create_task(self.handle_client(client_socket))

    def start_server(self):
        try:
            asyncio.run(self.main_server())
        except KeyboardInterrupt:
            self.logger.log("ServerShutdown", "Server shutting down.", log_level="INFO")
            self.server_socket.close()

    async def main_server(self):
        await self.client_acceptance()

if __name__ == "__main__":
    server = Server()
    server.start_server()
