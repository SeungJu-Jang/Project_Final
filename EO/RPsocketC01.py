#-*-coding:utf-8-*-
import socket

HOST = '192.168.0.%'
PORT = 80       

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()
client_socket, addr = server_socket.accept()

print('Connected by', addr)


while True:

    data = client_socket.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지합니다. 
    if not data:
        break

    print('Received from', addr, data.decode())
    client_socket.sendall(data)


client_socket.close()
server_socket.close()