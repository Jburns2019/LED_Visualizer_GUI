"""
Author: John Burns\n
Last Modified: 5/25/2021\n
OSU Email Address: burnsjo@oregonstate.edu\n
Course Number ECE 342\n
Project: LED Visualizer Group 2\n
Due Date: 5/28/2021
"""

from tkinter import *
from Animation import Animation
from Colors import *
import time
import sys

class Display:
    """
    Class made for displaying animations on a window.\n
        Animates at the speed of the animation.
        Play button and back button is disabled while animation is playing.
        Pause button pauses the animation in frame (togglable for easy quick clicking, disabled whne nothing is playing)
        Stop button enables play button and back button as well as restarts the animation (disabled when nothing is playing).\n
    parameters: window, a window for displaying a canvas on (Toplevel)\n
                animation, the animation to display (Animation)
                backBtnSettings, a way to get back to another window (txt, command)
    """
    def __init__(self, window: Toplevel, animation: Animation, backBtnSettings: list):
        #Save window for later.
        self.window = window
        self.window.protocol("WM_DELETE_WINDOW", sys.exit)

        #Is the program to be played, or are we paused?
        self.play = BooleanVar(value = True)

        #Make a frame for the buttons.
        self.frame = Frame(self.window)
        self.frame.pack(anchor = W)

        #Keep track of time.
        self.t = None

        #Save settings for later.
        self.backBtnSettings = backBtnSettings
        #Create the buttons.
        self.createBtns(self.frame)

        #Create a canvas for the display.
        self.canvas = Canvas(self.window, width = 500, height = 700, bg="#000000")
        self.canvas.pack()

        #Save animation features for later.
        self.animation = animation
        self.speed = int(1000/self.animation.getSpeed())

        #Provide a way to count within the class.
        self.counter = 0

    def createBtns(self, frame: Frame):
        """
        Creates the buttons used for controlling the animation.\n
            One button for starting the animation.
            One button for going back to the previous window.
            One button for pausing the animation.
            One button for stopping the animation.\n
        parameters: frame, the frame to create the buttons on (Frame).
        """
        #Create a fresh button for a nice layout.
        #Create the play button.
        self.playButton = Button(frame, text = "Play Animation", command = self.playAnimation)
        self.playButton.pack(side = LEFT)

        #Create the back button. Account for the user not having a command (no back button functionality)
        if len(self.backBtnSettings) == 1:
            self.backBtnSettings.append(None)
        self.backButton = Button(frame, text = self.backBtnSettings[0], command = self.backBtnSettings[1])
        self.backButton.pack(side = LEFT)
        
        #Create a togglable pause button.
        self.pauseButton = Checkbutton(frame, text="Pause Animation", onvalue=False, offvalue=True, variable=self.play, command = self.pauseBehavior, activeforeground="black")
        self.pauseButton.pack(side = LEFT)

        #Create a stop button.
        self.stopButton = Button(frame, text = "Stop Animation", command = self.stopAnimation)
        self.stopButton.pack(side = LEFT)

        #Disable the pause and stop button (nothing is playing right now).
        self.pauseButton['state'] = DISABLED
        self.stopButton['state'] = DISABLED

    def pauseBehavior(self):
        """
        Define the behavior of clicking pause.
        """
        #If we are playing, pause otherwise do nothing.
        if self.play.get():
            #If the animation is done, reenable the play and back button.
            if self.counter == self.animation.getNumFrames():
                #Clear animation if on last frame.
                self.resetCanvas()
            #If the play button is distabled, the animation must be paused.
            elif self.playButton['state'] == DISABLED:
                #Continue animation.
                self.drawCircles()

    def createCircle(self, x: int, y: int, r: int, **kwargs):
        """
        Helpfull function to create a circle with the oval function.\n
        parameters: x, the x coordinate (int)\n
                    y, the y coordinate (int)
                    r, the radius (int)
                    kwargs, extra arguments for create oval.
        """
        self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def resetCanvas(self):
        """
        Resets the canvas.
        """
        # If playing go ahead, otherwise return (prevents infinite recursion).
        if self.play.get():
            #clear the canvas.
            self.canvas.destroy()

            #Make a new canvas.
            self.canvas = Canvas(self.window, width = 500, height = 700, bg="#000000")
            self.canvas.pack()

            #Draw the next frame.
            self.window.after(0, self.drawCircles)

            #If the animation is done, reenable the play and back button.
            #   Disable the pause button and stop button.
            if self.counter == self.animation.getNumFrames():
                self.playButton['state'] = NORMAL
                self.backButton['state'] = NORMAL
                self.pauseButton['state'] = DISABLED
                self.stopButton['state'] = DISABLED
    
    def drawCircles(self):
        """
        Draw a frames of the animation.
        """
        #only draw a frame when the time has elapsed.
        if  not (not self.play.get() and self.counter != self.animation.getNumFrames()) \
                and self.counter < self.animation.getNumFrames() \
                and int((time.perf_counter() - self.t) * 1000) >= self.speed:
            #Record time.
            self.t = time.perf_counter()

            #Get the matrix.
            matrix = self.animation.getFrame(self.counter)
            for x in range(matrix.getxlen()):
                for z in range(matrix.getzlen()):
                    for y in range(matrix.getylen()):
                        #Create a 3D animation. Going back into the top right.
                        self.createCircle(x*100+y*10+25, 700-z*100-y*10-25, 5, fill = "#"+str(getHex(matrix.getVal(x, matrix.getylen() - 1 - y, z))))

            #Keep track of frame.
            self.counter += 1

            #Wait the preset amount of time and clear canvas for next animation.
            self.window.after(self.speed, self.resetCanvas)

    def playAnimation(self):
        """
        Rest the counter every time an animation is played.
        """
        #Reset the animation.
        self.counter = 0
        
        #Disable the play and back button, but activate the pause and stop button.
        self.playButton['state'] = DISABLED
        self.backButton['state'] = DISABLED
        self.pauseButton['state'] = NORMAL
        self.stopButton['state'] = NORMAL
        
        #Set time to the time that would have the program start.
        self.t = ((time.perf_counter() * 1000) - self.speed)/1000

        #Show the animation.
        self.drawCircles()
    
    def stopAnimation(self):
        """
        Stops the animation. This enables the play and stop button. It also enables the play\n
            button. If paused, it resets that as well.
        """
        #Put the counter at the end, so no currently waiting calls will run.
        self.counter = self.animation.getNumFrames()

        #If there is stuff disabled, the animation must be paused.
        # Otherwise it isn't. Prevents the play button from getting changed just by the stop button.
        if self.playButton['state'] == DISABLED:
            self.play.set(True)

            self.playButton['state'] = NORMAL
            self.backButton['state'] = NORMAL
            self.resetCanvas()