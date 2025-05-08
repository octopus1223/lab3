if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "server":
        port = int(input("Enter server port(50000-59999):"))
        if 50000 <= port <= 59999:
            server = TupleSpaceServer(port)
            server.start()
        else:
            print("Port must ba between 50000 and 59999")
            