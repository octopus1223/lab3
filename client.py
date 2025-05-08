import socket
import sys

class TupleSpaceClient:
    def __init__ (self,host,port,request_file):
        self.host = host
        self.port = port
        self.request_file = request_file
    
    def process_requests(self):
        try:
            with open(self.request_file,'r') as file:
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as s:
                    s.connect((self.host, self.port))

                    for line in file:
                        line = line.strip()
                        if not line:
                            continue


                        parts = line.split(maxsplit = 1)
                        if len(parts) <2:
                            print("Invalid request :{line}")
                            continue

                        cmd = parts[0]
                        remaining = parts[1]

                        if cmd == "PUT":
                            put_parts = remaining.split(maxsplit = 1)
                            if len(put_parts) < 2:
                                print(f"Invalid PUT format:{line}")
                                continue
                            key,value = put_parts
                            if len(key) + len(value) >970:
                                print(f"Size exceeded for:{line}")
                                continue
                            message = f"{len(f'P{key}{value}')+3:03d}P{key}{value}"
                        
                        elif cmd in ["READ","GET"]:
                            key = remaining 
                            if len(key) > 999:
                                print(f"Key is too long:{value}")
                                continue
                            prefix = 'R' if cmd == "READ" else 'G'
                            message = f"{len(f'{prefix}{key}') +3:03d}{prefix}{key}"
                        
                        else:
                            print(f"Unknown command:{cmd}")
                            continue

                        s.sendall(message.encode('utf-8'))
                        response = s.recv(1024).decode('utf-8')

                        if len(response) < 3:
                            print(f"Invalid response for:{line}")
                            continue

                        size = int(response[:3])
                        status = response[4:7]
                        details = response [7:].strip()

                        print(f"{line}:{status}{details}")
        except Exception as e:
            print(f"Error:{e}")




