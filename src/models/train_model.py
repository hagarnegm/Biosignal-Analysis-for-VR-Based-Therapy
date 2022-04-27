import pickle as pkl
from src.models.utils import *

data_dir = r"C:\Users\Hagar\Desktop\Dataset\Final"
feature_set = ["skewness", "rms", "iemg", "ar_coeff", "hjorth", "mav", "zc", "ssc", "wl"]
win_size = 200
win_stride = 50

callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

train_emg, test_emg, y_train, y_test = generate_dataset(data_dir, feature_set, win_size, win_stride)

X_train_scaled, X_test_scaled, y_train = transform_dataset(train_emg, test_emg, y_train)

model = build_model()

model_hist = model.fit(X_train_scaled, y_train, batch_size=32, epochs=48, callbacks=[callback], validation_split=0.3)

pkl.dump(model, open('../../models/dnn_model.sav', 'wb'))