from scipy.signal import butter, lfilter, iirnotch, filtfilt, lfilter_zi

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    '''Low pass filter for a signal. Performs filter initialization
    to avoid spikes at the beginning.
    '''
    b, a = butter_lowpass(cutoff, fs, order=order)
    zi = lfilter_zi(b, a) * data[0]
    y = lfilter(b, a, data, zi=zi)
    return y[0]

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut=20, highcut=450, fs=1000, order=4):
    '''Band pass for a signal. Performs filter initialization
    to avoid spikes at the beginning.
    '''
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    zi = lfilter_zi(b, a) * data[0]
    y = lfilter(b, a, data, zi=zi)
    return y[0]
    
def notch_filter(data, f=50, Q=30, fs=1000):
    '''Notch filter to remove powerline interference.
    '''
    b, a = iirnotch(f, Q, fs)
    y = filtfilt(b, a, data)
    return y
