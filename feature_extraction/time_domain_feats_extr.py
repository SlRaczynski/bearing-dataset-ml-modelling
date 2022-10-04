import numpy as np
import scipy.stats as scpstats

def amplitude_pk(data_array):
    return np.max(np.abs(data_array))

def amplitude_pk_pk(data_array):
    return np.max(data_array) - np.min(data_array)

def amplitude_pk_to_pk_pk_factor(data_array):
    return amplitude_pk(data_array) / amplitude_pk_pk(data_array)

def rms(data_array):
    return np.sqrt(np.mean(np.square(data_array)))

def absolute_mean(data_array):
    return np.mean(np.abs(data_array))

def std_dev(data_array):
    return np.std(data_array)

def skewness(data_array):
    return scpstats.skew(data_array, nan_policy='raise')

def kurtosis(data_array):
    return scpstats.kurtosis(data_array, nan_policy='raise')

def clearance_factor(data_array):
    return amplitude_pk_pk(data_array) / np.square(np.mean(np.sqrt(np.abs(data_array))))

def shape_factor(data_array):
    return rms(data_array) / absolute_mean(data_array)

def impulse_factor(data_array):
    return amplitude_pk(data_array) / absolute_mean(data_array)

def crest_factor(data_array):
    return amplitude_pk(data_array) / rms(data_array)

def extract_time_domain_features(data_array):
    time_domain_features_record = {}
    time_domain_features_record['Apk'] = amplitude_pk(data_array)
    time_domain_features_record['Apk_pk'] = amplitude_pk_pk(data_array)
    time_domain_features_record['Apk/Apk_pk_fct'] = amplitude_pk_to_pk_pk_factor(data_array)
    time_domain_features_record['RMS'] = rms(data_array)
    time_domain_features_record['abs_mean'] = absolute_mean(data_array)
    time_domain_features_record['std_dev'] = std_dev(data_array)
    time_domain_features_record['skewness'] = skewness(data_array)
    time_domain_features_record['kurtosis'] = kurtosis(data_array)
    time_domain_features_record['clearance_fct'] = clearance_factor(data_array)
    time_domain_features_record['shape_fct'] = shape_factor(data_array)
    time_domain_features_record['impulse_fct'] = impulse_factor(data_array)
    time_domain_features_record['crest_fct'] = crest_factor(data_array)

    return time_domain_features_record