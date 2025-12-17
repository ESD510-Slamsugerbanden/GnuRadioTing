import numpy as np
from matplotlib import pyplot as plt

vectorLength = 1024
center = 37

f = np.float64(np.fromfile(open("10meter/10metersnr.bin"),dtype=np.float32))
f2 = np.float64(np.fromfile(open("40meter/40metersnr.bin"),dtype=np.float32))

i10 = 1095718-38

i30 = 718885-37

i40 = int(len(f2))

#numOfPackets = int(1070)
numOfPackets = int(((i40)/1024))
noisePackets = int(((i10)/1024))



#Convert to linear from dB

for i in range(len(f2)):
    f2[i] = (10**f2[i])


#Plot Data

fig, ax = plt.subplots()

x = []
for i in range(len(f2)):
    x.append(i)


ax.plot(x,f2)
plt.show()


Signal = 0
Noise = 0

for i in range(int(numOfPackets)):
    #Fisker de tre rigtige bins ud
    for k in range(3): 
        Signal += f2[int(i*vectorLength+center-1+k)]
    
    
#Noise
for i in range(len(f)):
    f[i] = (10**f[i])

for i in range(noisePackets*1024, len(f)):
    Noise += f[i]



Signal = Signal/numOfPackets
Noise = Noise/((len(f))/1024-(noisePackets))

Signal = 10*np.log10(Signal)
Noise = 10*np.log10(Noise)


'''
plt.hist(f,bins = 1000, range=(0, 0.001))
plt.show()
'''
print("Signal", Signal)

print("Noise", Noise)

print("SNR: ", Signal-Noise)



#print((1095718-38)/1024)