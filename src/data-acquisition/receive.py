import csv
import argparse
import socket

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument("-h", "--host")
parser.add_argument("-p", "--port", type=int)
parser.add_argument("-f", "--filename")

args = parser.parse_args()
host = args.host
port = args.port
filename = args.filename

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
# s.listen(1)
# conn, addr = s.accept()

file = open(filename, "w")

# with conn:
#     print("Connected by: ", addr)
while True:
    reading = s.recvfrom(1024)
    data = reading[0].decode('utf8')
    print("Receiving...", data)
    file.write(data+"\n")
    if not data:
        file.close()
        break


