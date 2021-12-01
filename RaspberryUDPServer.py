import socket
from datetime import datetime

UDP_IP = "192.168.4.1"
UDP_PORT = 1234

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))


while True:
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S:%f")
    
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print("received message: %s" % data ,current_time)
