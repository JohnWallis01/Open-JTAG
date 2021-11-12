import sys
import csv
import serial
import time

Cable = serial.Serial(port="COM6", baudrate=57600, timeout=5)


JTAG_Data = [0] * 288


class std_logic(object):
    """docstring for std_logic."""

    def __init__(self, dPin, ePin):
        self.dPin = dPin
        self.ePin = ePin

    def set_value(self, value):
        JTAG_Data[self.dPin] = value
        JTAG_Data[self.ePin] = 1





Main_Bus = [std_logic(143, 142), std_logic(140, 139), std_logic(134, 133), std_logic(128, 127), std_logic(125, 124), std_logic(122, 121), std_logic(116, 115), std_logic(110, 109)]
Count = std_logic(224, 223)
CounterOutControl = std_logic(218, 217)
LowJumpRegLoad = std_logic(197, 196)
HighJumpRegLoad = std_logic(194, 193)
JumpEnable = std_logic(191, 190)
MemWriteControl = std_logic(173, 172)
InsRegControl = std_logic(215, 214)

#Everything else needs to be in the disable state; drive reset?

#these are otheroutput pins
CLK = std_logic(14, 13)
MainRegOutputControl =  std_logic(185, 184) #set high
MemOutEnable =  std_logic(179, 178) # set high
Ram_Addr_Enable =  std_logic(161, 160)# set high
StackOutControl =  std_logic(149, 148)# set high


def Bus_Write(BUS, VECTOR):
    for bit in range(len(BUS)):
        BUS[bit].set_value(int(VECTOR[-(bit+1)]))


def read_binaries(file_name):
    if file_name.split(".")[-1] == "bin":
        try:
            f = open(file_name, 'r')
            program = f.read()
            f.close()
            instructions = program.split()
        except Exception as e:
            print("Incorrect Input file was specified")
            exit()
    elif file_name.split(".")[-1] == "hex":
        f = open(file_name, 'r')
        program = f.read()
        f.close()
        n = 2
        hex = [program[i:i+n] for i in range(0, len(program), n)]
        numerical = [(int(hexed, 16)) for hexed in hex[0:-1]]
        n = 8
        instructions = ['{0:{fill}{width}b}'.format(
            (x + 2**n) % 2**n, fill='0', width=n) for x in numerical]
    else:
        print("bang")
        print("Incorrect Input file was specified")
        exit()
    return instructions


def Serial_Transmit(ByteStream):
    Cable.write(bytes("2", 'utf-8')) #transmits an extest command
    print(Cable.read(1))

    # print(Cable.readline())
    for i in range(len(str(ByteStream))):
        Cable.write(bytes((ByteStream[i]), 'utf-8'))
        # responses.append(Cable.readline())
    Cable.write(bytes("3", 'utf-8')) #transmits a reset JTAG command
    responses = (Cable.readline())
    return (responses)

Data_Bank = []


def main():
    #bootup sequence (puts pins to safe values)
    global Data_Bank
    MainRegOutputControl.set_value(1)
    MemOutEnable.set_value(1)
    Ram_Addr_Enable.set_value(1)
    StackOutControl.set_value(1)
    CLK.set_value(0)
    InsRegControl.set_value(0)
    MemWriteControl.set_value(1)
    Data_Bank.append(JTAG_Data.copy())


    #prepare for read
    for signal in Main_Bus:
        signal.set_value(0)
    Count.set_value(0)
    CounterOutControl.set_value(0) #these will be outputting
    LowJumpRegLoad.set_value(0)
    HighJumpRegLoad.set_value(0)
    Data_Bank.append(JTAG_Data.copy())

    #preset the jump buffer
    LowJumpRegLoad.set_value(1)
    HighJumpRegLoad.set_value(1)
    JumpEnable.set_value(1)

    Data_Bank.append(JTAG_Data.copy())


    #preset_the_counter
    Count.set_value(1)
    Data_Bank.append(JTAG_Data.copy())
    JumpEnable.set_value(0)
    LowJumpRegLoad.set_value(0)
    HighJumpRegLoad.set_value(0)
    Data_Bank.append(JTAG_Data.copy())

    instructions = read_binaries(sys.argv[1])
    for instruction in instructions:
        #sets the bus
        for bit in range(len(Main_Bus)):
            Main_Bus[bit].set_value(int(instruction[-(bit+1)]))
        Count.set_value(0)
        MemWriteControl.set_value(0)

        Data_Bank.append(JTAG_Data.copy())

        #might need a do nothing state here

        #next meme addr
        MemWriteControl.set_value(1) #just stored it in memory
        Count.set_value(1)
        Data_Bank.append(JTAG_Data.copy())

    #set the program counter to the inital state
    for signal in Main_Bus:
        signal.set_value(1)
    Data_Bank.append(JTAG_Data.copy())

    LowJumpRegLoad.set_value(1)
    HighJumpRegLoad.set_value(1)
    Count.set_value(0)
    JumpEnable.set_value(1)
    Data_Bank.append(JTAG_Data.copy())

    Count.set_value(1)
    Data_Bank.append(JTAG_Data.copy())

    for signal in Main_Bus:
        signal.set_value(0)
    Data_Bank.append(JTAG_Data.copy())
    InsRegControl.set_value(1)
    Data_Bank.append(JTAG_Data.copy())



    flat_Data = [item for sublist in Data_Bank for item in sublist]

    ByteStream = ("".join([str(item) for item in flat_Data]))
    # print(ByteStream)

    response = Serial_Transmit(ByteStream)
    print("Attempted to Send: " + str(len(ByteStream)) + " JTAG bits")
    print("Acknowleged: " + str(len(str(response))) + " JTAG bits")
    print(response)


    # print("sucess")
    # print("Data contains: " + str(len(Data_Bank)) + " Transfer Operations")

main()
