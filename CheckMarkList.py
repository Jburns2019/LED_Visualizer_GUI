"""
Author: John Burns\n
Last Modified: 5/25/2021\n
OSU Email Address: burnsjo@oregonstate.edu\n
Course Number ECE 342\n
Project: LED Visualizer Group 2\n
Due Date: 5/28/2021
"""

from tkinter import *
from Colors import *

class CheckButtonBar:
   """
   Setup the check buttons for setting colors. The panel of checks is colored and named based on the colors the checks represent.\n
   If no color is selected the listOfButtons will become disabled.\n
   parameters: master, the frame the color pannel will be put on (Frame)\n
               listOfButtons, a list of the dependent buttons (list(Button))\n
               text, the label used for the color selection (string).\n
               var, the variable that is changed with clicks (IntVar())\n
               command, the command to be used (function handle)\n
               commandlen, the number of commands available (int)\n
               txtLst, a list of txt for each command (list(string))\n
               badVal, the off value to avoid (int)
   """
   def __init__(self, master: Frame, listOfButtons: list, text: str, var: IntVar, command=None, commandlen = 0, txtLst = [], badVal = -1):
      #Make parameters accessible within the class.
      self.var = var
      self.command = command
      self.commandlen = commandlen
      self.txtLst = txtLst

      #prepare a list.
      self.checkList = []
      self.dependentButtons = listOfButtons

      #Make a labelFrame for describing the pannel.
      self.frame = LabelFrame(master, text=text)
      self.frame.pack()

      self.badVal = badVal

      #Setup the disabling and reenabling the dependant buttons.
      self.setupChecks()

   def setupChecks(self):
      """
      Make a list of CheckButtons that are off at -1 and on at the given numeric value.\n
         the variable, makes it so that the value will be accessible elsewhere without having to check it (auto updates).
      """
      #Make a list of CheckButtons and put them in the named pannel.
      #The length of the for loop is dependent on if there are commands expected.
      length = len(list(Colors.values())) if not self.command else self.commandlen

      for i in range(length):
         #Handle the case of black colors.
         fg = "white" if list(HexColors.keys())[i] == "000000" else "black"
         selectColor = "black" if list(HexColors.keys())[i] == "000000" else "white"
         
         #If there is a given command, then it isn't a colored list.
         if not self.command:
            #Creates a button, with the interest of allowing black to be seen.
            self.checkList.append(Checkbutton(
               self.frame,
               text = list(Colors.keys())[i],
               onvalue = list(Colors.values())[i],
               offvalue = -1,
               variable = self.var,
               command = self.activateSelection,
               activebackground='#' + str(list(HexColors.keys())[i]),
               activeforeground="black",
               fg = fg,
               selectcolor = selectColor,
               width = 11,
               bg = '#' + str(list(HexColors.keys())[i]),
               anchor = W
            ))
         else:
            #Make a generic check button list.
            self.checkList.append(Checkbutton(
               self.frame,
               text = self.txtLst[i],
               onvalue = i,
               offvalue = -1,
               variable = self.var,
               command = self.activateCommand
            ))
         #Pack the buttons as they come in.
         self.checkList[i].pack(anchor = W)

   def activateCommand(self):
      """
      Define the functionality for selecting a box.\n
         If a box is enabled use the command, otherwise do nothing.\n
         If an unreachable badValue is given, then command is executed every time the check is toggled.
      """
      if self.var.get() != self.badVal:
         self.command()

   def activateSelection(self):
      """
      Define the functionality for selecting a box.\n
         If a box is selected then the dependent buttons\n
         are enabled, otherwise the dependent buttons are disabled.
      """
      if self.var.get() != -1:
         for i in range(len(self.dependentButtons[0])):
            self.dependentButtons[0][i]['state'] = NORMAL
      
      elif self.var.get() == -1:         
         for i in range(len(self.dependentButtons[0])):
            self.dependentButtons[0][i]['state'] = DISABLED