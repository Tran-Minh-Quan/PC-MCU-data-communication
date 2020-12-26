import serial
from time import sleep as wait
from time import time
import numpy as np
import cv2
from numpy.random import randint

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


ser = serial.Serial('COM16', baudrate=1000000, bytesize=serial.EIGHTBITS)
i = 0
wait(2)
receive = ''
send_counter = 0
error_counter = 0
num_crc_error = 0
num_timeout_error = 0
while 1:
    if send_counter:
        # data = bytearray(input('Input string: '), 'utf-8')
        data = bytearray(randint(256, size=randint(10, 256)))
    else:
        data = bytearray(1)
    len_data = bytearray(len(data))
    crc = crc8(databytes=len_data + data)
    transmit = len_data + data + crc
    ser.timeout = 0.00002 * len(transmit) + 0.001
    ser.write(transmit)
    receive = ser.read(1).hex()
    status = bool(receive == str(0) + str(6))
    if status == False:
        if receive == '30':
            num_crc_error += 1
        elif receive == '31':
            num_timeout_error += 1
        error_counter += 1
    # if send_counter:
    #     print(f'Transmitted data: {transmit}')
    #     print(f'Received data: {receive}, status: {status}')
    while receive != '06':
        ser.write(transmit)
        receive = ser.read(1).hex()
        status = bool(receive == str(0) + str(6))
        if status == False:
            if receive == '30':
                num_crc_error += 1
            elif receive == '31':
                num_timeout_error += 1
            error_counter += 1
        # if send_counter:
        #     print(f'Transmitted data: {transmit}')
        #     print(f'Received data: {receive}, status: {status}')
    send_counter += 1
    percent_error = error_counter * 100 // send_counter
    print(f'Number of crc error: {num_crc_error}')
    print(f'Number of timeout: {num_timeout_error}')
    print(f'Number of send data: {send_counter}')
    print(f'Number of error data: {error_counter}')
    print(f'Percent_error: {percent_error}%')

    # buffer = np.random.randint(9, size=10).astype(np.uint8)
