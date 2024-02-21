"""
Author: John Burns\n
Last Modified: 5/15/2021\n
OSU Email Address: burnsjo@oregonstate.edu\n
Course Number ECE 342\n
Project: LED Visualizer Group 2\n
Due Date: 5/28/2021
"""

class LEDMatrix:
    """
    The definition for how a LED matrix can be defined.\n
        Primarily as a x, y, z list of colors. This particular implementation also has a limit on
        how high the value can be set.
    There are two modes to call this class's constructor.\n
        The default LEDMatrix() with default size of 5x5x7 with a limit on the value of 63.
        The full parameter list can also be entered thanks to *args.
        LEDMatrix(x (int), y (int), z (int), lim (int)) can be called to make a custom matrix.\n
    parameters: *args, either 4 parameters long or 0 parameters long. Otherwise nothing is set.
    """
    def __init__(self, *args):
        #full parameter list
        if len(args) == 4:
            #Parse expected parameters.
            x, y, z, lim = args
            #Make a matrix of the requested side.
            self.matrix = [[[0 for k in range(z)] for j in range(y)] for i in range(x)]
            #set values.
            self.x = x
            self.y = y
            self.z = z
            self.lim = lim
        #Default parameter list.
        elif len(args) == 0:
            #Make a matrix of the default 5x5x7 size.
            self.matrix = [[[0 for k in range(7)] for j in range(5)] for i in range(5)]
            #Set the values to the default values.
            self.x = 5
            self.y = 5
            self.z = 7
            self.lim = 63
    
    def getxlen(self):
        """method for getting the x value."""
        return self.x
    
    def getylen(self):
        """method for getting the y value."""
        return self.y

    def getzlen(self):
        """method for getting the z value."""
        return self.z
    
    def getlim(self):
        """method for getting the lim value."""
        return self.lim

    def getMatrix(self):
        """method for getting the matrix."""
        return self.matrix

    def setVal(self, x: int, y: int, z: int, val: int):
        """
        Sets a value in the matrix.\n
        Note: implementing the color of a bulb is implented in getRowValue.\n
        parameters: x, the x value on the layer (int).\n
                    y, the y value on the layer (int).
                    z, the layer (int).
                    val, the value of the corresponding bulb (int).\n
        returns: wasProb, whether the value was valid (boolean).
        """
        #Allow for problem detection.
        wasProb = False

        #Try to prevent users from entering bogus values.
        if val <= self.lim and val >= 0:
            self.matrix[x][y][z] = val
        else:
            wasProb = True
        
        return wasProb
    
    def getVal(self, x: int, y: int, z: int):
        """
        Retrieve te value from the matrix.\n
        paramaters: x, the x value on the layer (int).\n
                    y, the y value on the layer (int).
                    z, the layer (int).\n
        returns: value, the value stored in the matrix at that location.
        """
        return self.matrix[x][y][z]

    def clearVal(self, x: int, y: int, z: int):
        """
        Provide a way to clear the value. Same as setting the value to 0.\n
        paramaters: x, the x value on the layer (int).\n
                    y, the y value on the layer (int).
                    z, the layer (int).
        """
        self.matrix[x][y][z] = 0
    
    def clearMatrix(self):
        """
        Provide a way to clear the entire matrix. Rebuilds the matrix by setting every value to 0.
        """
        self.matrix = [[[0 for k in range(self.z)] for j in range(self.y)] for i in range(self.x)]
    
    def toString(self):
        """
        Provide a way to get an intelligent string of the matrix.\n
            Matrices are printed as layers from bottom to top.\n
        returns: outStr, the string to be used (string).
        """
        outStr = ""
        for z in range(self.z):
            for y in range(self.y):
                for x in range (self.x):
                    outStr += str(self.matrix[x][y][z])
                    #Don't put strings at the end of printout.
                    if x < self.x - 1:
                        outStr += "   "
                #Put a new line at the end of every row.
                outStr += "\n"
            #Put a new line at the end of every layer except the last one.
            if z < self.z - 1:
                outStr += "\n"
        return outStr

    def __str__(self):
        """Overwriting the default address print statement."""
        return self.toString()

    #Written by Henry Gillespie for getting his binary numbers.
    def getRowValue(self, row: int, color: int):
        """This function calculates the values that will fill the header file. This creates the correct value (in binary) to push to the LEDs\n
        Each value is multiplied by a factor of 2^(3i) to set it to a different value. The color variable allows the writeFile function to\n
        get switch between / and % from the values that are in the Colors dictionary in the main visualizer.py file."""
        layer = int(row / self.y)
        horizontalRow = row % self.y
        value = 0
        
        for i in range(self.x):
            if color == 0:
                value += int(self.matrix[horizontalRow][i][layer] / 8) * 2**(3*i)
            else:
                value += (self.matrix[horizontalRow][i][layer] % 8) * 2**(3*i)
        return value