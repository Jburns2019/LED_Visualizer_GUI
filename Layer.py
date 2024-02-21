"""
Author: John Burns\n
Last Modified: 5/15/2021\n
OSU Email Address: burnsjo@oregonstate.edu\n
Course Number ECE 342\n
Project: LED Visualizer Group 2\n
Due Date: 5/28/2021
"""

from tkinter import *
from Colors import *
from Matrix import LEDMatrix
import numpy as np

class LEDLayer:
   """
   Built for the display and edit of the layer values of a given layer and matrix.\n
               It is implemented in such a way that buttons are only selectable if a color is selected.
               The buttons will also change color in accordance with the color chosen.\n
   paramaters: master, the frame that button layer will be placed into (Frame).\n
               matrix, the LED layer is within (Matrix).
               colorChosen, the variable assigned for changing a button's color (IntVar)
               layerChosen, the variable assigned for keeping track of the desired layer (IntVar).
   """
   def __init__(self, master: Frame, matrix: LEDMatrix, colorChosen: IntVar, layerChosen: IntVar):
      #Make a label frame that tells the user how to use it.
      self.frame = LabelFrame(master, text = 'Select LEDs Below')
      self.frame.pack(anchor = W)

      #Make the parameters easily accessable elsewhere.
      self.matrix = matrix
      self.layerChosen = layerChosen
      #Get the row and column of a set layer, using numpys easy splicing.
      self.layer = np.array(self.matrix.getMatrix())[:, :, self.layerChosen.get()].tolist()
      self.colorChosen = colorChosen

      #Make the buttons available to the class.
      self.buttonLst = []

      counter = 0
      #Create strips of buttons.
      stripFrames = []
      for y in range(len(self.layer[0])):
         stripFrames.append(Frame(self.frame))
         stripFrames[y].pack(anchor = W, pady = 10)

         for x in range(len(self.layer)):            
            #Make the button unusable if no color has been selected.
            state = NORMAL if colorChosen.get() != -1 else DISABLED

            #Make a button with the bg color of that layer's value, name it and define it based on its positioning.
            btn = Button(stripFrames[y], bg = '#' + str(getHex(self.layer[x][y])), width = 5, state = state, command = self.defAction(x, y, counter))
            btn.pack(side = LEFT, padx = 10)
            #Put the button in the list.
            self.buttonLst.append(btn)
            counter += 1
   
   def remove(self):
      """
      Make it easy to remove the layer so that it can be easily replaced.
      """
      self.frame.pack_forget()
      self.frame.destroy()

   def defAction(self, x: int, y: int, btnRef: Button):
      """
      Define the action for an active button in the button layer being clicked.\n
      parameters: x, the column number in the button layer (int).\n
                  y, the row number in the button layer (int).
                  btnRef, the direct reference to the button in the grid created (Button).\n
      returns: function handle, a preset function handle that can be run whenever an even is read (lambda).
      """
      return lambda: self.changeMatrix(x, y, btnRef)

   def changeMatrix(self, x: int, y: int, btnRef: Button):
      """
      Change the matrix based on the actions of the user.\n
         When a button is clicked (that is clickable), the color of that button should change to the chosen color
         and the matrix value should also change.\n
      parameters: x, the column number in the button layer (int).\n
                  y, the row number in the button layer (int).
                  btnRef, the direct reference to the button in the grid created (Button).
      """
      #Update the layer based on the user's action.
      self.matrix.setVal(x, y, self.layerChosen.get(), self.colorChosen.get())
      self.layer = np.array(self.matrix.getMatrix())[:, :, self.layerChosen.get()].tolist()

      #Set the color of the button based on the user's selection.
      self.buttonLst[btnRef]['bg'] = '#' + str(getHex(self.colorChosen.get()))