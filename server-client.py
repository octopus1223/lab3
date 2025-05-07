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