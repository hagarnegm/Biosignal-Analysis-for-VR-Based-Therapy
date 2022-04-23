import numpy as np
import scipy as sp
from scipy import signal
from nitime.algorithms.autoregressive import AR_est_YW


def iemg(data):
    """
    :param data: EMG signal samples within rolling window segment
    :return: Integrated EMG which is the summation of the absolute values of the EMG signal amplitude.
    It is used as an onset index to detect muscle activity.
    """
    return np.sum(np.abs(data), axis=1)


def mav(data):
    """
    :param data: EMG signal samples within rolling window segment
    :return: Mean Absolute Value which is the average of the absolute values of the EMG signal.
    It is used for the detection of muscle contraction levels.
    """
    return np.mean(np.abs(data), axis=1)


def mmav1(data):
    """
    :param data: EMG signal samples within rolling window segment
    :return: Modified Mean Absolute Value 1 which is an extension of the MAV by applying a discrete
    weighting window function.
    """
    llim = int(0.25 * data.shape[1])
    hlim = int(0.75 * data.shape[1]) + 1
    r1 = np.arange(0, llim)
    r2 = np.arange(llim, hlim)
    r3 = np.arange(hlim, data.shape[1])

    return np.mean(np.concatenate((np.abs(np.take(data, r1, axis=1)) * 0.5, np.abs(np.take(data, r2, axis=1)),
                                   np.abs(np.take(data, r3, axis=1)) * 0.5), axis=1), axis=1)


def mmav2(data):
    """
    :param data: EMG signal samples within rolling window segment
    :return: Modified Mean Absolute Value 2 which is similar to MMAV2 but a smoother continuous
    weighting window function is used.
    """
    llim = int(0.25 * data.shape[1])
    hlim = int(0.75 * data.shape[1]) + 1
    r1 = np.arange(0, llim)
    r2 = np.arange(llim, hlim)
    r3 = np.arange(hlim, data.shape[1])
    c1 = (4 * (r1 + 1) / data.shape[1])[np.newaxis, :, np.newaxis]
    c2 = (4 * (r3 + 1 - data.shape[1]) / data.shape[1])[np.newaxis, :, np.newaxis]

    return np.mean(np.concatenate((np.abs(np.take(data, r1, axis=1)) * c1, np.abs(np.take(data, r2, axis=1)),
                                   np.abs(np.take(data, r3, axis=1)) * c2), axis=1), axis=1)


def mavslp(mavs):
    """
    :param mavs: Mean Absolute Value of each EMG segment
    :return: The slope/difference of the MAV segments of the EMG signal.
    """
    return np.insert(np.diff(mavs, axis=0), 0, 0, axis=0)


def ssi(data):
    """
    :param data: EMG signal samples within rolling window segment
    :return: Simple Square Integral which is the energy of the sEMG signal segment.
    """
    return np.sum(np.power(np.abs(data), 2), axis=1)


def variance(data):
    """
    :param data: EMG signal samples within rolling window segment
    :return: Variance which is the average of the square of the signal's deviation from the mean.
    It uses the signals power as a feature.
    """
    return np.var(data, axis=1)


def rms(data):
    """
    :param data: EMG signal samples within rolling window segment
    :return: Root Mean Square which is the standard deviation of the signal amplitude values.
    It is related to the constant force and non-fatiguing contraction of the muscle.
    """
    return np.sqrt(np.mean(data ** 2, axis=1))


def wl(data):
    """
    :param data: EMG signal samples within rolling window segment
    :return: Waveform Length which is the cumulative length of the waveform over the time segment.
    It is related to the waveform amplitude, frequency and time.
    """
    return np.sum(np.abs(np.diff(data, axis=1)), axis=1)


def zc(data, th=10):
    """
    :param data: EMG signal samples within rolling window segment
    :param th: Threshold used to reduce noise effects
    :return: Zero Crossing which is the number of times the signal values cross zero.
    It provides an approximation of the signal frequency. The threshold used is for reducing the effect of noise.
    """
    return np.sum((np.diff(np.sign(data), axis=1) != 0) & (np.abs(np.diff(data, axis=1)) > th), axis=1)


def ssc(data, th=10):
    """
    :param data: EMG signal samples within rolling window segment
    :param th: Threshold used to reduce noise effects
    :return: Slope Sign Changes which is the number of changes between positive and negative slopes of the signal.
    It also provides information about the signal frequency. The threshold used is for reducing the effect of noise.
    """
    pos_slope = (-np.diff(data, prepend=1, axis=1) > 0) & (np.diff(data, append=1, axis=1) > 0)
    neg_slope = (-np.diff(data, prepend=1, axis=1) < 0) & (np.diff(data, append=1, axis=1) < 0)
    denoised = (np.abs(-np.diff(data, prepend=1, axis=1)) > th) | (np.abs(np.diff(data, append=1, axis=1)) > th)
    ssc_ = (pos_slope | neg_slope) & denoised
    return np.sum(np.delete(ssc_, [0, -1], axis=1), axis=1)


def wamp(data, th=10):
    """
    :param data: EMG signal samples within rolling window segment
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
    :param data: EMG signal samples within rolling window segment
    :return: Kurtosis which is a statistical measure that defines how the tails of a distribution differs
    from the tails of a normal distribution. It identifies the presence of extreme values in the EMG signal.
    """
    return sp.stats.kurtosis(data, axis=1)


def skewness(data):
    """
    :param data: EMG signal samples within rolling window segment
    :return: Skewness which measures the lack of symmetry of a distribution. It also identifies the
    presence of extreme values in the EMG signal.
    """
    return sp.stats.skew(data, axis=1)


