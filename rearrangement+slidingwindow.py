import pyedflib
import numpy as np
from window_slider import Slider

def digit(n):
    c = 0
    while (int(n) > 0):
        n = n / 10
        c = c + 1

    return c


datalist = []
rearrange = [22, 23, 24, 29, 28, 27, 26, 25, 30, 31, 32, 33, 34, 35
    , 36, 37, 38, 40, 7, 6, 5, 4, 3, 2, 1, 39, 43, 41, 8, 9, 10, 11, 12, 13, 14, 42, 44, 46, 21, 20, 19, 18, 17, 16, 15,
             45, 47, 48, 49, 50
    , 51, 52, 53, 54, 55, 60, 59, 58, 57, 56, 61, 62, 63, 64]
list1 = []
for i in range(1, 3):
    s = "S"
    d = digit(i)

    for j in range(0, 3 - d):
        s = s + "0"
    s = s + str(i)
    temp1 = s
    #print(temp1)
    s = s + "R"
    temp = s
    list2 = []
    for k in range(1, 15):
        s = temp
        p = digit(k)

        for t in range(0, 2 - p):
            s = s + "0"

        s = s + str(k)
        s = s + ".edf"
        #print(s)
        p = r"C:\Users\user\Desktop\Motor_Imagery_using_EEG\files\{}{}{}".format(temp1, "\\", s)
        print(p)
        f5 = pyedflib.EdfReader(p)
        n = f5.signals_in_file
        signal_labels = f5.getSignalLabels()
        sigbufs = np.zeros((n, f5.getNSamples()[0]))
        for i in np.arange(n):
            sigbufs[i, :] = f5.readSignal(i)
        sig = sigbufs.tolist()
        emptylist = []
        for i in range(0, 64):
            emptylist.append(sigbufs[rearrange[i] - 1])
            # print(emptylist)
        list2.append(emptylist)
    list1.append(list2)

#print(list1)

window_data_array = []
list = []
overlap_ratio = 0.5
bucket_size = 5000
overlap_count = int(bucket_size * overlap_ratio)


for x in range(1,3):
    window_data_list1 = []
    for y in range(1,15):
        #list = list1[x][y]
        #print(list)
        slider = Slider(bucket_size, overlap_count)
        slider.fit(list1[x][y])
        window_data_list = []
        while True:
            window_data = slider.slide()
            window_data_array.append(window_data)
            if slider.reached_end_of_list():
                break
        window_data_list1.append(window_data_list)
    window_data_array.append(window_data_list1)

print(window_data_array)