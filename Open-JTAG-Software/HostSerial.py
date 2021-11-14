import serial
import time
import dearpygui.dearpygui as dpg

#detect host device
Slave = serial.Serial(port="COM6", baudrate=57600, timeout=0.1)

def write_read(x):
    Slave.write(bytes(x, 'utf-8'))
    time.sleep(1)
    data = Slave.readline()
    return data


dpg.create_context()
dpg.create_viewport(title="Custom Title", width=600, height=300)

with dpg.window(lable="Example Window"):
    dpg.add_title("Hello World")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
