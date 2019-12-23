import sys
import socket
import select

# declaring IP address and PORT number
IP            = "127.0.0.1"
PORT          = 8080
HEADER_LENGTH = 10

# creating and initializing socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

# connecting and sending username
username = input('enter username : ')

try:
    client_socket.send((f'{len(username):<{HEADER_LENGTH}}' + username.strip()).encode())
    print(f'You are connected as {username}')

except socket.error as e:
    print('Oops an error occured!')

read_info = [sys.stdin, client_socket]
# sending messages to the server
while True:
    readable, writable, exceptional = select.select(read_info, [], [])
    for input_end in readable:
        if input_end == client_socket:
            try:
                relayed_message_length = client_socket.recv(HEADER_LENGTH).decode()
                relayed_message = client_socket.recv(int(relayed_message_length)).decode()
                print(f'friend > {relayed_message}')
            except socket.error as e:
                pass
        else:
            message = input(f'{username} > ')
            if message:
                client_socket.send((f'{len(message):<{HEADER_LENGTH}}' + message.strip()).encode())
    