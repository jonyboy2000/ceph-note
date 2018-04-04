服务器
```
import socket
import os
server_address = './uds_socket'
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        while True:
            data = connection.recv(16)
            if data == "Status":
                connection.sendall("OK")
            else:
                connection.sendall("NOT Support")
            break
    finally:
        connection.close()
```

客户端
```
import socket
import sys
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = './uds_socket'
try:
    sock.connect(server_address)
except socket.error, msg:
    sys.exit(1)
try:
    message = 'Status'
    sock.sendall(message)
    amount_received = 0
    amount_expected = len(message)
    data = sock.recv(16)

    while data:
        print data
        data = sock.recv(16)

finally:
    sock.close()
```
