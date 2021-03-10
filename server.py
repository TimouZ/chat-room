import socket
import select
import sys
import threading
import logging
import argparse


args_parser = argparse.ArgumentParser(prog='TCP chat server',
                                      description='TCP chat server. Default ip: 127.0.0.1, port: 8081 ')
args_parser.add_argument('-ip',
                         type=str,
                         action='store',
                         dest='ip_address',
                         help='Server IP address',
                         default='127.0.0.1')
args_parser.add_argument('-port',
                         '-p',
                         type=int,
                         action='store',
                         dest='port',
                         help='Server port',
                         default=8081)
args_parser.add_argument('-c',
                         type=int,
                         action='store',
                         dest='connections',
                         help='Connections',
                         default='5')
args_parser.add_argument('-n',
                         type=str,
                         action='store',
                         dest='chat_room_name',
                         help='Room name',
                         default='Room #1')

args = args_parser.parse_args()

logging.basicConfig(level=logging.DEBUG,
                    filename='server.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((args.ip_address, args.port))
server.listen(args.connections)
logging.info(f'Started new server(room) {args.chat_room_name} on {args.ip_address}:{args.port}')

active_clients = []


def clientthread(conn, addr):
    conn.send(f'Welcome to {args.chat_room_name} chat room'.encode())
    while True:
        try:
            message = conn.recv(2048)
            if message:
                # Print user address and message
                print('<' + addr[0] + '>' + message)
                # Calls broadcast function to send message to all
                message_to_send = '<' + addr[0] + '>' + message
                broadcast(message_to_send, conn)
            else:
                remove_connection(conn)
        except:
            continue


def broadcast(message, connection):
    for clients in active_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove_connection(clients)


def remove_connection(connection):
    if connection in active_clients:
        active_clients.remove(connection)
        logging.info(f'{connection} removed')


def main():
    while True:
        conn, addr = server.accept()

        active_clients.append(conn)
        print(addr[0] + ' connected')
        logging.info(f'{addr[0]} connected')

        threading.Thread(target=clientthread,
                         args=(conn, addr)
                         ).start()

    conn.close()
    server.close()
    logging.info(f'Closed new server(room) {chat_room_name} on {ip_address}:{port}')


if __name__ == '__main__':
    main()
