import socket, threading
import time, select, datetime
import multiprocessing, sys, os
import rollbar

rollbar.init('bcabca58d8084e6592c9e233b5ae81e5')
# rollbar.report_message('Rollbar is configured correctly in slave')
logger = open("slave.log", "w")

class SlaveInputProcess():
    def __init__(self, station_response):
        self.station_response = station_response
        forked_process = multiprocessing.Process(target=self.runSlave)
        forked_process.daemon=True #To close all child process fd's
        forked_process.start()
        self.child_pid = forked_process.pid

    def runSlave(self):
        while True:
            try:
                data = self.station_response.recv(1024)
                if data == 'bye':
                    os.kill(self.child_pid, signal.SIGTERM)
                print('Received from the server :',str(data.decode('ascii')))
            except BlockingIOError:
                pass
            except Exception as e:
                rollbar.report_exc_info()
                logger.write("Exception raised at " + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + " Reason: " + str(e) + "\n")
        self.station_response.close()

class StationResponseThread(threading.Thread):
    def __init__(self, station_response):
        threading.Thread.__init__(self)
        self.station_response = station_response

    def run(self):
        message=""
        while True:
            message = input()
            if message == 'bye':
                self.station_response.send(message.encode('ascii'))
                self.station_response.close()
                break
            self.station_response.send(message.encode('ascii'))

def Main():
    host = '127.0.0.1'
    port = 8080
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host, port))
    select.select([], [s], [], 1.0)
    data = s.recv(1024)
    print('Received from the server :', str(data.decode('ascii')))
    station_response = StationResponseThread(s)
    slave_input_process = SlaveInputProcess(s)
    station_response.start()

if __name__ == '__main__':
    Main()
