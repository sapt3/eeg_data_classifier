import pyedflib
import numpy as np
from window_slider import Slider

overlap_ratio = 0.5

window_data_array = []
fname = "C:/Users/user/Desktop/Motor_Imagery_using_EEG/files/S001/S001R"
for j in range(1, 14):
    f = pyedflib.EdfReader(fname + f"{j}.edf")
    n = f.signals_in_file
    signal_labels = f.getSignalLabels()

    sigbufs = np.zeros((14, n, f.getNSamples()[0]))
    for i in np.arange(n):
        sigbufs[j, i, :] = f.readSignal(i)

    list = sigbufs[j]
    bucket_size = 5000  # length of sliding window
    overlap_count = bucket_size * overlap_ratio  # overlap
    slider = Slider(bucket_size, overlap_count)
    slider.fit(list)
    while True:
        window_data = slider.slide()
        print(window_data[j])
        if slider.reached_end_of_list():
            window_data_array.append(window_data)
            break
