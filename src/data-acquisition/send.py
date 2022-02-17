import socket
import random

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((ip, port))

print("Connecting to....", ip, port)
file = open("send.csv", "w")
while 1:
    sig = random.randint(0, 1023)
    data = str(sig) + "," + str(sig)
    file.write(data + "\n")
    print("Sending...", data)
    s.sendto(data.encode('utf8'), (ip, port))
