import os

import warnings

from src.utils.constants import constants
from src.utils.preprocess import correctWifiFP, read_checkpoint, proximity_pixel_interpolation
from src.utils.preprocess import fix_na_wifi, rolling_mean, scale_wifi, get_checkpoints_data

# We take the ssids that have appeared in more than one data collection
CHECKPOINT_DATA_PATH = constants.data.test.CHECKPOINT_DATA_PATH
WIFI_CHECKPOINT = f"{CHECKPOINT_DATA_PATH}/Wifi"

# Maximum sampling time per label
t_max_sampling = constants.T_MAX_SAMPLING_TEST

# Dictionary from labels to meters
labels_dictionary_meters = constants.labels_dictionary_meters_test

warnings.filterwarnings("ignore")


def processTest():
    get_checkpoints_data(dir_data=constants.data.test.INITIAL_DATA,
                         out_dir="output/data/test",
                         dict_labels=labels_dictionary_meters)

    wifi_data = read_checkpoint(WIFI_CHECKPOINT, constants.labels_test)
    wifi_corrected = correctWifiFP(wifi_data=wifi_data,
                                   t_max_sampling=t_max_sampling,
                                   dict_labels_to_meters=labels_dictionary_meters)
    wifi_corrected = fix_na_wifi(wifi_corrected)
    wifi_corrected = proximity_pixel_interpolation(wifi_corrected, threshold=30)

    '''
    Obtain Wi-Fi without scaling the data to 0 - 1
    '''

    raw_wifi = rolling_mean(wifi_corrected, window_size=30, step=5)

    os.makedirs(constants.data.test.RAW_OUT_PATH, exist_ok=True)  # Creamos el directorio en bruto
    raw_wifi.to_csv(f"{constants.data.test.RAW_OUT_PATH}/raw_radiomap.csv", index=False)

    '''
    Obtain Wi-Fi scaling the data to 0 - 1
    '''

    proc_wifi = scale_wifi(wifi_corrected)
    proc_wifi = rolling_mean(proc_wifi, window_size=30, step=5)

    os.makedirs(constants.data.test.PROC_OUT_PATH, exist_ok=True)  # Creamos el directorio procesado
    proc_wifi.to_csv(f"{constants.data.test.PROC_OUT_PATH}/processed_radiomap.csv", index=False)
