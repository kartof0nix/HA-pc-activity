import socket
import ssl

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./server/res/cert/cert.pem', './server/res/cert/key.pem')

# cipher = 'DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256'
# context.set_ciphers(cipher)

#print(context.get_ciphers())

print("redy..")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    with context.wrap_socket(s, server_side=True) as ssock:

        while True:
            conn, addr = ssock.accept()

            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.send(data)
    s.close()