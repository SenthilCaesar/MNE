import os
import numpy as np 
import mne
# pylint: disable=E1101

sample_data_raw_file = 'sample_audvis_filt-0-40_raw.fif'
raw = mne.io.read_raw_fif(sample_data_raw_file)
# print(raw.info)

# # Set up and fit the ICA
# ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
# ica.fit(raw)
# ica.exclude = [1, 2]
# #ica.plot_properties(raw)

# orig_raw = raw.copy()
# raw.load_data()
# ica.apply(raw)

# # show some frontal channels to clearly illustrate the artifact removal
# chs = ['MEG 0111', 'MEG 0121', 'MEG 0131', 'MEG 0211', 'MEG 0221', 'MEG 0231',
#        'MEG 0311', 'MEG 0321', 'MEG 0331', 'MEG 1511', 'MEG 1521', 'MEG 1531',
#        'EEG 001', 'EEG 002', 'EEG 003', 'EEG 004', 'EEG 005', 'EEG 006',
#        'EEG 007', 'EEG 008']

# chan_indxs = [raw.ch_names.index(ch) for ch in chs]
# print(chan_indxs)
# orig_raw.plot(order=chan_indxs, start=12, duration=4)
# raw.plot(order=chan_indxs, start=12, duration=4)

events = mne.find_events(raw, stim_channel='STI 014')
print(np.shape(events), type(events))
event_dict = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,
              'visual/right': 4, 'smiley': 5, 'buttonpress': 32}
# fig = mne.viz.plot_events(events, event_id=event_dict, sfreq=raw.info['sfreq'],
#                           first_samp=raw.first_samp)

reject_criteria = dict(mag=4000e-15,     # 4000 fT
                       grad=4000e-13,    # 4000 fT/cm
                       eeg=150e-6,       # 150 µV
                       eog=250e-6)       # 250 µV

epochs = mne.Epochs(raw, events, event_id=event_dict, tmin=-0.2, tmax=0.5,reject=reject_criteria, preload=True)
print(epochs.event_id)
print(f'Shape of epoch is {np.shape(epochs)}')
print(f'Number of Trails is {len(epochs)}')
print(f'Number of channels is {len(epochs.ch_names)}')

conds_we_care_about = ['auditory/left', 'auditory/right',
                       'visual/left', 'visual/right']
epochs.equalize_event_counts(conds_we_care_about)  # this operates in-place
aud_epochs = epochs['auditory']
vis_epochs = epochs['visual']
aud_epochs.plot_image(picks=['MEG 1332', 'EEG 021'])
