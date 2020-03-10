#python3

import socket
import sys

HOST = '192.168.0.144'
PORT = 8080

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    msg=input()

    if msg == 'exit':
        print('Program Close')
        s.close()

    s.send(msg.encode(encoding='utf_8', errors='strict'))
    # data = s.recv(1024)
    print ('보낸 데이터 : ' + msg)

    data = s.recv(1024)
    print('받은 데이터 : ', data.decode('utf_8'))
