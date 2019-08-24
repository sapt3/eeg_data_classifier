import pyedflib
import numpy as np
from window_slider import Slider

overlap_ratio = 0.5

window_data_array = []
fname = "C:/Users/user/Desktop/Motor_Imagery_using_EEG/files/S"
for k in range(1, 109):
    for j in range(1,15):
        p = fname + str(k).zfill(3) + "/S" + str(k).zfill(3) + "R" + str(j).zfill(2) + ".edf"
        f = pyedflib.EdfReader(p)
        n = f.signals_in_file
        signal_labels = f.getSignalLabels()

        sigbufs = np.zeros((15, n, f.getNSamples()[0]))
        for i in np.arange(n):
            sigbufs[k, j, i, :] = f.readSignal(i)

        list = sigbufs[j]
        bucket_size = 5000  # length of sliding window
        overlap_count = int(bucket_size * overlap_ratio)  # overlap
        slider = Slider(bucket_size, overlap_count)
        slider.fit(list)
        while True:
            window_data = slider.slide()
            window_data_array.append(window_data)
            if slider.reached_end_of_list():
                break