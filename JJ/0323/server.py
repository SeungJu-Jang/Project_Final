from threading import *
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import testtt

# stock_num = manager_menu_stockmenu.stock_num()

class Signal(QObject):
    conn_signal = pyqtSignal()
    recv_signal = pyqtSignal(str)


class ServerSocket:
    def __init__(self, parent):


        self.parent = parent
        self.bListen = False
        self.clients = []
        self.ip = []
        self.threads = []

        self.conn = Signal()
        self.recv = Signal()

        self.conn.conn_signal.connect(self.parent.updateClient)
        self.recv.recv_signal.connect(self.parent.updateMsg)

    def __del__(self):
        self.stop()

    def start(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)

        try:
            self.server.bind((ip, port))
        except Exception as e:
            print('Bind Error : ', e)
            return False
        else:
            self.bListen = True
            self.t = Thread(target=self.listen, args=(self.server,))
            self.t.start()
            print('Server Listening...')

        return True

    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print('Server Stop')

    def listen(self, server):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()
            except Exception as e:
                print('Accept() Error : ', e)
                break
            else:
                self.clients.append(client)
                self.ip.append(addr)
                self.conn.conn_signal.emit()
                t = Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()

        self.removeAllClients()
        self.server.close()

    def receive(self, addr, client):
        while True:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                msg = str(recv, encoding='utf-8')
                if msg:
                    self.send(msg)
                    self.recv.recv_signal.emit(msg)
                    print('[RECV]:', addr, msg)

                    if msg == '0':
                        print('0')
                        self.send('0')

                    if msg == '1':
                        print('1')

                    if msg == '2':
                        print('2')

                    if msg == '3':
                        print('3')

                    if msg == '4':
                        print('4')

                    if msg == '5':
                        print('5')

                    if msg == '6':
                        print('6')

                    if msg == '7':
                        print('7')
                        self.send(testtt.manager_menu_stockmenu.li_num)
                        # self.send()
                    if msg == '8':
                        print('8')

                    if msg == '9':
                        print('9')

                    if msg == '10':
                        print('10')

                    if msg == '11':
                        print('11')

                    if msg == '12':
                        print('12')

                    if msg == '13':
                        print('13')




        self.removeCleint(addr, client)

    def send(self, msg):
        try:
            for c in self.clients:
                c.send(msg.encode('utf8'))
        except Exception as e:
            print('Send() Error : ', e)

    def removeCleint(self, addr, client):
        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)

        self.conn.conn_signal.emit()

        i = 0
        for t in self.threads[:]:
            if not t.isAlive():
                del (self.threads[i])
            i += 1

        self.resourceInfo()

    def removeAllClients(self):
        for c in self.clients:
            c.close()

        self.ip.clear()
        self.clients.clear()
        self.threads.clear()

        self.conn.conn_signal.emit()

        self.resourceInfo()

    def resourceInfo(self):
        print('Number of Client ip\t: ', len(self.ip))
        print('Number of Client socket\t: ', len(self.clients))
        print('Number of Client thread\t: ', len(self.threads))