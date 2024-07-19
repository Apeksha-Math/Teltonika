import tkinter as tk
import socket
import logging

# Configure logging
logging.basicConfig(filename='socket_communication.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Application")

        self.create_widgets()

    def create_widgets(self):
        # IP Address
        ip_label = tk.Label(self.root, text="Server IP Address:")
        ip_label.grid(row=0, column=0, padx=10, pady=10)
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=10)

        # Port
        port_label = tk.Label(self.root, text="Server Port:")
        port_label.grid(row=1, column=0, padx=10, pady=10)
        self.port_entry = tk.Entry(self.root)
        self.port_entry.grid(row=1, column=1, padx=10, pady=10)

        # Messages Label
        messages_label = tk.Label(self.root, text="Message:")
        messages_label.grid(row=2, column=0, padx=10, pady=10)

        # Messages Text Area
        self.messages_text = tk.Text(self.root, height=10, width=40)
        self.messages_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Send Button
        send_button = tk.Button(self.root, text="Send", command=self.send_message)
        send_button.grid(row=4, column=0, columnspan=2, pady=10)

    def send_message(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        message = self.messages_text.get("1.0", tk.END).strip()  # Get all text from the Text widget

        try:
            # Validate IP and port
            if not ip:
                raise ValueError("Server IP Address cannot be empty")
            if not port:
                raise ValueError("Server Port cannot be empty")
            port = int(port)  # Convert port to integer

            # Create a socket connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))

            # Send message
            if message:
                client_socket.sendall(message.encode())

            # Receive response from server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Received response from server: {response}")

            # Log the sent message and received response
            logging.info(f"Sent: {message}")
            logging.info(f"Received: {response}")

            # Close the socket
            client_socket.close()

        except ValueError as ve:
            error_message = f"Error: {ve}"
            print(error_message)
            logging.error(error_message)
        except socket.error as se:
            error_message = f"Socket error: {se}"
            print(error_message)
            logging.error(error_message)
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            logging.error(error_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
