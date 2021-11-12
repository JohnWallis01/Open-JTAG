import serial
import time


#detect host device
Slave = serial.Serial(port="COM6", baudrate=57600, timeout=0.1)

def write_read(x):
    Slave.write(bytes(x, 'utf-8'))
    time.sleep(1)
    data = Slave.readline()
    return data


while True:
    data = input("Enter data: ")
    response = write_read(data)
    print(response)
