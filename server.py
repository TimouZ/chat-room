import socket
import select
import sys
import threading
import logging


logging.basicConfig(level=logging.DEBUG,
                    filename='server.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 5:
    print('Incorrect params! Use IP address, port number, active connections, chat room name')
    exit()

ip_address = str(sys.argv[1])
port = int(sys.argv[2])
connections = int(sys.argv[3])
chat_room_name = str(sys.argv[4])

server.bind((ip_address, port))
server.listen(connections)
logging.info(f'Started new server(room) {chat_room_name} on {ip_address}:{port}')

active_clients = []

def clientthread(conn, addr):
    conn.send(f'Welcome to {chat_room_name} chat room')

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
try:
    while True:
        conn, addr = server.accept()

        active_clients.append(conn)
        print(addr[0] + ' connected')
        logging.info(f'{addr[0]} connected')

        threading
        threading.start_new_thread(clientthread, (conn, addr))
finally:
    conn.close()
    server.close()
    logging.info(f'Closed new server(room) {chat_room_name} on {ip_address}:{port}')