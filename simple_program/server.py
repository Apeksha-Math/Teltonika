import socket

def start_server(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    
    # Listen for incoming connections (max 5 clients in the queue)
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}")
    
    while True:
        # Wait for a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        # Receive data from the client
        client_data = client_socket.recv(1024).decode('utf-8')
        if client_data:
            print(f"Received message from client: {client_data}")
            
            # Echo the message back to the client
            client_socket.sendall(client_data.encode('utf-8'))
        
        # Close the connection with the client
        client_socket.close()

if __name__ == "__main__":
    # Define the host and port on which the server will run
    host = "127.0.0.1"  # Localhost
    port = 12345
    
    # Start the server
    start_server(host, port)
