import serial
from time import sleep as wait
import numpy as np

ser = serial.Serial('COM16', baudrate=1000000, bytesize=serial.EIGHTBITS, timeout=1)
i = 0
buffer = np.random.randint(256, size=10)
print(buffer)
# test = (str(i) + ' ').encode('utf-8')
# print(type(test))
wait(2)
while 1:
    received = 0
    while received != 6:
        for i in range(10):
            transmitted = str(buffer[i]).encode('utf-8')
            ser.write(transmitted)
            print(f'transmitted data: {transmitted}')
        received = ser.read(1).hex()
    print(f'received data: {received}')
    wait(0.5)
    buffer = np.random.randint(256, size=10)
