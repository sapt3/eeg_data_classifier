import pyedflib
import numpy as np
f = pyedflib.EdfReader("C:/Users/user/Desktop/Motor_Imagery_using_EEG/files/S001/S001R03.edf")
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))
for i in np.arange(n):
    sigbufs[i, :] = f.readSignal(i)
print(sigbufs.shape)
print(sigbufs)
print(signal_labels)