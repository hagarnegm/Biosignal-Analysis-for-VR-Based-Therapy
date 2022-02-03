import numpy as np
import scipy as sp


def iemg(data):
    """
    :param data: EMG signal samples within rolling window
    :return: Integrated EMG which is the summation of the absolute values of the EMG signal amplitude.
    It is used as an onset index to detect muscle activity.
    """
    return np.sum(np.abs(data), axis=1)


def mav(data):
    """
    :param data: EMG signal samples within rolling window
    :return: Mean Absolute Value which is the average of the absolute values of the EMG signal.
    It is used for the detection of muscle contraction levels.
    """
    return np.mean(np.abs(data), axis=1)


def variance(data):
    """
    :param data: EMG signal samples within rolling window
    :return: Variance which is the average of the square of the signal's deviation from the mean.
    It uses the signals power as a feature.
    """
    return np.var(data, axis=1)


def rms(data):
    """
    :param data: EMG signal samples within rolling window
    :return: Root Mean Square which is the standard deviation of the signal amplitude values.
    It is related to the constant force and non-fatiguing contraction of the muscle.
    """
    return np.sqrt(np.mean(data ** 2, axis=1))


def wl(data):
    """
    :param data: EMG signal samples within rolling window
    :return: Waveform Length which is the cumulative length of the waveform over the time segment.
    It is related to the waveform amplitude, frequency and time.
    """
    return np.sum(np.abs(np.diff(data, axis=1)), axis=1)


def zc(data):
    """
    :param data: EMG signal samples within rolling window
    :return: Zero Crossing which is the number of times the signal values cross zero.
    It provides an approximation of the signal frequency. The threshold used is for reducing the effect of noise.
    """
    return np.count_nonzero(np.diff(np.sign(data), axis=1), axis=1)


def ssc(data, th=0):
    """
    :param data: EMG signal samples within rolling window
    :param th: Threshold used to reduce noise effects
    :return: Slope Sign Changes which is the number of changes between positive and negative slopes of the signal.
    It also provides information about the signal frequency. The threshold used is for reducing the effect of noise.
    """
    return np.sum((-np.diff(data, prepend=1, axis=1)[:, 1:-1, :] * np.diff(data, axis=1)[:, 1:, :]) > th, axis=1)


def wamp(data, th=10):
    """
    :param data: EMG signal samples within rolling window
    :param th: Threshold used to reduce noise effects
    :return: Wilson's Amplitude which is the number of times that the difference between two consecutive signal segments
    passes a certain threshold, which is also used to reduce the effect of noise. WAMP is related to the firing of
    motor unit action potentials (MUAP) and the muscle contraction levels.
    """
    x = np.abs(np.diff(data, axis=1))
    above = x > th
    return np.sum(above, axis=1)


def kurtosis(data):
    """
    :param data: EMG signal samples within rolling window
    :return: Kurtosis which is a statistical measure that defines how the tails of a distribution differs
    from the tails of a normal distribution. It identifies the presence of extreme values in the EMG signal.
    """
    return sp.stats.kurtosis(data, axis=1)


def skewness(data):
    """
        :param data: EMG signal samples within rolling window
        :return: Skewness which measures the lack of symmetry of a distribution. It also identifies the
        presence of extreme values in the EMG signal.
        """
    return sp.stats.skew(data, axis=1)







