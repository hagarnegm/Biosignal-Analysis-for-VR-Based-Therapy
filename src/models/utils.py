from datetime import datetime
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from imblearn.under_sampling import RandomUnderSampler

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from tensorflow import keras
from keras import Sequential, layers, initializers, optimizers, losses

from src.data.dataset import *


def generate_dataset(data_dir, feature_set, win_size, win_stride, is_td=True):
    start = datetime.now()
    dataset = EmgDataset(data_dir, win_size, win_stride, feature_set, is_td)
    end = datetime.now()

    print("Feature Extraction Time per Window: ",
          ((end - start).total_seconds() * 1000) / dataset.extracted_features.shape[0])

    emg_features = dataset.extracted_features
    labels = dataset.rolled_labels
    reps = dataset.rolled_repetition

    train_rows = np.isin(reps, ['1', '3', '4']).ravel()
    test_rows = np.isin(reps, ['2']).ravel()

    train_emg = emg_features[train_rows]
    y_train = labels[train_rows].ravel()

    test_emg = emg_features[test_rows]
    y_test = labels[test_rows].ravel()

    print(f"X_train shape: {train_emg.shape} y_train shape: {y_train.shape}")
    print(f"X_test shape: {test_emg.shape} y_test shape: {y_test.shape}")

    y_train = y_train[~np.isnan(train_emg).any(axis=1)]
    train_emg = train_emg[~np.isnan(train_emg).any(axis=1)]

    y_test = y_test[~np.isnan(test_emg).any(axis=1)]
    test_emg = test_emg[~np.isnan(test_emg).any(axis=1)]

    return train_emg, test_emg, y_train, y_test


def transform_dataset(train_emg, test_emg, y_train):
    undersampler = RandomUnderSampler(random_state=0)
    X_train_under, y_train_under = undersampler.fit_resample(train_emg, y_train)

    X_train, y_train = shuffle(X_train_under, y_train_under, random_state=0)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(test_emg)

    return X_train_scaled, X_test_scaled, y_train


def build_model():
    model = Sequential()
    model.add(layers.Dense(128, kernel_initializer=initializers.HeNormal(), activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(192, kernel_initializer=initializers.HeNormal(), activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(320, kernel_initializer=initializers.HeNormal(), activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.1))
    model.add(layers.Dense(6, activation="softmax"))

    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
                  loss=keras.losses.SparseCategoricalCrossentropy(), metrics=["accuracy"])

    return model


def evaluate_model(y_test, predictions):
    acc = accuracy_score(y_test, predictions.argmax(axis=1))
    balanced_acc = balanced_accuracy_score(y_test, predictions.argmax(axis=1))
    return acc, balanced_acc


def plot_results(y_test, predictions):
    print(classification_report(y_test, predictions.argmax(axis=1)))
    cm = confusion_matrix(y_test, predictions.argmax(axis=1))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    disp.plot(ax=ax)
    plt.show()