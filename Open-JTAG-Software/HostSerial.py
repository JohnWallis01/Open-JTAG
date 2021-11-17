import serial
import time
import PySimpleGUI as sg
#detect host device
Slave = serial.Serial(port="COM6", baudrate=57600, timeout=0.1)


#binary graph to use for navigating the JTAG state machine

class Node(object):
    """docstring for Node."""

    def __init__(self, statename):
        self.statename = statename

    def set_links(self, one, zero):
        self.one = one
        self.zero = zero
#defining the graph


JTAG_RESET      =   Node("JTAG_RESET")
JTAG_IDLE       =   Node("JTAG_IDLE")
JTAG_SELECT_DR  =   Node("JTAG_SELECT_DR")
JTAG_CAPTURE_DR =   Node("JTAG_CAPTURE_DR")
JTAG_SHIFT_DR   =   Node("JTAG_SHIFT_DR")
JTAG_EXIT1_DR   =   Node("JTAG_EXIT1_DR")
JTAG_PAUSE_DR   =   Node("JTAG_PAUSE_DR")
JTAG_EXIT2_DR   =   Node("JTAG_EXIT2_DR")
JTAG_UPDATE_DR  =   Node("JTAG_UPDATE_DR")
JTAG_SELECT_IR  =   Node("JTAG_SELECT_IR")
JTAG_CAPTURE_IR =   Node("JTAG_CAPTURE_IR")
JTAG_SHIFT_IR   =   Node("JTAG_SHIFT_IR")
JTAG_EXIT1_IR   =   Node("JTAG_EXIT1_IR")
JTAG_PAUSE_IR   =   Node("JTAG_PAUSE_IR")
JTAG_EXIT2_IR   =   Node("JTAG_EXIT2_IR")
JTAG_UPDATE_IR  =   Node("JTAG_UPDATE_IR")


JTAG_RESET.set_links(JTAG_RESET, JTAG_IDLE)
JTAG_IDLE.set_links(JTAG_SELECT_DR, JTAG_IDLE)
JTAG_SELECT_DR.set_links(JTAG_SELECT_IR, JTAG_CAPTURE_DR)
JTAG_CAPTURE_DR.set_links(JTAG_EXIT1_DR, JTAG_SHIFT_DR)
JTAG_SHIFT_DR.set_links(JTAG_EXIT1_DR, JTAG_SHIFT_DR)
JTAG_EXIT1_DR.set_links(JTAG_UPDATE_DR, JTAG_PAUSE_DR)
JTAG_PAUSE_DR.set_links(JTAG_EXIT2_DR, JTAG_PAUSE_DR)
JTAG_EXIT2_DR.set_links(JTAG_UPDATE_DR, JTAG_SHIFT_DR)
JTAG_UPDATE_DR.set_links(JTAG_SELECT_DR, JTAG_IDLE)
JTAG_SELECT_IR.set_links(JTAG_RESET, JTAG_CAPTURE_IR)
JTAG_CAPTURE_IR.set_links(JTAG_EXIT1_IR, JTAG_SHIFT_IR)
JTAG_SHIFT_IR.set_links(JTAG_EXIT1_IR, JTAG_SHIFT_IR)
JTAG_EXIT1_IR.set_links(JTAG_UPDATE_IR, JTAG_PAUSE_IR)
JTAG_PAUSE_IR.set_links(JTAG_EXIT2_IR, JTAG_PAUSE_IR)
JTAG_EXIT2_IR.set_links(JTAG_UPDATE_IR, JTAG_SHIFT_IR)
JTAG_UPDATE_IR.set_links(JTAG_SELECT_DR, JTAG_IDLE)



jtag_state = None

#a bfs for a path to the target jtag state.
def PathSearch(current_node, end_key, visited=[], path=[]):
    visited.append(current_node)
    if current_node.statename == end_key:
        return (current_node, visited, True, path)

    if current_node.one not in visited:
         path.append(1)
         oneStatus = PathSearch(current_node.one, end_key, visited, path)
         if oneStatus[2] == True:
              return (current_node, visited, True, path)

    if current_node.zero not in visited:
         path.append(0)
         zeroStatus = PathSearch(current_node.zero, end_key, visited, path)
         if zeroStatus[2] == True:
              return (current_node, visited, True, path)

    #if we get to here we have gone down a path with no route to the state
    return (current_node, visited, True, path)
    #backtrack until we can get to a place we havent been to.


def SwitchState(target_state):
    global jtag_state
    if target_state == jtag_state:
        return -1
    transfer_sequence = PathSearch(jtag_state, target_state.statename)[3]
    for i in transfer_sequence:
        serial_transcieve(i,1)
    jtag_state = target_state
    return 0

def serial_transcieve(tms, tdi):
    Slave.write(bytes(tms, 'utf-8'))
    Slave.write(bytes(tdi, 'utf-8'))
    return Slave.read()

def reset_jtag():
    for i in range(5):
        serial_transcieve(1,1)
    global jtag_state
    jtag_state = JTAG_RESET
    return 0


#
# sg.theme("DarkAmber")
#
# layout = [  [sg.Text("Some text on Row 1")],
#             [sg.Text("Some More text on Row 2"), sg.InputText()],
#             [sg.Button("Ok"), sg.Button("Cancel"), sg.Button("else")]  ]
#
# window = sg.Window("Test", layout)
#
# while True:
#     event, value = window.read() #pole the window
#     if event == sg.WIN_CLOSED or event =="Cancel":
#         break
#     if event == "Ok":
#         print("You have entered",  value[0])
#
# window.close()
