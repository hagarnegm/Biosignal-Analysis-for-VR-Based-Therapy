import time
import timeit

def prediction_time(data_features, model):
    pred_t_start = timeit.default_timer()
    pred = model.predict(data_features[:1]) # prediction time for only one record
    pred_t_end = timeit.default_timer()
    print(f'prediction time: {pred_t_end - pred_t_start}')
    