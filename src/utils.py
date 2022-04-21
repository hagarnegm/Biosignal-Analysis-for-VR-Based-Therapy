import re
import os
import numpy as np
from urllib3 import encode_multipart_formdata

exercise_names = {"hc": 1,
                  "ok": 2,
                  "vict": 3,
                  "we": 4,
                  "wf": 5}
                  
def encode_labels(data, ex_name):
    """
    Encodes a binary array of active/rest areas to its corresponding exercise label.
    :param data: numpy array containing binary values of rest/activity.
    :param ex_name: name of the performed exercise.
    :return: numpy array
    """
    ex_name = ex_name.lower()
    enc_data = data.copy()
    enc_data[data == 1] = exercise_names[ex_name] 
    return enc_data

def extract_ex_info(path):
    """
    Extract subject name, exercise name, and trial number from a file path.
    :param path: path pointing to data file.
    :return: dict containing extracted info.
    """
    info = {}
    split_path = path.split(os.path.sep)
    file_name = split_path[-1]
    subject_name = split_path[-2]
    ex_name = file_name.split('-')[0]
    trial_num = re.findall(r"\d+", file_name.split('-')[1])[0]
    
    info["subject_name"] = subject_name
    info["ex_name"] = ex_name
    info["trial_num"] = trial_num

    return info