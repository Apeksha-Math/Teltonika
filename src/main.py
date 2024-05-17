import socket
import asyncio
import datetime
import configparser
import threading
from logger import Logger

class Server:
    def __init__(self, config_file='D:\\Apeksha\\APRIL\\14-05-24\\Teltonika_socket_pgm\\src\\config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        # self.client = DynamicSender()
        # self.redis_uploader = RedisUploader()
        self.server_host = self.config.get('Server', 'host')
        self.server_port = self.config.getint('Server', 'port')
        self.max_clients = self.config.getint('Server', 'max_clients')
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_host, self.server_port))
        self.server_socket.listen(self.max_clients)

        print(f"Server listening on {self.server_host}:{self.server_port}")
        self.clients = []
        self.lock = threading.Lock()
        self.logger = Logger()

    async def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(2048).strip()
                if not data:
                    break

                acknowledgment = b'\x01'
                client_socket.sendall(acknowledgment)

                inserted_time = datetime.datetime.now()               
                hex_data = data.hex()
                print(hex_data)
                # self.redis_uploader.upload_record("Teltonika", hex_data)
                self.logger.log("RawData", f"RawData: {hex_data}", log_level="INFO")  
                

        except Exception as e:
            self.logger.log("HandleClientError", f"Error handling Device {e}", log_level="INFO")                      

        finally:
            with self.lock:
                for client_info in self.clients:
                    if client_info[0] == client_socket:
                        self.clients.remove(client_info)
                        pass
                        

    async def client_acceptance(self):
        loop = asyncio.get_event_loop()
        while True:
            client_socket, client_address = await loop.sock_accept(self.server_socket)
            if len(self.clients) < self.max_clients:
                client_handler_task = asyncio.create_task(self.handle_client(client_socket))
                self.clients.append((client_socket, client_address))
            else:
                print("Maximum number of clients reached. Connection rejected.")
                client_socket.close()

    def start_server(self):
        try:
            asyncio.run(self.main_server())
        except KeyboardInterrupt:
            self.logger.log("HandleClientError", f"Server shutting down.", log_level="INFO") 
        

    async def main_server(self):
        await asyncio.gather(self.client_acceptance())    

if __name__ == "__main__":
    server = Server()
    server.start_server()
   



