import socket
import select
import sys


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print('Incorrect params! Use IP address, port number')
    exit()

ip_address = str(sys.argv[1])
port = int(sys.argv[2])
client.connect((ip_address, port))

while True:
    sockets_list = [sys.stdin, client]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == client:
            message = socks.recv(1024)
            print(message)
        else:
            message = sys.stdin.readline()
            client.send(message)
            sys.stdout.write('<You>')
            sys.stdout.write(message)
            sys.stdout.flush()
client.close()