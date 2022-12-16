import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import sounddevice as sd
import math
from sklearn.preprocessing import normalize

ka = 4
duration = 0.01
speed_sound = 343
afstan = 0.26*2
samplerat = 44100*4
vinkel_afsnit = 3600

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
while True:
    
    mid_vadi = np.zeros((int(duration * samplerat),vinkel_afsnit))
    recording = sd.rec(int(duration * samplerat), samplerate=samplerat, channels=4)
    sd.wait()

    lis = np.zeros(vinkel_afsnit)
    
    for channel in range(ka):
        recording[:, channel] = np.interp(recording[:, channel], (recording[:, channel].min(), recording[:, channel].max()), (0, 1))
        kernel_size = 1
        kernel = np.ones(kernel_size) / kernel_size
        recording[:, channel] = np.convolve(recording[:, channel], kernel, mode='same')
    for i in range(vinkel_afsnit):
        v = i*(2*math.pi/vinkel_afsnit)
        rol = [0,0,0,0]
        for j in range(ka):
            tid = (math.cos(v+j*math.pi/2))*afstan/(speed_sound*2)
            rol[j] = tid*samplerat;
        #print(rol[0])
        mid_spor = [0,0,0,0];
        for j in range(ka):
            mid_spor[-j] = recording[:,j].copy()

        mid_vadi[:,i] = (np.roll(mid_spor[0],int(rol[0]))- np.roll(mid_spor[2],int(rol[2])))*(np.roll(mid_spor[0],int(rol[0])) - np.roll(mid_spor[2],int(rol[2]))) + (np.roll(mid_spor[1],int(rol[1])) - np.roll(mid_spor[3],int(rol[3])))*(np.roll(mid_spor[1],int(rol[1])) - np.roll(mid_spor[3],int(rol[3])))
        #mid_vadi[:,i] = (np.roll(mid_spor[0],int(rol[0])) + np.roll(mid_spor[2],int(rol[2]))) + (np.roll(mid_spor[1],int(rol[1])) - np.roll(mid_spor[3],int(rol[3])))
        for channel in range(ka):
            #plt.subplot(1, 2, 1)
            #plt.plot(np.roll(mid_spor[channel],int(rol[channel])), label=f"Kanal {channel+1}")
            pass
        #plt.plot(mid_vadi[:,i])
        #plt.show()
        lis[i] = mid_vadi[:,i].sum()
    #cv.imshow("test",mid_vadi)
    print( f"{lis.argmin()/10}")
    #plt.subplot(1, 2, 2)
    #plt.show()
    plt.plot(lis,label=f"Kanal {0}")
    # plt.show()
    fig.canvas.flush_events()
    fig.canvas.draw()
    fig.clear(True)
