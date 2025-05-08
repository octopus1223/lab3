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
    def start(self):
        #Create and configure a socket 
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', self.port))
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

                if datetime.now() - self.last_report_time >= timedelta(seconds = 10):
                    self.report_stats()
                    self.last_report_time = datetime.now()
    #Use the client handling function
    def handle_client(self,conn,addr):
        with conn:
            print(f"Connected by{addr}")
            while True:
                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break

                    response = self.process_request(data)
                    conn.sendall(response.encode('utf-8'))

                except Exception as e:
                    print(f"Error with client{addr}:{e}")
                    break
        print(f"Client{addr} disconnected")

    def process_request(self, request):
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
                        value = self.tuple_space[key]
                        return f"{len(f'OK({key},{value})removed') + 3:03d}OK({key},{value})read"
                    else:
                        self.status["errors"] += 1
                        return f"{len(f'ERR{key}does not exist') + 3:03d}ERR{key} does not exist"
            elif cmd == "G":
                self.status['get'] += 1
                key = remaining
                with self.lock:
                    if key in self.tuple_space:
                        value = self.tuple_space.pop(key)
                        return f"{len(f'OK({key},{value})removed') + 3:03d}OK{key} does not exist"
                    else:
                        self.status['errors'] += 1
                        return f"{len(f'ERR{key}does not exist') + 3:03d}ERR{key}does not exist"
            elif cmd == 'P':
                self.status['put'] += 1
                parts = remaining.split(maxsplit=1)
                if len(parts) < 2:
                    self.status["errors"] += 1
                    return "005 ERR size exceed"

                key, value = parts
                if len(key) + len(value) > 970:
                    self.status['errors'] += 1
                    return "005 ERR size exceed"

                with self.lock:
                    if key in self.tuple_space:
                        self.stats['errors'] += 1
                        return f"{len(f'ERR{key}already exists') + 3:03d}ERR{key} already exists"
                    else:
                        self.tuple_space[key] = value
                        return f"{len(f'OK({key},{value})added') + 3:03d} OK({key},{value})added"
        except Exception as e:
            self.stats["errors"] += 1
            return "005 ERR invalid request"


    def report_stats(self):
        with self.lock:
            total_tuples = len(self.tuple_space)
            avg_tuple_size = sum(len(k) + len(v) for k, v in self.tuple_space.items())/total_tuples if total_tuples > 0 else 0
            avg_key_size = sum(len(k) for k in self.tuple_space)/total_tuples if total_tuples>0 else 0
            avg_value_size = sum(len(v) for v in self.tuple_space.values())/total_tuples if total_tuples > 0 else 0

            print("\n=== Server Statistics ===")
            print(f"Tuples:{total_tuples}")
            print(f"Avg tuple size :{avg_tuple_size:.2f}")
            print(f"Avg key size:{avg_key_size:.2f}")
            print(f"Avg value size:{avg_value_size:.2f}")
            print(f"total clients:{self.status['total_clients']}")
            print(f"total operations:{self.status['total_operations']}")
            print(f"READS:{self.status['read']}")
            print(f"GETS:{self.status['get']}")
            print(f"PUTS:{self.status['put']}")
            print(f"Errors:{self.status['errors']}")
            print("======================\n")