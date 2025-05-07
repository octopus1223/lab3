import socket
import threading
from datetime import datetime, timedelta

class TupleSpaceServer:
    #define the constructor
    def __init__(self,port):
        self.port = port
        self.tuple_space = ()
        self.lock = threading.Lock()
        #initialize the status of some indicators
        self.status = {
            "total_clients": 0,
            "total_operations": 0,
            "read": 0,
            "put": 0,
            "errors": 0
        }
        #initialize the time
        self.last_report_time = datetime.now()
    
    #define the main loop of server
    def Start(self):
        #Create and configure a socket 
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.blind(('0.0.0.0', self.port))
            s.listen()
            print(f"Server listening on the port{self.port}")

            while True:
                conn, addr = s.accept()
                self.status['total_clents'] += 1
                client_threads = threading.Thread(
                    target = self.handle_client,
                    args = (conn, addr)
                )
                client_threads.start()

                if datatime.now() - self.last_report_time >= timedelta(seconds = 10):
                    self.report_status()
                    self.last_report_time = detertime.now()
    #Use the client handling function
    def handle_client(self,conn,addr):
        with conn:
            print(f"Connected by{addr}")
            while True:
                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break

                    reponse = self.process_request(data)
                    conn.sendall(response.encode('utf-8'))

                except Exception as e:
                    print(f"Error with client{addr}:{e}")
                    break
        print(f"Client{addr} disconnected")