import os
import numpy as np
import pandas as pd
from datetime import datetime
from .time_domain_feats_extr import extract_time_domain_features
from .order_domain_feats_extr import extract_order_domain_features

def filepath_list_from_directory(directory_path):
    filepath_list = [f'{directory_path}/{file}' for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
    filepath_list.sort()
    return filepath_list

def read_data(filepath, column_indices):
    data_array = np.loadtxt(filepath)
    data_array = data_array.T
    data_array = data_array[column_indices,:]
    return data_array

def timestamp_from_filepath(filepath, time_str_format):
    file_date = os.path.basename(filepath)
    time = datetime.strptime(file_date, time_str_format)
    epoch_time = time.timestamp()
    return epoch_time

def convert_epochs_list_to_RUL_rotations(epochs_list, shaft_rpm):
    rul_epochs_array = np.array(epochs_list)
    rul_epochs_array -= np.max(rul_epochs_array)
    rul_epochs_array *= -1
    rul_epochs_array = np.abs(rul_epochs_array)
    rul_rotations_array = rul_epochs_array * (shaft_rpm / 60)
    return rul_rotations_array

def extract_features(directory_path, column_indices, time_format, sampling_freq, sampling_time, shaft_rpm, roll_elem_diam, pitch_diam, roll_elem_count, contact_angle):
    filepath_list = filepath_list_from_directory(directory_path)

    epochs_list = []
    time_features_records_list = []
    order_features_records_list = []

    for filepath in filepath_list:
        epoch = timestamp_from_filepath(filepath, time_format)
        
        data_array = read_data(filepath, column_indices)

        for i in range(len(data_array)):
            epochs_list.append(epoch)
            time_features_record = extract_time_domain_features(data_array[i])
            order_features_record = extract_order_domain_features(data_array[i], sampling_freq, sampling_time, shaft_rpm, roll_elem_diam, pitch_diam, roll_elem_count, contact_angle)

            time_features_records_list.append(time_features_record)
            order_features_records_list.append(order_features_record)
    
    rul_rotations_array = convert_epochs_list_to_RUL_rotations(epochs_list, shaft_rpm)
    rul_rotations_df_cols = ['RUL_rotations']

    y_rotations = pd.DataFrame(rul_rotations_array, columns=rul_rotations_df_cols)
    X_time_domain = pd.DataFrame(time_features_records_list)
    X_order_domain = pd.DataFrame(order_features_records_list)

    return  y_rotations, X_time_domain, X_order_domain