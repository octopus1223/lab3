import sys
from server import TupleSpaceServer
from client import TupleSpaceClient


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "server":
        port = int(input("Enter server port(50000-59999):"))
        if 50000 <= port <= 59999:
            server = TupleSpaceServer(port)
            server.start()
        else:
            print("Port must ba between 50000 and 59999")
    elif len(sys.argv) == 4 and sys.argv[1] == "client":
        host = sys.argv[2]
        port = int(sys.argv[3])
        request_file = sys.argv[4]
        client = TupleSpaceClient(host, port, request_file)
        client.process_requests()
    else:
        print("Usage:")
        print("Server: python tuplespace.py server")
        print("Client: python tuplespace.py client <host><port><request_file>")