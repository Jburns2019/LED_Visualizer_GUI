#!/usr/bin/python
"""
Author: John Burns\n
Last Modified: 5/26/2021\n
OSU Email Address: burnsjo@oregonstate.edu\n
Course Number ECE 342\n
Project: LED Visualizer Group 2\n
Due Date: 5/28/2021
"""

from tkinter import *
from Animation import Animation
from ArduinoInterface import *
from Layer import LEDLayer
from CheckMarkList import CheckButtonBar
from Slider import SliderFrames
from Display import Display
from pythonCOMport import *
import sys
import numpy as np

#Constants that increase the readability of the slider array in one of the functions shown below.
LAYER = 0
FRAME = 1
SPEED = 2
FRAMECNT = 3
EFFECT = 4

class MultiWindow:
   """
   A class that sets up the visualizer multiwindow.\n
   The first window sends numeric data to sendValToArd(num) based on the chosen animation.\n
   The second window is built to customize animation 4, 5, and 6.\n
   All three animations are saved during the session, but would have to be rebuilt if the session was closed.\n
   Clicking submit sends the animations to animationsForHeader(animations) based on the selections made in the interface.\n
   To change an animation, select the animation (default 4), choose a frame (default 0), choose a layer (default 0),
      choose a color (default none or black), finally click an LED.\n
   You will not only keep animations when going to other tabs, you will also keep the place you were last working on that animation
      when you come back.\n
   The speed of an animation is adjustable. Just adjust the slider.\n
   The maximum frame count of an animation is adjustable. Just adjust the slider.\n
      Adjusting the maximum frame count will delete frames past that frame.
      You needn't worry about the current frame slider. It will be always be in a valid state (will be reduced if max count is lower).\n
   You may fill the animation with set commands. It is trivial to add more, just add them in the Animation.py file.\n
   You may demo the animations by clicking the play Animation button.\n

   For the curious... non of the features of the default animation (1, 2, and 3) are adjustable. Which is why they don't show up under
      advanced settings bar.

   Verified os: Windows and Linux. Due to the pack and grid methods, the windows should show up with the proper size on any system.
      The system as a whole will not be cross platform, but this gui is.\n

   Parameters: master, the top frame (Frame).
   """
   def __init__(self, master: Tk):
      #Setup windows.
      self.master = master
      self.secondaryWin = None
      self.playWindow = None

      #Prepare for button layer.
      self.currentBtnLst = [None]
      self.currentBtnLayer = None

      #Prepare for sliders.
      self.sliders = None

      #setup global variables that can be changed with widget actions.
      #These do not change between animations.
      self.colorChosen = IntVar(value = -1)
      self.commandChosen = IntVar(value = -1)
      self.animationChosen = IntVar()
      self.comChosen = IntVar(value = -1)

      #These do change between animations, so there is 1 for each animation.
      self.animations = []
      self.speeds = []
      self.frameCnts = []
      self.layers = []
      self.frames = []
      self.effects = []
      for i in range(3):
         self.animations.append(Animation())
         self.speeds.append(IntVar(value = self.animations[self.animationChosen.get()].getSpeed()))
         self.frameCnts.append(IntVar(value = self.animations[self.animationChosen.get()].getNumFrames()))
         self.layers.append(IntVar())
         self.frames.append(IntVar())
         self.effects.append(IntVar())

      #Make the com frame based on available coms.
      self.sendBtns = []
      self.comFrame = None
      self.submitBtn = None
      self.updateComFrame()

      #layout the buttons and their functionality.
      self.setupMainWindow(master)

      #Allow for creating another window with
      self.nextBtn = Button(self.master, text="Advanced Settings", width = 15, command=self.advancedSettingOptions)
      self.nextBtn.grid(row = 2, column = 1)

      #Create an uodate button.
      self.updateBtn = Button(self.master, text="Update COMs", width = 15, command=self.updateComFrame)
      self.updateBtn.grid(row = 2, column = 2)      

   def updateComDependentBtns(self):
      """
      update the sending buttons based on whether a com is chosen.
      """
      #Activate for selected, Disabled if not.
      val = NORMAL if len(self.listOfComs) > 0 and self.comChosen.get() != -1 else DISABLED

      #Update the buttons based on their functionality.
      for i in range(len(self.sendBtns)):
         self.sendBtns[i]['state'] = val
      if self.submitBtn:
         self.submitBtn['state'] = val

   def updateComFrame(self):
      """
      Update the com frame.
      """
      #Destroy the com frame if it exists.
      if self.comFrame:
         self.comFrame.destroy()

      #Find the descriptions of the available ports.      
      self.listOfComs = getDescriptions()
      #If there aren't any coms, remove chosen com.
      if len(self.listOfComs) == 0:
         self.comChosen.set(-1)
      
      #Make a frame for the com. Put it at the far right. Shape it based number of coms available.
      self.comFrame = Frame(self.master)
      self.comFrame.grid(row = 0, column=3, rowspan = len(self.listOfComs) if len(self.listOfComs) > 3 else 3, sticky = N)

      #Update the buttons.
      self.updateComDependentBtns()

      #make the button list.
      self.comChecks = CheckButtonBar(self.comFrame, None, 'Select a COM', self.comChosen, self.findPort(self.listOfComs), len(self.listOfComs), self.listOfComs, -2)

   def findPort(self, listOfComs: list):
      """
      update the port and get the ports. Verbose mode is activated if a comport was chosen.\n
      Returns a function handle to be executed when check button is clicked. [funct1, funct2].
      """
      return lambda: [self.updateComFrame(), getPort(listOfComs[self.comChosen.get()], True if self.comChosen.get() > -1 else False)]

   def setupMainWindow(self, basic):
      """
      Sets up the main window. The main wondow contains 6 windows in a 2*3 grid of buttons.\n
      The 6 buttons send a number to a function to be used by the Arduino Interface.
      """
      #Keep track of the button number.
      counter = 0
      #Make 2 rows.
      for i in range(2):
         #Make 3 columns.
         for j in range(3):
            #Create uniform buttons with a function handle that allows for a number to be passed every time it is called.
            self.sendBtns.append(Button(basic, text =f"Animation {counter+1}", width = 15, height = 1, command = self.choiceLambda(counter)))
            self.sendBtns[counter].grid(row = i, column = j)
            if len(self.listOfComs) == 0 or self.comChosen.get() == -1:
               self.sendBtns[counter]['state'] = DISABLED
            counter += 1
   
   def choiceLambda(self, num: int):
      """
      function handle generator. This allows the buttons to use a command with a numeric input.\n
      parameters: num, the numeric representation of the user's choice.\n
      returns: a lambda, a function handle that can be run any time one of the determined buttons is clicked.
      """
      return lambda: self.displayChoice(num)

   def displayChoice(self, num: int):
      """
      Let the user know what they did as well as let them know how to continue.\n
      parameters: num, the numeric representation of the user's choice.
      """
      #Send the value over the to arduino once the user closes the messagebox.
      sendValToArd(num, self.listOfComs[self.comChosen.get()])

   def sendAnimationsLam(self, animations: list):
      """
      function handle generator. This allows one function to control multiple events via a parameter.\n
      parameters: animation, the number attached to the animation button clicked.\n
      returns: a lambda, a function handle that can be run any time, with the preset value.
      """
      return lambda: animationsForHeader(animations, self.listOfComs[self.comChosen.get()])

   def advancedSettingOptions(self):
      """
      Set up an advanced setting window temporarily closing the main window. This setup process only needs
         to happen if this Secondary Window has not already been setup.\n
      As can be seen below the functionaliy of this is split into making a tab frame and then an action frame.\n
         The tab frame allows one to select an animation to modify, go to the basic settings window, or send the animation
         to the arduino (Submit)
      """
      #If a window is not already setup. Make one.
      if not self.secondaryWin:
         #Make a top level window frame.
         self.secondaryWin = Toplevel()
         #If the user closes the GUI, exit the program.
         self.secondaryWin.protocol("WM_DELETE_WINDOW", sys.exit)

         #Setup the top button (tab) frame and action frame.
         #The action frame is the main place where settings are changed.
         tabFrame = Frame(self.secondaryWin)
         actionFrame = Frame(self.secondaryWin)
         tabFrame.pack(anchor = W)
         actionFrame.pack(anchor = W)

         #Allow easy access to the future btn pannel.
         self.btnFrame = None
         
         #Setup 3 animation tabs. They are Animations whose matrix will be edited by changing the colors of the buttons.
         for i in range(3):
            Button(tabFrame, text =f"Animation {i+4}", width = 12, command = self.selectActLam(i)).pack(side = LEFT)
         Button(tabFrame, text="Play Animation", width = 12, command = self.playAnimationWindow).pack(side = LEFT)
         #Allow the user to return to the original window.
         Button(tabFrame, text="Basic Settings", width = 12, command=self.basicSettingOptions).pack(side = LEFT)
         #Allow the user to submit the edited animations to the Arduino.
         self.submitBtn = Button(tabFrame, text="Submit", bg = 'green', width = 12, command = self.sendAnimationsLam(self.animations))
         self.submitBtn.pack(side = LEFT)

         #Put the window in the top left so that no matter the os, it will show as best as possible.
         self.secondaryWin.geometry("+0+0")
         #Hide the main window.
         self.master.withdraw()

         #Remove the animation demo window.
         if self.playWindow:
            self.playWindow.destroy()
            self.playWindow = None
         
         #Setup the action frame.
         self.setupActionFrame(actionFrame)
      else:
         #If the secondary window has already been setup, then just show the secondary window and hide the main window.
         #withdraw() turns the window into a hidden icon. deiconify() undoes this action.
         self.secondaryWin.deiconify()
         #if there is a play window, remove it.
         if self.playWindow:
            self.playWindow.destroy()
            self.playWindow = None
         self.master.withdraw()

      self.submitBtn['state'] = DISABLED if len(self.listOfComs) == 0 or self.comChosen.get() == -1 else NORMAL
   
   def basicSettingOptions(self):
      """
      Method for togling the visible window.\n
         Hides the secondary window and shows the primary window.
      """
      self.secondaryWin.withdraw()
      self.master.deiconify()
   
   def playAnimationWindow(self):
      """
      Create a play Animation window.
      """   
      #Create, title, place, and define closing behavior.
      self.playWindow = Toplevel()
      self.playWindow.title("Animation Demo")
      self.playWindow.geometry("+0+0")
      self.playWindow.protocol("WM_DELETE_WINDOW", sys.exit)

      #Hide the secondary window.
      self.secondaryWin.withdraw()

      #Show the display window, with ability to go back to secondary window.
      Display(self.playWindow, self.animations[self.animationChosen.get()], ["Advanced Settings", self.advancedSettingOptions])

   def setupActionFrame(self, actionFrame: Frame):
      """
      Sets up the frame in the secondary window where the user makes all the edits.\n
      parameters: actionFrame, the frame to be used for the action frame.
      """
      #Save the frame used for the buttons (changes every time one of the settings changes).
      self.btnFrame = Frame(actionFrame)
      #Make a frame for the color selection frame.
      colorSelFrame = Frame(actionFrame)
      #make a command frame for the far right.
      commandSelFrame = Frame(actionFrame)

      #Put the frames on the window with some asthetic intent.
      colorSelFrame.pack(side = LEFT, fill = Y)
      self.btnFrame.pack(side = LEFT, fill = BOTH)
      commandSelFrame.pack(side = LEFT, fill = Y)

      #Make the slider frames and let them be accessessable elsewhere.
      self.sliders = SliderFrames(self.btnFrame, self.getInfo())

      #Setup the button layer functionality.
      self.LEDSelectionSetup()

      #Setup a color selection bar which enable/disable the buttons as well as allow you to click the buttons until the user decides
      #to change color.
      CheckButtonBar(colorSelFrame, self.currentBtnLst, 'Possible Colors', self.colorChosen)

      #Add a check list for the right side of the gui.
      listOfCommands = self.animations[self.animationChosen.get()].specialAnimations
      CheckButtonBar(commandSelFrame, None, 'Choose a Command', self.commandChosen, self.doAction, len(listOfCommands), np.array(listOfCommands)[:, 0].tolist())

   def doAction(self):
      """
      Fill the animation acording to the button checked. Update the layer buttons as well.
      """
      #Remove the current btn layer.
      self.currentBtnLayer.remove()

      #Execute the command on the current animation.
      if self.effects[self.animationChosen.get()].get() == 0:
         self.animations[self.animationChosen.get()].specialAnimations[self.commandChosen.get()][1](self.frames[self.animationChosen.get()].get(), self.layers[self.animationChosen.get()].get(), self.colorChosen.get())
      elif self.effects[self.animationChosen.get()].get() == 1:
         self.animations[self.animationChosen.get()].specialAnimations[self.commandChosen.get()][1](self.frames[self.animationChosen.get()].get(), self.colorChosen.get())
      elif self.effects[self.animationChosen.get()].get() == 2:
         self.animations[self.animationChosen.get()].specialAnimations[self.commandChosen.get()][1](self.colorChosen.get())

      #find the chosen animation based on the list of animations.
      chosenAnimation = self.animations[self.animationChosen.get()]
      #Setup the layer corresponding to the layer information chosen.
      self.setLayer(chosenAnimation, self.frames[self.animationChosen.get()].get())

      self.commandChosen.set(-1)
   
   def getInfo(self):
      """
      Retrieve the information required for the sliders.\n
         It is setup in such a way that more of either type of slider can be added fairly simply.
         format of the parameters is: text (string), lo (int), hi (int), variable (needs .get() method), command (function handle).\n
      returns: info, a 2 element array of slider parameters.
      """
      #Get the chosen matrix based on the chosen animation and chosen frame (matrix).
      matrix = self.animations[self.animationChosen.get()].getFrame(self.frames[self.animationChosen.get()].get())
      #Parameters for the info changing sliders (layer and frame).
      posInfo = [['Choose Layer', 0, matrix.getzlen()-1, self.layers[self.animationChosen.get()], self.selAct], \
         ['Choose Frame', 0, self.animations[self.animationChosen.get()].getNumFrames()-1, self.frames[self.animationChosen.get()], self.selAct]]
      
      #Parameters for the feature changing sliders (speed and max frame count).
      featureInfo = [['Choose Speed (fps)', 1, self.animations[self.animationChosen.get()].getSpeed(), self.speeds[self.animationChosen.get()], self.selAct], \
         ['Max Frame Count', 1, self.animations[self.animationChosen.get()].getNumFrames(), self.frameCnts[self.animationChosen.get()], self.selAct], \
         ['Effect (layer, frame, whole)', 0, 2, self.effects[self.animationChosen.get()], self.selAct]]
      
      return [posInfo, featureInfo]

   def LEDSelectionSetup(self):
      """
      Setup the selection of LEDs. A 5x5 (size of a matrix layer) button frame is presented. Based on the layer, animation, frame,
         and color the values of the animations can be changed with a click. The change in the animations is reflected by the
         color of these buttons.
      """
      #Get the chosen matrix based on the chosen animation and chosen frame (matrix).
      matrix = self.animations[self.animationChosen.get()].getFrame(self.frames[self.animationChosen.get()].get())
      #Make a new btn layer.
      self.currentBtnLayer = LEDLayer(self.btnFrame, matrix, self.colorChosen, self.layers[self.animationChosen.get()])
      #Add the button layer to the button list. This makes it easier to destroy and rebuild later.
      self.currentBtnLst[0] = self.currentBtnLayer.buttonLst

   def selectActLam(self, animSelected: int):
      """
      function handle, allows multiple buttons to have the same function with slightly different (preset) values.\n
      parameters: animSelected, the animation that is being edited (int).\n
      returns: function handle, a way to change the features of the animation being changed based on the variables set up\n
         and animation edited so far (lambda).
      """
      return lambda: self.selAnimAct(animSelected)
   
   def selAnimAct(self, animSelected: int):
      """
      Definition of what happens when an animation is selected. It resets the sliders to the values they were when editing that
         animation as well as changes the btn layer to the layer corresponding to the sliders.\n
      parameters: animSelected, the animation being edited (int).
      """
      #Remove the current btn layer.
      self.currentBtnLayer.remove()

      #update the chosen animation variable.
      self.animationChosen.set(animSelected)

      #get the scales from the information saved on the sliders (when the sliders were created).
      scales = []
      for strip in range(len(self.sliders.listofscaleFrame_sels)):
         for scale in range(len(self.sliders.listofscaleFrame_sels[strip])):
            scales.append(self.sliders.listofscaleFrame_sels[strip][scale][1])
      
      #Update the scales to how they were with the current animation.
      scales[LAYER].set(self.layers[self.animationChosen.get()].get())
      scales[FRAME].set(self.frames[self.animationChosen.get()].get())
      scales[SPEED].set(self.speeds[self.animationChosen.get()].get())
      scales[FRAMECNT].set(self.frameCnts[self.animationChosen.get()].get())
      scales[EFFECT].set(self.effects[self.animationChosen.get()].get())

      #find the chosen animation based on the list of animations.
      chosenAnimation = self.animations[self.animationChosen.get()]
      #Setup the layer corresponding to the layer information chosen.
      self.setLayer(chosenAnimation, self.frames[self.animationChosen.get()].get())
   
   def selAct(self, selected: int):
      """
      Very similar to the above method however it had a fundemental difference. One is that
         it is called by sliders (which pass changed parameters so animSelected would be flagged
         inapropriately), but also that the variable are updated based on the sliders rather than
         the slider on the variables. Since one slider is being used for all three animations
         (akward things happen if you try to delete and resetup the sliders due to the variables being attached)
         the best course of action is to update the variables based on the sliders and then when the animation
         changes, change the slider values to those animation dependent variables.\n
      parameters: selected, the feature selected. Ghost parameter, not in use as it would require a seperate function\n
         for each parameter. As seen in the description an adequate work arond was found.
      """
      #Remove the current button layer.
      self.currentBtnLayer.remove()

      #get the scales from the information saved on the sliders (when the sliders were created).
      scales = []
      for strip in range(len(self.sliders.listofscaleFrame_sels)):
         for scale in range(len(self.sliders.listofscaleFrame_sels[strip])):
            scales.append(self.sliders.listofscaleFrame_sels[strip][scale][1])

      #Update the variables for the animation depended variables based on the scale's current value.
      #Update the layer variable based on the slider.
      self.layers[self.animationChosen.get()].set(scales[LAYER].get())
      #Update the maximum frame variable based on the slider.
      self.frameCnts[self.animationChosen.get()].set(scales[FRAMECNT].get())
      #Update the maximum effect variable based on the slider.
      self.effects[self.animationChosen.get()].set(scales[EFFECT].get())

      #Protect the user from moving the frame slider past the maximum value.
      if scales[FRAME].get() < scales[FRAMECNT].get():
         #Update the frame variable based on the slider.
         self.frames[self.animationChosen.get()].set(scales[FRAME].get())
      else:
         #Reset the slider to the maximum value if the user tried to take it past.
         scales[FRAME].set(scales[FRAMECNT].get()-1)
      
      #Update speed variable based on the slider.
      self.speeds[self.animationChosen.get()].set(scales[SPEED].get())
      
      #Make the chosen animation easily accessable.
      chosenAnimation = self.animations[self.animationChosen.get()]
      #Update the speed and maximum frame count of the chosen animation to the values stored in the variables updated above.
      chosenAnimation.setSpeed(self.speeds[self.animationChosen.get()].get())
      chosenAnimation.changeFrameCnt(self.frameCnts[self.animationChosen.get()].get())

      #If the user is moving the maximum frame count below the frame selected,
      #  move frame selected with it.
      frameNum = 0
      if chosenAnimation.getNumFrames() <= self.frames[self.animationChosen.get()].get():
         #The frame chosen must be the maximum frame possible (0 indexed list)
         frameNum = chosenAnimation.getNumFrames() - 1
      else:
         #The frame chosen is just the value in the variable.
         frameNum = self.frames[self.animationChosen.get()].get()
      
      #Update the layer based on the animation and frame number.
      #Be warned that lowering the frame number will erase any custom frames in the animation after that point.
      self.setLayer(chosenAnimation, frameNum)

   def setLayer(self, chosenAnimation: IntVar, frameNum: int):
      """
      Create a new layer based on the chosen values.\n
      parameters: chosenAnimation, the animation that has been chosen (IntVar).\n
                  frameNum, the frame (matrix) to select (int).
      """
      #Make the chosen Matrix easy to access.
      chosenMatrix = chosenAnimation.getFrame(frameNum)
      #Create a new button layer.
      self.currentBtnLayer = LEDLayer(self.btnFrame, chosenMatrix, self.colorChosen, self.layers[self.animationChosen.get()])
      self.currentBtnLst[0] = self.currentBtnLayer.buttonLst
