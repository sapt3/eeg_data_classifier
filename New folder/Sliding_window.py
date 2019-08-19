import pyedflib
import numpy as np
from window_slider import Slider

f = pyedflib.EdfReader("C:/Users/user/Desktop/Motor_Imagery_using_EEG/files/S001/S001R03.edf")
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))
for i in np.arange(n):
    sigbufs[i, :] = f.readSignal(i)

list = sigbufs
bucket_size = 5000     #length of sliding window
overlap_count = 2500   #overlap
slider = Slider(bucket_size,overlap_count)
slider.fit(list)
while True:
    window_data = slider.slide()
    print(window_data)
    if slider.reached_end_of_list(): break