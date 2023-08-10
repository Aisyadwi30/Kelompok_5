import socket
import threading
import os

HOST = '10.217.17.205'
PORT = 12345

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode("utf-8"))
        except:
            break

def send_file(client_socket, file_path):
    file_type = file_path.split(".")[-1].lower()
    file_size = os.path.getsize(file_path)
    message = f"!file {file_type} {file_size}"
    client_socket.send(message.encode("utf-8"))

    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.send(data)

    print(f"File {file_path} sent successfully.")

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Input username from the client
    username = input("Enter your username: ")
    client_socket.send(username.encode("utf-8"))

    # Input groupname from the client
    groupname = input("Enter your group name: ")
    client_socket.send(groupname.encode("utf-8"))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()

        if message == "exit":
            client_socket.send(message.encode("utf-8"))
            break
        elif message.startswith("@"):
            parts = message.split(" ", 1)
            recipient = parts[0][1:]
            message = parts[1]
            full_message = "@{} {}".format(recipient, message)
        elif message.startswith("$"):
            parts = message.split(" ", 1)
            group = parts[0][1:]
            message = parts[1]
            full_message = "${} {}".format(group, message)
        elif message.startswith("!file"):
            file_path = message.split(" ")[1]
            send_file(client_socket, file_path)
            continue
        else:
            full_message = message

        client_socket.send(full_message.encode("utf-8"))

    client_socket.close()

if __name__ == "__main__":
    main()
