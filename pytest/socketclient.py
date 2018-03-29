import socket

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 8888))

    result = sock.recv(1024)
    print result

    data = "some data this is very funny./p\n"
    sock.sendall(data)
    result = sock.recv(1024)
    print result
    sock.close()
