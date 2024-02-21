"""
Author: John Burns\n
Last Modified: 5/15/2021\n
OSU Email Address: burnsjo@oregonstate.edu\n
Course Number ECE 342\n
Project: LED Visualizer Group 2\n
Due Date: 5/28/2021\n
Description: The colors used in the visualizer project. Makes it easy to use in multiple programs.
"""

"""
Colors that are used for naming the tabs.
"""
Colors = {'Off': 0, 'Dim Blue': 1, 'Dim Green': 2, 'Dim Cyan': 3, \
            'Dim Red': 4, 'Dim Purple': 5, 'Dim Yellow': 6, 'Dim White': 7, \
            'Blue': 9, 'Blue-Cyan': 11, 'Blue-Purple': 13, 'Baby Blue': 15, \
            'Green': 18, 'Green-Cyan': 19, 'Green-Yellow': 22, 'Green-White': 23, \
            'Cyan': 27, 'Cyan-White': 31, 'Red': 36, 'Red-Purple': 37, \
            'Orange': 38, 'Pink': 39, 'Purple': 45, 'Purple-White': 47, \
            'Yellow': 54, 'Yellow-White': 55, 'White': 63}

"""
Corresponding hex values for the above colors. Retrieved from analysis done on possible colors.
"""
HexColors = {'000000': 0, '00007f': 1, '007f00': 2, '007f7f': 3, \
             '7f0000': 4, '7f007f': 5, '7f7f00': 6, '7f7f7f': 7, \
             '0000ff': 9, '007fff': 11, '7f00ff': 13, '7f7fff': 15, \
             '00ff00': 18, '00ff7f': 19, '7fff00': 22, '7fff7f': 23, \
             '00ffff': 27, '7fffff': 31, 'ff0000': 36, 'ff007f': 37, \
             'ff7f00': 38, 'ff7f7f': 39, 'ff00ff': 45, 'ff7fff': 47, \
             'ffff00': 54, 'ffff7f': 55, 'ffffff': 63}

def getHex(val: int):
    """
    A method for getting the key based on the value of a dictionary.\n
    params: val, the value to search with.\n
    returns: key, the value being looked for.
    """
    hxVals = list(HexColors.keys())
    numVals = list(HexColors.values())
    indexOfVal = numVals.index(val)
    return hxVals[indexOfVal]