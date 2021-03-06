import mne
import numpy as np
import matplotlib.pyplot as plt

dict_session = {1:'CTL', 2:'PD'}
electrodes = ['Fp1', 'Fz', 'F3', 'F7', 'FT9', 'FC5', 'FC1', 'C3', 'T7', 'TP9', 'CP5', 
    'CP1', 'Pz', 'P3', 'P7', 'O1', 'Oz', 'O2', 'P4', 'P8', 'TP10', 'CP6', 'CP2', 'Cz', 
    'C4', 'T8', 'FT10', 'FC6', 'FC2', 'F4', 'F8', 'Fp2', 'AF7', 'AF3', 'AFz', 'F1', 
    'F5', 'FT7', 'FC3', 'FCz', 'C1', 'C5', 'TP7', 'CP3', 'P1', 'P5', 'PO7', 'PO3', 
    'POz', 'PO4', 'PO8', 'P6', 'P2', 'CP4', 'TP8', 'C6', 'C2', 'FC4', 'FT8', 
    'F6', 'F2', 'AF4', 'AF8']

CTL_power_eyes_closed_S3S4avg = mne.time_frequency.read_tfrs(f'S3_S4-{dict_session[1]}-tfr.h5')
CTL_power_eyes_closed_S3S4avg[0].data = 10 * np.log10(CTL_power_eyes_closed_S3S4avg[0].data)
PD_power_eyes_closed_S3S4avg = mne.time_frequency.read_tfrs(f'S3_S4-{dict_session[2]}-tfr.h5')
PD_power_eyes_closed_S3S4avg[0].data = 10 * np.log10(PD_power_eyes_closed_S3S4avg[0].data)


CTL_power_eyes_closed_S3S4avg[0].data = CTL_power_eyes_closed_S3S4avg[0].data - PD_power_eyes_closed_S3S4avg[0].data

for pick_channel in electrodes:
    fig, axis = plt.subplots(1, 1, figsize=(8,5))
    CTL_power_eyes_closed_S3S4avg[0].plot([pick_channel], show=False, axes=axis, colorbar=True)
    fig.suptitle(f'CTL minus PD eyes closed {pick_channel}', fontsize=12)
    fig.savefig(f'/Users/senthilp/Desktop/CTL_minus_PD_eyesclosed/{pick_channel}.png')