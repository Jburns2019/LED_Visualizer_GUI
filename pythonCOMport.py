"""
File:       pythonCOMport.py\n
Author:     Henry Gillespie\n
Date:       May 25, 2021\n
Purpose:    This program defines the serial connection to the arduino by searching the available COM ports
"""

import serial.tools.list_ports
from tkinter import messagebox

def getPort(description: str, showBox: bool):
    """This function loops through the available COM ports to find the Arduino Nanos provided by Tekbots.\n
    When it has found the device, the function returns its COM port as a string."""
    serList = serial.tools.list_ports.comports()
    descriptions = []
    for i in range(len(serList)):
        descriptions.append(serList[i].description) # append description
    try:
        idx = descriptions.index(description)
        if showBox:
            messagebox.showinfo(f"{serList[idx].name} Selected", "Please click okay or close the window to continue.")
        return serList[idx].name # this will return COMX
    except:
        messagebox.showerror(f"{description} was unavailble", "Please ensure you have the desired com inserted." \
                "\nThis will allow you to play animations on the Arduino.\n" \
                "\nNote: You can still make custom animation and view them" \
                "\n\t in the demo tab, you just cannot send them.")
        return ""

def getDescriptions():
    """This function returns a list of the descriptions of the available COM ports"""
    serList = serial.tools.list_ports.comports()
    descriptions = []
    for i in range(len(serList)):
        descriptions.append(serList[i].description)
    return descriptions