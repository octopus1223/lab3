import socket
import threading
from datetime import datetime, timedelta

class TupleSpaceServer:
    def __init__(self,port):
        self.port = port
        self.tuple_space = ()
        self.lock = threading.Lock()
        self.status = {
            "total_clients": 0,
            "total_operations": 0,
            "read": 0,
            "put": 0,
            "errors": 0
        }
        self.last_report_time = datetime.now()
    
    def Start(self):
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
                

            
