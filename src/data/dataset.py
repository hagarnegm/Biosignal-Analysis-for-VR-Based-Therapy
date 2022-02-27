import os
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from src.features.extract_features import *

# TODO: Use command pattern instead
# TODO: Add supported features to config file
supported_features = {"iemg": iemg, "mav": mav,
                      "mmav1": mmav1, "mmav2": mmav2, "mavslp": mavslp,
                      "ssi": ssi, "rms": rms,
                      "wl": wl, "zc": zc,
                      "ssc": ssc, "wamp": wamp,
                      "kurtosis": kurtosis,
                      "skewness": skewness,
                      "var": variance}


class EmgDataset:
    def __init__(self, data_dir, win_size, win_stride, feature_set):
        self.data_dir = data_dir
        self.feature_set = feature_set
        self.win_size = win_size
        self.win_stride = win_stride
        self.raw_emg = []
        self.rolled_emg = None
        self.labels = []
        self.rolled_labels = None
        self.reps = []
        self.rolled_reps = None
        self.extracted_features = None
        # file_names are just for debugging purposes, will be removed in the future
        self.file_names = []

        self.read_signals()
        self.prepare_data()

    def read_signals(self, skip_cols=0):
        """
        Read signals from data directory.
        :param skip_cols: Columns to skip (from beginning), like timestamp.
        :return: None
        """
        label_col = -1
        for root, dirs, files in os.walk(self.data_dir):
            for f in files:
                file_path = os.path.join(root, f)
                data = np.genfromtxt(file_path, delimiter=',')[:, skip_cols:]
                self.raw_emg.append(data[:, :label_col])
                self.labels.append(data[:, label_col])
                self.file_names.append(file_path.split("/")[-1])

    def prepare_data(self):
        """
        Roll window on EMG data and labels, then extract features.
        :return: None
        """
        n_channels = self.raw_emg[0].shape[-1]
        self.rolled_emg = np.empty((0, self.win_size, n_channels))
        self.rolled_labels = np.empty((0, 1))

        for i in range(len(self.raw_emg)):
            trial_rolled_emg = np.dstack(self.roll_window(self.raw_emg[i][:, j])
                                         for j in range(n_channels))
            trial_rolled_labels = self.roll_window(self.labels[i])[:, 0]
            trial_rolled_labels = np.reshape(trial_rolled_labels, (-1, 1))
            self.rolled_emg = np.vstack([self.rolled_emg, trial_rolled_emg])
            self.rolled_labels = np.vstack([self.rolled_labels, trial_rolled_labels])

        self.extract_features()

    def extract_features(self):
        """
        Extract features from EMG data after rolling window.
        :return: None
        """
        extracted_features = []
        for feature in self.feature_set:
            feat_func = supported_features.get(feature.lower(), None)
            if feat_func:
                extracted_features.append(feat_func(self.rolled_emg))
            else:
                print(f"Feature {feature} not supported yet")
        if len(extracted_features):
            self.extracted_features = np.hstack(extracted_features)
        else:
            print("No features have been extracted")

    def train_test_split(self, train_reps, test_reps):
        """
        Split data to training and testing by repetition number
        :param train_reps: List containing training repetition numbers
        :param test_reps: List containing test repetition numbers
        :return: None
        """
        pass

    # TODO: Consider moving this to utils
    def roll_window(self, data):
        """
        Roll window on data.
        :param data: 1-D numpy array containing data to roll window on
        :return: None
        """
        y = sliding_window_view(data, self.win_size, axis=0)[::self.win_stride, :]
        return y

    def update_features(self, new_features):
        """
        :param new_features: List containing new features
        :return: None
        Update features and prepare the data again.
        """
        self.feature_set = new_features
        self.prepare_data()

    def update_window(self, new_win_size, new_win_stride):
        """
        Update window size and stride and prepare the data again.
        :param new_win_size: int containing new window size
        :param new_win_stride: int containing new window string
        :return: None
        """
        self.win_size = new_win_size
        self.win_stride = new_win_stride
        self.prepare_data()
