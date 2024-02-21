"""
Author: John Burns
Last Modified: 5/15/2021
OSU Email Address: burnsjo@oregonstate.edu
Course Number ECE 342
Project: LED Visualizer Group 2           Due Date: 5/28/2021
"""

from tkinter import *

class SliderFrames:
    """
    Built to makes slider frames more intuitive for the gui.\n
    Make a strips of frames and insert frames of sliders into those strips based on the infos parameter.\n

    Though this could be expandable with multiple
        types of sliders as well as sub sliders, that is untested and likely will look awfull.
    parameters: frame, a frame to put the sliders on.\n
                infos, an array of arrays. Each sub array should have the parameter list for the creation of a slider.
    """
    def __init__(self, frame: Frame, infos: list[list]):
        #Make a frame for the slider.
        self.frame = Frame(frame)
        self.frame.pack(anchor = W)
        
        #Make it easy to retrieve the frames and scales created.
        self.listofscaleFrame_sels = [[], []]
        self.stripFrames = []

        #Create strips of frames, with each frame containing LabelFrames of sliders.
        for i in range(len(infos)):
            #Create a frame to put sliders in (horizontally)
            self.stripFrames.append(Frame(self.frame))
            self.stripFrames[i].pack(anchor = W)

            for j in range(len(infos[i])):
                #Create the individual slider in the strip.
                infos[i][j].insert(0, self.stripFrames[i])
                self.listofscaleFrame_sels[i].append(self.scaleSetup(infos[i][j]))

    def scaleSetup(self, info: list):
        """
        Make a scale based on the parameters given in info.\n
        parameters: info, a list of parameters in the format selFrame (Frame class), title (string), 
            lo (int), hi (int), variable (needs a get function), command (function handle).\n
        returns: references to frames and sliders created (list).
        """
        #Parse info.
        selFrame, title, from_, to, var, command = info

        #Create a LabelFrame for the slider.
        scaleFrame = LabelFrame(selFrame, text = title)
        scaleFrame.pack(side = LEFT, anchor=W)

        #Create a slider based on the info parameter.
        sel = Scale(scaleFrame, from_=from_, to=to, command = command, orient=HORIZONTAL)
        
        #Set the default value.
        sel.set(var.get())
        sel.pack(side = LEFT)
        
        return [scaleFrame, sel]