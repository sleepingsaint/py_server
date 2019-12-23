import socket
import select
from time import strftime, gmtime

# defining IP address and PORT number
IP            = "127.0.0.1"
PORT          = 8080
HEADER_LENGTH = 10

# creating and initializing socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

print(f'chat server is listening on {IP}:{PORT}')

# sockets to listen for incoming connections
readable_sockets = [server_socket]

# dict to store users info
clients_info = {}

# all the good stuff : recieving and closing connections, adding users, showing and relaying messages
while True:
    readable, writable, exception = select.select(readable_sockets, [], [])
    for temp_sock in readable:

        # accepting new connection
        if temp_sock == server_socket:
            client_socket, client_address = server_socket.accept()
            message_length = client_socket.recv(HEADER_LENGTH).decode()
            username = client_socket.recv(int(message_length))
            readable_sockets.append(client_socket)
            clients_info[client_socket] = username.decode()
            print(f'{clients_info[client_socket]} has joined the chat')
        
        # existing client connection 
        else:
            try:
                message_length = temp_sock.recv(HEADER_LENGTH).decode()
                
                # client closing the connection / socket 
                if not len(message_length):
                    print(f'{clients_info[temp_sock]} has left the server :(')
                    temp_sock.close()
                    readable_sockets.remove(temp_sock)
                    del clients_info[temp_sock]
                
                # receiving the client message
                else:
                    message = temp_sock.recv(int(message_length)).decode()
                    print(f'{clients_info[temp_sock]} > {message}')
                    for other_client in readable_sockets:
                        if other_client != server_socket and other_client != temp_sock:
                            other_client.send((f'{len(message):<{HEADER_LENGTH}}' + message).encode()) 

            # client forcibly closing the session i.e. closing the window
            except ConnectionResetError as e:
                print(f'{clients_info[temp_sock]} has left the server :(')
                temp_sock.close()
                readable_sockets.remove(temp_sock)
                del clients_info[temp_sock]
