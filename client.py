import socket
import select
import sys
import argparse


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


args_parser = argparse.ArgumentParser(prog='TCP chat client',
                                      description='TCP chat client. Default ip: 127.0.0.1, port: 8081 ')
args_parser.add_argument('-ip',
                         type=str,
                         action='store',
                         help='Server IP address',
                         default='127.0.0.1')
args_parser.add_argument('-port',
                         '-p',
                         type=int,
                         action='store',
                         help='Server port',
                         default=8081)

args = args_parser.parse_args()

client.connect((args.ip, args.port))

while True:
    sockets_list = [sys.stdin, client]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == client:
            message = socks.recv(2048)
            print(message)
        else:
            message = sys.stdin.readline()
            client.send(message.encode())
            sys.stdout.write('<You>')
            sys.stdout.write(message)
            sys.stdout.flush()
client.close()
