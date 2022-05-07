import pickle
from pyexpat import features
import socket
import keras
import numpy as np
import time


from src.features.extract_features import *
from src.data.dataset import *

# unity connection 
host, port = '127.0.0.1', 25002  # identify the host address and its port 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #creating streaming object from socket
sock.connect((host, port))

# Main Variables
data_dir = r"../../data/Semi-final data" # to be edited
feature_set = ["skewness", "rms", "iemg", "ar_coeff", "hjorth", "mav", "zc", "ssc", "wl"]
model = pickle.load(open('../../models/rf.sav', 'rb'))

#functions
def __get_data_valid(data_dir, feature_set):
    dataset = EmgDataset(data_dir, win_size = 200, win_stride = 50, feature_set = feature_set, is_td = True)
    emg_features = dataset.extracted_features
    labels = dataset.rolled_labels
    reps = dataset.rolled_repetition
    train_rows = np.isin(reps, ['1', '2', '3', '4']).ravel()
    valid_idxs = ~np.isnan(emg_features).any(axis=1)
    #emg_features = emg_features[valid_idxs]
    features = emg_features[valid_idxs]
    
    return features

# prediction and sending
def predict_and_send(data_dir, feature_set):
    data = __get_data_valid(data_dir, feature_set)
    pred = model.predict(data)
    sock.sendall(str(pred).encode("UTF-8")) # for RF model
    #sock.sendall(str(np.argmax(pred)).encode("UTF-8")) # for DNN model
    #time.sleep(0.200)