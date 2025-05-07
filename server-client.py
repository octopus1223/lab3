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
        def process_request(self,request):
            try:
                size = int(request[:3])
                cmd = request[4]
                remaining = request[5:].strip()

                self.status['total_ops'] += 1

                if cmd == "R":
                    self.status['read'] += 1
                    key = remaining
                    with self.lock:
                        if key in self.tuple_space:
                            value = self.tuple_space.pop(key)
                            return f"{len(f'OK({key},{value})removed')+3:03d}OK({key},{value})read"
                        else:
                            self.status["errors"]+= 1
                            return f"{len(f'ERR{key}does not exist')+3:03d}ERR{key} does not exist"
                elif cmd == "G":
                    self.stats["get"] += 1
                    key = remaining
                    with self.lock:
                        if key in self.tuple_space:
                            value = self.tuple_space.pop(key)
                            return f"{len(f'OK({key},{value})removed')+3:03d}OK{key} does not exist"
                        else:
                            self.stats['errors']+= 1
                            return f"{len(f'ERR{key}does not exist')+3:03d}ERR{key}does not exist"
                elif cmd == 'P':
                    self.stats['put'] += 1
                    parts = remaining.split(maxsplit = 1)
                    if len(parts)<2:
                        self.stats["errors"]+=1
                        return "005 ERR size exceed"
                    
                    key,value = parts
                    if len(key) + len(value) >970:
                        self.stats['errors'] += 1
                        return "005 ERR size exceed"
                    
                    with self.lock:
                        if key in self.tuple_space:
                            self.stats['errors']+= 1
                            return f'{len(f'ERR{key}already exosts')+3:03d}ERR{key} already exists'
                        else:
                            self.tuple_space[key] = value
                            return f"{len(f"OK({key},{value})added")+3:03d} OK({key},{value})adde"
            except Exception as e :
                self.stats["errors"] += 1
                return "005 ERR invalid request"