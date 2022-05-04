import pickle
import socket
import keras
import numpy as np
import time

# unity connection 
host, port = '127.0.0.1', 25002  # identify the host address and its port 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #creating streaming object from socket
sock.connect((host, port))

# model loading
model = pickle.load(open('../../models/rf.sav', 'rb'))

# prediction and sending
def predict_and_send(data):
    pred = model.predict(data)
    sock.sendall(str(pred).encode("UTF-8")) # for RF model
    #sock.sendall(str(np.argmax(pred)).encode("UTF-8")) # for DNN model
    #time.sleep(0.200)