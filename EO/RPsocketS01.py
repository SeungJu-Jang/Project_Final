#-*-coding:utf-8-*-
import socket

HOST = '192.168.0.214'
PORT = 9000 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen(1)
client_socket, addr = server_socket.accept()
print('Connected by', addr)

while True:

    data = client_socket.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지합니다. 
    if not data:
        break
    
    dataget=data.decode("utf-8")

    print('Received from', addr, dataget)
    
    client_socket.send(data)


client_socket.close()
server_socket.close()