def ar_coefficients(data, order=11):
    ar_coeff = []
    for window in data:
        window_coeff = []
        for channel in range(len(window[0])):
            ak, _ = AR_est_YW(window[:, channel], order)
            window_coeff.extend(ak)
        ar_coeff.append(window_coeff)

    return np.array(ar_coeff)


def hjorth_params(data):
    first_deriv = np.diff(data, axis=1)
    second_deriv = np.diff(data, 2, axis=1)

    var_zero = np.mean(data ** 2, axis=1)
    var_d1 = np.mean(first_deriv ** 2, axis=1)
    var_d2 = np.mean(second_deriv ** 2, axis=1)

    activity = var_zero
    morbidity = np.sqrt(var_d1 / var_zero)
    complexity = np.sqrt(var_d2 / var_d1) / morbidity

    hjorth_params = np.concatenate((activity, morbidity, complexity), axis=1)
    return hjorth_params


def hjorth_activity(data):
    return np.mean(data ** 2, axis=1)


def hjorth_morbidity(data):
    first_deriv = np.diff(data, axis=1)

    activity = np.mean(data ** 2, axis=1)
    var_d1 = np.mean(first_deriv ** 2, axis=1)

    morbidity = np.sqrt(var_d1 / activity)

    return morbidity


def hjorth_complexity(data):
    first_deriv = np.diff(data, axis=1)
    second_deriv = np.diff(data, 2, axis=1)

    activity = np.mean(data ** 2, axis=1)
    var_d1 = np.mean(first_deriv ** 2, axis=1)
    var_d2 = np.mean(second_deriv ** 2, axis=1)

    morbidity = np.sqrt(var_d1 / activity)
    complexity = np.sqrt(var_d2 / var_d1) / morbidity

    return complexity


# def frequency_domain(data, win_len, win_stride, fs=980):
#     """
#     :param data: EMG signal
#     :param fs: Sampling frequency of EMG signal
#     :param win_len: Number of EMG signal samples per STFT sliding window segment
#     :param win_stride: Number of overlapping samples
#     :return: Power Spectrum and Frequency range of the EMG signal resulting from a short time fourier transform
#     """
#     frequencies, t, fourier_coefficients = signal.stft(data, fs=fs, window='cosine', nperseg=win_len, padded=False,
#                                                        noverlap=win_stride, boundary=None, axis=0)
#     power_spectrum = np.square(np.abs(np.transpose(fourier_coefficients, (2, 0, 1))))
#     return frequencies, power_spectrum


def frequency_domain(data, fs=980):
    """
    :param data: EMG signal
    :param fs: Sampling frequency of EMG signal
    :return: Power Spectrum and Frequency range of the EMG signal resulting from a short time fourier transform
    """
    fourier_coefficients = sp.fft.fft(data, axis=1)
    frequencies = np.linspace(0, fs/2, fourier_coefficients.shape[1])
    power_spectrum = np.square(np.abs(fourier_coefficients))
    return frequencies, power_spectrum


def mnf(frequencies, power_spectrum):
    """
    :param frequencies: Frequency range of the power spectrum
    :param power_spectrum: Power of the EMG signal at different frequencies
    :return: Mean Frequency which is the average frequency of the power spectrum
    """
    return np.divide(np.sum(np.multiply(power_spectrum, np.repeat(frequencies, power_spectrum.shape[2]).reshape(
        power_spectrum.shape[1], power_spectrum.shape[2])), axis=1), np.sum(power_spectrum, axis=1))


def mdf(frequencies, power_spectrum):
    """
    :param frequencies: Frequency range of the power spectrum
    :param power_spectrum: Power of the EMG signal at different frequencies
    :return: Median Frequency which is the frequency at which the spectrum is divided into two regions with equal power
    """
    med_freq = np.zeros((power_spectrum.shape[0], power_spectrum.shape[2]))
    for indx, segment in enumerate(power_spectrum):
        differences = []
        for ind in range(frequencies.shape[0]):
            diff = np.abs(np.subtract(np.sum(segment[:ind, :], axis=0), 0.5 * np.sum(segment, axis=0)))
            differences.append(diff)

        differences = np.array(differences)
        med_freq[indx, :] = frequencies[differences.argmin(axis=0)]

    return med_freq


def mmnf(frequencies, power_spectrum):
    """
    :param frequencies: Frequency range of the power spectrum
    :param power_spectrum: Power of the EMG signal at different frequencies
    :return: Modified Mean Frequency which uses the amplitude spectrum instead of the power spectrum
    """
    amplitude_spectrum = np.sqrt(power_spectrum)
    return np.divide(np.sum(np.multiply(amplitude_spectrum, np.repeat(frequencies, amplitude_spectrum.shape[2]).reshape(
        amplitude_spectrum.shape[1], amplitude_spectrum.shape[2])), axis=1), np.sum(amplitude_spectrum, axis=1))


def mmdf(frequencies, power_spectrum):
    """
    :param frequencies: Frequency range of the power spectrum
    :param power_spectrum: Power of the EMG signal at different frequencies
    :return: Modified Median Frequency which uses the amplitude spectrum instead of the power spectrum. It
    is the frequency at which the spectrum is divided into two regions with equal amplitude
    """
    amplitude_spectrum = np.sqrt(power_spectrum)
    med_freq = np.zeros((amplitude_spectrum.shape[0], amplitude_spectrum.shape[2]))
    for indx, segment in enumerate(amplitude_spectrum):
        differences = []
        for ind in range(frequencies.shape[0]):
            diff = np.abs(np.subtract(np.sum(segment[:ind, :], axis=0), 0.5 * np.sum(segment, axis=0)))
            differences.append(diff)

        differences = np.array(differences)
        med_freq[indx, :] = frequencies[differences.argmin(axis=0)]

    return med_freq
