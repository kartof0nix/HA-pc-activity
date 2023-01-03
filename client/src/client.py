import socket
import ssl
import subprocess
import time
# import json

pattern = {"wifi":"nmcli -g name connection show --active"}

HOST = "localhost"  # The server's hostname or IP address
PORT = 65439  # The port used by the server
NAME="karol-hp"
TOKEN="3gdf8ugg"

SSL=True
UPDATE_FRQ = 5

def connect_and_send(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        if(ssl):
            s = context.wrap_socket(sock, server_hostname=HOST)
            print(s.version())
        else:
            s = sock

        s.send(bytes(data, 'utf-8'))
        rcv = s.recv(1024)
        s.close()
    return rcv


context = ssl.create_default_context()
context.load_verify_locations('server/res/cert/cert.pem')


while True:
    payload = {"name" : NAME, "token" : TOKEN}
    data = {}

    for cm in pattern:
        print(pattern[cm])
        p = subprocess.run(pattern[cm].split(" "), capture_output=True)
        out = p.stdout.decode('utf-8')
        out = out.replace('\n', '') #Remove trailing newline
        data |= {cm : out}


    payload |= {"data" : data}

    print(payload)

    print(connect_and_send(payload.__str__().replace("'", '"')))

    time.sleep(UPDATE_FRQ)




print(f"Received {data!r}")