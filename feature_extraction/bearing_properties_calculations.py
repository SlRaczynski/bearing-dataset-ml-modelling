import numpy as np

def calculate_BPFO_base_order(roll_elem_diam, pitch_diam, roll_elem_count, contact_angle):
    bpfo_base_order = (roll_elem_count / 2) * (1 - (roll_elem_diam / pitch_diam) * np.cos(np.deg2rad(contact_angle)))
    return bpfo_base_order

def calculate_BPFI_base_order(roll_elem_diam, pitch_diam, roll_elem_count, contact_angle):
    bpfi_base_order = (roll_elem_count / 2) * (1 + (roll_elem_diam / pitch_diam) * np.cos(np.deg2rad(contact_angle)))
    return bpfi_base_order

def calculate_BSF_base_order(roll_elem_diam, pitch_diam, contact_angle):
    bsf_base_order  = (pitch_diam / roll_elem_diam) * (1 - ((roll_elem_diam / pitch_diam) * np.cos(np.deg2rad(contact_angle))**2))
    return bsf_base_order

def calculate_FTF_base_order(roll_elem_diam, pitch_diam, contact_angle):
    ftf_base_order = (1 - (roll_elem_diam / pitch_diam) * np.cos(np.deg2rad(contact_angle))) / 2
    return ftf_base_order

def calculate_order_multiplies(base_order, harmonics_number):
    orders_list = [base_order * i for i in range(1, (harmonics_number+1))]
    return orders_list

def add_modulation_sidebands(base_order, modulation_sideband_distance, modulation_sidebands_number):
    modulation_sidebands_orders_list = [base_order]

    for i in range(1, (modulation_sidebands_number + 1)):
        modulation_sidebands_orders_list.append(base_order + (i * modulation_sideband_distance))
        modulation_sidebands_orders_list.append(base_order - (i * modulation_sideband_distance))
    
    modulation_sidebands_orders_list.sort()
    
    return modulation_sidebands_orders_list

def calculate_bearing_faults_base_orders(roll_elem_diam, pitch_diam, roll_elem_count, contact_angle):
    bearing_faults_base_orders_dict = {}
    bearing_faults_base_orders_dict['BPFO'] = calculate_BPFO_base_order(roll_elem_diam, pitch_diam, roll_elem_count, contact_angle)
    bearing_faults_base_orders_dict['BPFI'] = calculate_BPFI_base_order(roll_elem_diam, pitch_diam, roll_elem_count, contact_angle)
    bearing_faults_base_orders_dict['BSF'] = calculate_BSF_base_order(roll_elem_diam, pitch_diam, contact_angle)
    bearing_faults_base_orders_dict['FTF'] = calculate_FTF_base_order(roll_elem_diam, pitch_diam, contact_angle)

    return bearing_faults_base_orders_dict

def calculate_BPFO_multiplies_orders_dict(bpfo_base_order, harmonics_number=10):
    bpfo_multiplies_orders_dict = {}

    for multiply_counter, bpfo_multiply in enumerate(calculate_order_multiplies(bpfo_base_order, harmonics_number)):
        multiply_number = 1 + multiply_counter
        bpfo_multiplies_orders_dict[f'{multiply_number}xBPFO'] = bpfo_multiply
    
    return bpfo_multiplies_orders_dict

def calculate_FTF_multiplies_orders_dict(ftf_base_order, harmonics_number=5):
    ftf_multiplies_orders_dict = {}

    for multiply_counter, ftf_multiply in enumerate(calculate_order_multiplies(ftf_base_order, harmonics_number)):
        multiply_number = 1 + multiply_counter
        ftf_multiplies_orders_dict[f'{multiply_number}xFTF'] = ftf_multiply
    
    return ftf_multiplies_orders_dict

def calculate_BPFI_multiplies_orders_dict(bpfi_base_order, harmonics_number=10, modulation_sideband_distance=1, modulation_sidebands_number=3):
    bpfi_modulated_multiplies_orders_dict = {}

    for multiply_counter, bpfi_multiply in enumerate(calculate_order_multiplies(bpfi_base_order, harmonics_number)):
        multiply_number = 1 + multiply_counter

        for modulation_counter, bpfi_modulated_multiply in enumerate(add_modulation_sidebands(bpfi_multiply, modulation_sideband_distance=modulation_sideband_distance, modulation_sidebands_number=modulation_sidebands_number)):
            modulation_number = modulation_counter - modulation_sidebands_number
            
            if modulation_number == 0:
                bpfi_modulated_multiplies_orders_dict[f'{multiply_number}xBPFI'] = bpfi_modulated_multiply
            else:
                bpfi_modulated_multiplies_orders_dict[f'{multiply_number}xBPFI{modulation_number:+}X'] = bpfi_modulated_multiply
    
    return bpfi_modulated_multiplies_orders_dict

def calculate_BSF_multiplies_orders_dict(bsf_base_order, harmonics_number=5, modulation_sideband_distance=1, modulation_sidebands_number=3):
    bsf_modulated_multiplies_orders_dict = {}

    for multiply_counter, bsf_multiply in enumerate(calculate_order_multiplies(bsf_base_order, harmonics_number)):
        multiply_number = 1 + multiply_counter

        for modulation_counter, bsf_modulated_multiply in enumerate(add_modulation_sidebands(bsf_multiply, modulation_sideband_distance=modulation_sideband_distance, modulation_sidebands_number=modulation_sidebands_number)):
            modulation_number = modulation_counter - modulation_sidebands_number
            
            if modulation_number == 0:
                bsf_modulated_multiplies_orders_dict[f'{multiply_number}xBSF'] = bsf_modulated_multiply
            else:
                bsf_modulated_multiplies_orders_dict[f'{multiply_number}xBSF{modulation_number:+}X'] = bsf_modulated_multiply
    
    return bsf_modulated_multiplies_orders_dict

def calculate_rotational_speed_orders(harmonics_number=3):
    rotational_orders_dict = {}
    
    for i in range(harmonics_number):
        rotational_orders_dict[f'{i+1}X'] = i
    
    return rotational_orders_dict

def calculate_multiplied_modulated_bearing_faults_orders(roll_elem_diam, pitch_diam, roll_elem_count, contact_angle):
    bearing_faults_base_orders_dict = calculate_bearing_faults_base_orders(roll_elem_diam, pitch_diam, roll_elem_count, contact_angle)
    
    multiplied_modulated_bearing_faults_orders_dict = calculate_rotational_speed_orders()
    multiplied_modulated_bearing_faults_orders_dict |= calculate_BPFO_multiplies_orders_dict(bearing_faults_base_orders_dict['BPFO'])
    multiplied_modulated_bearing_faults_orders_dict |= calculate_FTF_multiplies_orders_dict(bearing_faults_base_orders_dict['FTF'])
    multiplied_modulated_bearing_faults_orders_dict |= calculate_BPFI_multiplies_orders_dict(bearing_faults_base_orders_dict['BPFI'])
    multiplied_modulated_bearing_faults_orders_dict |= calculate_BSF_multiplies_orders_dict(bearing_faults_base_orders_dict['BSF'], modulation_sideband_distance=bearing_faults_base_orders_dict['FTF'])

    return multiplied_modulated_bearing_faults_orders_dict