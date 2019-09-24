import socket, select, datetime
from _thread import *
import threading
import rollbar

rollbar.init('bcabca58d8084e6592c9e233b5ae81e5')
# rollbar.report_message('Rollbar is configured correctly in station')
logger = open("station.log", "w")

save_slaves = []
class SlaveThread(threading.Thread):
    def __init__(self,slaveAddress,slavesocket):
        threading.Thread.__init__(self)
        self.csocket = slavesocket
        self.slaveAddress = slaveAddress
        print ("New connection added: ", self.slaveAddress)

    def broadcast(self, msg):
        for slave in save_slaves:
            #if slave != self.csocket:
            slave.send(msg)

    def run(self):
        self.runStation()

    def runStation(self):
        print ("Connection from : ", self.slaveAddress)
        msg = ''
        while True:
            # data received from slave
            data = self.csocket.recv(2048)
            if not data:
                print('bye')
                break
            print ("from slave", data)
            self.broadcast(data)
        # connection closed
        print ("Slave at ", self.slaveAddress , " disconnected...")
        save_slaves.remove(self.csocket)
        self.csocket.close()

LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)
server.bind((LOCALHOST, PORT))
server.listen(1)

print("Server started")
print("Waiting for slave request..")
while True:
    select.select([server], [], [], 1.0)
    # establish connection with slave
    try:
        slavesock, slaveAddress = server.accept()
        print('Connected to :', slaveAddress[0], ':', slaveAddress[1])
        slavesock.send("Connection Establised!".encode('ascii'))
        save_slaves.append(slavesock)
        slave = SlaveThread(slaveAddress, slavesock)
        slave.start()
    except BlockingIOError as e:
        pass
        # rollbar.report_message("Got BlockingIOError in runSlave loop!")
    except Exception as e:
        rollbar.report_exc_info()
        logger.write("Exception raised at " + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " Reason: " + str(e) + "\n")
# server.close()
