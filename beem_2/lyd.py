import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

# Vælg længden af lydoptagelsen (i sekunder)
duration = 5

# Optag lyd fra mikrofonen
recording = sd.rec(int(duration * 44100), samplerate=44100, channels=4)
sd.wait()

# Beregn lydstyrken for hvert tidspunkt i optagelsen for hver kanal
#volumes = np.abs(recording)




# Plot lydstyrken over tid for hver kanal
for channel in range(4):
    fft_out = np.fft.fft(recording[:, channel])
    frequencies = np.fft.fftfreq(len(recording[:, channel]))
    plt.plot(frequencies, fft_out, label=f"Kanal {channel+1}")
    #plt.plot(recording[:, channel], label=f"Kanal {channel+1}")

plt.legend()
plt.show()

plt.xlabel('Frekvens')
plt.ylabel('Amplitude')
plt.show()
