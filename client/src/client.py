import socket
import ssl

context = ssl.create_default_context()
context.load_verify_locations('server/res/cert/cert.pem')
# print(context.get_ciphers())
print("LOL")
HOST = "localhost"  # The server's hostname or IP address
PORT = 65433  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        print(ssock.version())
    #ssock.connect((HOST, PORT))
        ssock.send(b"Hello, world")
        data = ssock.recv(1024)

print(f"Received {data!r}")