import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import sounddevice as sd
import math
from sklearn.preprocessing import normalize

def afstand(a,b):
    return (a-b)*(a*b);

ka = 4
duration = 0.01
speed_sound = 343
afstan = 0.26
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
            tid = (math.sin(v+j*math.pi/2)+1)*afstan/(speed_sound)
            rol[j] = int(tid*samplerat);
        mid_spor = [0,0,0,0];
        for j in range(ka):
            mid_spor[-j] = recording[:,j].copy()
        #gensnit = 
        #mid_vadi[:,i] = (np.roll(mid_spor[0],int(rol[0]))- np.roll(mid_spor[2],int(rol[2])))*(np.roll(mid_spor[0],int(rol[0])) - np.roll(mid_spor[2],int(rol[2]))) + (np.roll(mid_spor[1],int(rol[1])) - np.roll(mid_spor[3],int(rol[3])))*(np.roll(mid_spor[1],int(rol[1])) - np.roll(mid_spor[3],int(rol[3])))
        #mid_vadi[:,i] = (np.roll(mid_spor[0],int(rol[0])) + np.roll(mid_spor[2],int(rol[2]))) + (np.roll(mid_spor[1],int(rol[1])) - np.roll(mid_spor[3],int(rol[3])))
        trim_int = int(afstan*2*samplerat/(speed_sound))+1
        #print(rol[0])
        #print(trim_int)
        #print(-(trim_int-rol[0]))
        trim_mid_vadi = mid_spor[0][rol[0]:-(trim_int-rol[0])] +  mid_spor[1][rol[1]:-(trim_int-rol[1])] +  mid_spor[2][rol[2]:-(trim_int-rol[2])] +  mid_spor[3][rol[3]:-(trim_int-rol[3])]  
        #print(trim_mid_vadi)
        for channel in range(ka):
            #plt.subplot(1, 2, 1)
            #plt.plot(np.roll(mid_spor[channel],int(rol[channel])), label=f"Kanal {channel+1}")
            pass
        #plt.plot(mid_vadi[:,i])
        #plt.show()
        #trim_mid_vadi = mid_vadi[trim_int:-trim_int,i].copy()
        lis[i] = trim_mid_vadi.max()
        #lis[i] = mid_vadi[:,i].sum()
    #cv.imshow("test",mid_vadi)
    print( f"{lis.argmax()/10}")
    #plt.subplot(1, 2, 2)
    #plt.show()
    plt.plot(lis,label=f"Kanal {0}")
    # plt.show()
    fig.canvas.flush_events()
    fig.canvas.draw()
    fig.clear(True)
