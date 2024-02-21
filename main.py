"""
Runs the ECE 342 visualizer program.
"""

from MultiWindow import MultiWindow
from tkinter import Tk

if __name__ == '__main__':
    #Initilizer a GUI window, with a title at the top left of the screen.
    basic = Tk()
    basic.title("LED Visualizer GUI")
    basic.geometry("+0+0")

    #Setup all frames and windows in the gui.
    window = MultiWindow(basic)
    #Allow the program to terminate if the main window is closed.
    basic.protocol("WM_DELETE_WINDOW", basic.destroy)
    #Listen for events in the setup gui until the window is destroyed.
    basic.mainloop()