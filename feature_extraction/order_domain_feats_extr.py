import numpy as np
import scipy.signal as scpsig
import scipy.fft as scpfft
from math import isclose
from .bearing_properties_calculations import calculate_multiplied_modulated_bearing_faults_orders as calculate_bearing_fault_orders 

def calculate_amplitude_order_spectrum(time_data_array, sampling_freq, sampling_time, shaft_rpm):
    new_time_data_array = time_data_array[:sampling_time * sampling_freq]
    window = scpsig.get_window('hann', len(new_time_data_array))
    amplitude_correction_factor = len(window) / np.sum(window)
    windowed_new_time_data_array = window * new_time_data_array
    orders_amplitude_array = np.abs(scpfft.rfft(windowed_new_time_data_array, norm='forward', workers=-1)) * amplitude_correction_factor
    freq_array = scpfft.rfftfreq(len(new_time_data_array), 1/sampling_freq)
    orders_array = freq_array / (shaft_rpm / 60)
    return orders_amplitude_array, orders_array

def extract_orders_amplitudes_from_available_orders_dict(bearing_fault_orders, available_orders_amplitude_array, available_orders_array):
    extracted_orders_amplitudes_dict = {}
    
    tolerance = np.max(np.diff(available_orders_array))

    for order_name, calculated_order in bearing_fault_orders.items():
        approximate_orders_indexes_list = []
        for index, available_order in enumerate(available_orders_array):
            if isclose(calculated_order, available_order, abs_tol=tolerance):
                approximate_orders_indexes_list.append(index)
            if len(approximate_orders_indexes_list) == 2:
                break

        order_selected_amplitude = np.max(available_orders_amplitude_array[approximate_orders_indexes_list])
        extracted_orders_amplitudes_dict[order_name] = order_selected_amplitude

    return extracted_orders_amplitudes_dict

def extract_order_domain_features(time_data_array, sampling_freq, sampling_time, shaft_rpm, roll_elem_diam, pitch_diam, roll_elem_count, contact_angle):
    bearing_fault_orders = calculate_bearing_fault_orders(roll_elem_diam, pitch_diam, roll_elem_count, contact_angle)
    available_orders_amplitude_array, available_orders_array = calculate_amplitude_order_spectrum(time_data_array, sampling_freq, sampling_time, shaft_rpm)
    order_domain_features_record = extract_orders_amplitudes_from_available_orders_dict(bearing_fault_orders, available_orders_amplitude_array, available_orders_array)
    return order_domain_features_record