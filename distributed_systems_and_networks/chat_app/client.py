import socket
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext, simpledialog


class Client:
    def __init__(self):

        # Initialize GUI
        self.root = tk.Tk()
        self.root.title("Messenger Application")

        self.host = simpledialog.askstring(
            "IP Address", "Please enter the IP address you want to connect to:")
        self.port = simpledialog.askinteger(
            "Port", "Please enter the Port you want to connect to:")

        # Connect to the server
        self.socket = socket.socket()
        try:
            self.socket.connect((self.host, self.port))
        except ConnectionError as e:
            print(f"Failed to connect to server: {e}")
            return

        # Set up the main window (assuming self.root is your main window)
        # Allow row 0 to expand vertically
        self.root.grid_rowconfigure(0, weight=1)
        # Allow column 0 to expand horizontally
        self.root.grid_columnconfigure(0, weight=1)
        # Column 1 (Send button) does not expand
        self.root.grid_columnconfigure(1, weight=0)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self.root, state='disabled', wrap=tk.WORD, width=50, height=15)
        self.chat_display.grid(row=0, column=0, padx=10,
                               pady=10, columnspan=2, sticky="nsew")

        # Message entry box
        self.message_entry = tk.Entry(self.root, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.message_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(
            self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Prompt for username
        self.name = simpledialog.askstring("Username", "Enter your name:")
        if self.name:
            self.socket.send(self.name.encode())
            # Start the receive thread for incoming messages
            Thread(target=self.receive_message, daemon=True).start()
            # Start the Tkinter main loop
            print("Starting main loop with networking...")
            self.root.mainloop()
        else:
            print("Username entry canceled.")
            self.root.destroy()

    def send_message(self, event=None):
        client_message = self.message_entry.get()
        if client_message:
            self.socket.send(client_message.encode())
            self.message_entry.delete(0, tk.END)

    def receive_message(self):
        while True:
            try:
                server_message = self.socket.recv(1024).decode()
                if not server_message.strip():
                    print("Server message empty, exiting...")
                    self.root.quit()
                    break
                self.display_message(server_message)
            except OSError:
                # Socket was closed
                break

    def display_message(self, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state='disabled')


if __name__ == '__main__':
    Client()
