import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from src.features.extract_features import *
from src.utils import *
import pandas as pd

# TODO: Use command pattern instead
# TODO: Add supported features to config file
supported_features = {"iemg": iemg, "mav": mav,
                      "mmav1": mmav1, "mmav2": mmav2,
                      "ssi": ssi, "rms": rms,
                      "wl": wl, "zc": zc,
                      "ssc": ssc, "wamp": wamp,
                      "kurtosis": kurtosis,
                      "skewness": skewness,
                      "var": variance,
                      "ar_coeff": ar_coefficients,
                      "hjorth": hjorth_params,
                      "mnf": mnf, "mdf": mdf, "mmnf": mmnf, "mmdf": mmdf}


class EmgDataset:
    def __init__(self, data_dir, win_size, win_stride, feature_set, is_td):
        self.data_dir = data_dir
        self.feature_set = feature_set
        self.win_size = win_size
        self.win_stride = win_stride
        self.is_td = is_td
        
        self.raw_emg = []
        self.rolled_emg = np.empty((0, self.win_size, 2), dtype=np.float64)

        self.subject_name = []
        self.rolled_subject_name = []
        self.repetition = []
        self.rolled_repetition = []

        self.labels = []
        self.rolled_labels = np.empty((0, 1), dtype=np.int32)

        self.reps = []
        self.extracted_features = None
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
                file_info = extract_ex_info(file_path)
                ex_name = file_info["ex_name"]
                subject_name = file_info["subject_name"]
                repetition = file_info["trial_num"]

                data = pd.read_csv(file_path)
                
                self.raw_emg.append(data.iloc[:, skip_cols:label_col].values)
                
                labels = data.iloc[:, label_col].values
                enc_labels = encode_labels(labels, ex_name)
                self.labels.append(enc_labels)

                self.subject_name.append(subject_name)
                self.repetition.append(repetition)

    def prepare_data(self):
        """
        Roll window on EMG data and labels, then extract features.
        :return: None
        """
        n_channels = self.raw_emg[0].shape[-1]
        for i in range(len(self.raw_emg)):
            trial_rolled_emg = np.dstack(self.roll_window(self.raw_emg[i][:, j])
                                         for j in range(n_channels))

            trial_rolled_labels = self.roll_window(self.labels[i])[:, 0]
            trial_rolled_labels = np.expand_dims(trial_rolled_labels, 1)
            
            trial_rolled_subject = [self.subject_name[i]] * trial_rolled_emg.shape[0]
            trial_rolled_repetition = [self.repetition[i]] * trial_rolled_emg.shape[0]

            self.rolled_emg = np.vstack([self.rolled_emg, trial_rolled_emg])
            self.rolled_labels = np.vstack([self.rolled_labels, trial_rolled_labels])
            self.rolled_subject_name.extend(trial_rolled_subject)
            self.rolled_repetition.extend(trial_rolled_repetition)

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
                if self.is_td:
                    extracted_features.append(feat_func(self.rolled_emg))
                else:
                    frequencies, power_spectrum = frequency_domain(self.rolled_emg)
                    extracted_features.append(feat_func(frequencies, power_spectrum))
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
        :return: numpy array after rolling window
        """
        y = sliding_window_view(data, self.win_size, axis=0)[::self.win_stride, :]
        return y

    def update_features(self, new_features):
        """
        Update features and prepare the data again.
        :param new_features: List containing new features
        :return: None
        """
        self.feature_set = new_features
        self.extracted_features = None
        self.extract_features()

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
