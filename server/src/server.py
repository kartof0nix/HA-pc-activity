import socket
import ssl
import json

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 65439  # Port to listen on (non-privileged ports are > 1023)
SSL=True

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./server/res/cert/cert.pem', './server/res/cert/key.pem')

known_devices = {"karol-hp" : "3gdf8ug"}
states = {}
# cipher = 'DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256'
# context.set_ciphers(cipher)

#print(context.get_ciphers())

print("redy..")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    if(SSL):
        s = context.wrap_socket(sock, server_side=True)
    else:
        s = sock
    

    while True:
        conn, addr = s.accept()

        with conn:
            print(f"Connected by {addr}")
            rcv = b""
            while True:
                d = conn.recv(1024)
                if not d:
                    break
                rcv += d
                conn.send(b"OK")

        
        data = json.loads(rcv.decode('utf-8'))
        
        if(data['name'] not in known_devices):
            print("Unknown device!")
            continue
        if(data['token'] != known_devices[data["name"]]):
            print("Invalid token!")
            continue
        
        states[data['name']] = data['data']

        print(states)
            #print("p")

    s.close()