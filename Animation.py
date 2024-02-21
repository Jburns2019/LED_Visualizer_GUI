"""
Author: John Burns\n
Last Modified: 5/27/2021\n
OSU Email Address: burnsjo@oregonstate.edu\n
Course Number ECE 342\n
Project: LED Visualizer Group 2\n
Due Date: 5/28/2021
"""

from Matrix import LEDMatrix
import random
from Colors import *

class Animation:
    """
    The definition for how an Animation can be defined.\n
        Animations are lists of LEDMatrices with an adjustable frame count and speed.
        You can add animation filler functions at the end and then add them to the special Animations list.
    3 constructors\n
        Animation(x, y, z, lim, frameCnt, speed)
            x, number of columns in an LEDMatrix (int).
            y, number of rows in an LEDMatrix (int).
            z, number of layers in an LEDMatrix (int).
            lim, maximum allowable value (int).
            frameCnt, number of frames (int).
            speed, speed of the animation in fps (int).\n
        Animation(frameCnt, speed)
            Default Matrix() constructor (5x5x7) with a lim of 63.
            frameCnt, number of frames (int).
            speed, speed of the animation in fps (int).\n
        Animation()
            Default Matrix() constructor (5x5x7) with a lim of 63.
            Default frameCnt of 30.
            Default speed of 20.
    """
    def __init__(self, *args):
        #Full parameter list.
        if len(args) == 6:
            x, y, z, lim, frameCnt, speed = args
            self.animation = [LEDMatrix(x, y, z, lim) for frame in range(frameCnt)]
            self.frameCnt = frameCnt
            self.viewable = self.frameCnt
            self.speed = speed
        #Default matrix with custom speed and frame count.
        elif len(args) == 2:
            frameCnt, speed = args
            self.animation = [LEDMatrix() for frame in range(frameCnt)]
            self.frameCnt = frameCnt
            self.viewable = self.frameCnt
            self.speed = speed
        #Default animation.
        elif len(args) == 0:
            self.animation = [LEDMatrix() for frame in range(30)]
            self.frameCnt = 30
            self.viewable = self.frameCnt
            self.speed = 30
        
        #Easy way for coder to add more custom animations.
        self.specialAnimations = []
        self.specialAnimations.append(["Sequential", self.seq])
        self.specialAnimations.append(["Random", self.rand])
        self.specialAnimations.append(["Set Color", self.solid])
        self.specialAnimations.append(["Clear", self.clear])

    def getNumFrames(self):
        """
        Method for getting number of frames.\n
        returns: viewable, the effective number of available frames an animation has (int).
        """
        return self.viewable
    
    def setSpeed(self, speed: int):
        """
        Method for changing the speed of an animation.\n
        parameters: speed, the speed to run the animation at (in fps, int).
        """
        self.speed = speed

    def getSpeed(self):
        """
        Method for getting the Animation's speed.\n
        returns: speed, the Animations current speed (int).
        """
        return self.speed

    def setFrame(self, frame: int, matrix: LEDMatrix):
        """
        Method for adjusting the number of frames.\n
        parameters: frame, the matrix to edit (int).\n
                    matrix, the matrix to replace the current matrix with (Matrix).
        """
        self.animation[frame] = matrix

    def getFrame(self, frame: int):
        """
        Method for getting a frame from the Animation.\n
        parameters: frame, the frame of interest (int).\n
        returns: matrix, the Matrix at the given frame (Matrix).
        """
        return self.animation[frame]
    
    def changeFrameCnt(self, newFrameCnt: int):
        """
        Method for adjusting the number of frames in an Animation.\n
        parameters: newFrameCnt, the desired frame count for the Animation (int).
        """
        self.viewable = newFrameCnt

    def clear(self, *args):
        """
        Method for clearing the animation.\n
            set effected part's LEDs to off.\n
        parameters: args -> frame, layer, val (layer effect, val doesn't matter)\n
                            frame, val (frame effect, val doesn't matter)
                            val (whole animation, val doesn't matter)
        """
        args = list(args)
        args[-1] = 0
        self.fill(args)
    
    def seq(self, *args):
        """ 
        Making sequential colors on animation.\n
            set effected part to colors in a sequential order.\n
        parameters: args -> frame, layer, val (layer effect, val doesn't matter)\n
                            frame, val (frame effect, val doesn't matter)
                            val (whole animation, val doesn't matter)
        """
        args = list(args)

        #give special arguement value, unreachable otherwise.
        args[-1] = -3

        self.fill(args)

    def rand(self, *args):
        """ 
        Customized method for adding random colors.\n
            set effected part to random color values.\n
        parameters: args -> frame, layer, val (layer effect, val doesn't matter)\n
                            frame, val (frame effect, val doesn't matter)
                            val (whole animation, val doesn't matter)
        """
        args = list(args)

        #give special arguement value, unreachable otherwise.
        args[-1] = -2

        self.fill(args)

    def solid(self, *args):
        """
        Custom method for adding solid color.\n
            set effected part to the decided color.\n
        parameters: args -> frame, layer, color (layer effect)\n
                            frame, color (frame effect)
                            color (whole animation)
        """
        self.fill(list(args))

    def fill(self, args:list):
        """
        Modular function for setting\n
        parameters: args -> frame, layer, val (layer effect)\n
                            frame, val (frame effect)
                            val (whole animation)\n
            val may be of the color dictionary or a specific value that has meaning
                -2: random
                -3: sequential
        """
        #Choose frame length based on the parameter list.
        frameLen = self.getNumFrames()
        if len(args) > 1:
            frameLen = args[0]
        
        counter = 0

        lower = frameLen if len(args) > 1 else 0
        upper = frameLen+1 if len(args) > 1 else frameLen
        for frame in range(lower, upper):
            matrix = self.getFrame(frame)

            #Choose layer count based on the parameter list.
            layerCnt = matrix.getzlen()
            if len(args) > 2:
                layerCnt = args[1]

            lower = layerCnt if len(args) > 2 else 0
            upper = layerCnt+1 if len(args) > 2 else layerCnt
            for layer in range(lower, upper):
                for y in range(matrix.getylen()):
                    for x in range(matrix.getxlen()):
                        #Choose method of filling based on specialized parameter values.
                        #-1 means no color has been selected (bad state).
                        if args[-1] == -2:
                            matrix.setVal(x, y, layer, random.choice(list(HexColors.values())))
                        
                        elif args[-1] == -3:
                            matrix.setVal(x, y, layer, list(HexColors.values())[counter])
                            
                            #Reset the counter when it hits max.
                            if counter < len(list(HexColors.values())) - 1:
                                counter += 1
                            else:
                                counter = 0
                        
                        elif args[-1] >= 0:
                            matrix.setVal(x, y, layer, args[-1])

    def toString(self):
        """
        Intelligent stringification of the class.\n
            Shows frame by frame of the Matrices which are layer by layer.\n
        returns: outStr, the out come of the work (string).
        """
        outStr = ""

        for frame in range(self.viewable):
            outStr += self.animation[frame].toString()
            if frame < self.viewable - 1:
                outStr += ''.join(['-' for i  in range(4 * (self.animation[frame].getxlen()-1) + 1)])
                outStr += "\n"
        
        return outStr

    def __str__(self):
        """
        Overwrite the default string for the class, by showing good information.
        """
        return self.toString()