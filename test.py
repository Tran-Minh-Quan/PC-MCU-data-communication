import serial
from time import sleep as wait
from time import time
import numpy as np
import cv2

def crc8_1byte(databyte, generator=285):
    generator -= 256
    crc = databyte
    for bit in range(7, -1, -1):
        if crc & 0b10000000:
            crc = crc << 1 & 255 ^ generator
        else:
            crc <<= 1
    return crc


crc8_dict = {databyte: crc8_1byte(databyte=databyte) for databyte in range(256)}


def crc8(databytes, generator=285):
    generator -= 256
    crc = 0
    for byte in databytes:
        crc = crc8_dict[byte ^ crc]
    return bytearray([crc])


ser = serial.Serial('COM3', baudrate=1000000, bytesize=serial.EIGHTBITS, timeout=0.004)
i = 0
wait(2)
while 1:
    receive = None
    while receive != '06':
        data = bytearray(input('Input string: '), 'utf-8')
        crc = crc8(databytes=data)
        transmit = data
        ser.write(transmit)
        print(f'transmitted data: {transmit}')
        receive = ser.read(1).hex()
        print(f'received data: {receive}, status: {receive == str(0) + str(6)}')
    # buffer = np.random.randint(9, size=10).astype(np.uint8)
