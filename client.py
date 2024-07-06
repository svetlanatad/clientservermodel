import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection.connect((socket.gethostname(), 8000))

while True:

    message = connection.recv(1024)
    print(message.decode("utf-8"))
