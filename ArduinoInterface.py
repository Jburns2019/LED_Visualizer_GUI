"""
File:       ArduinoInterface.py\n
Author:     Henry Gillespie\n
Date:       May 25, 2021\n
Purpose:    This program defines functions that communicate with the Arduino
"""

import os
from Animation import Animation
from tkinter import messagebox
import pythonCOMport as com

def sendValToArd(val:int, port:str):
    """This function sends the input value to Serial Port COM3"""
    portNum = com.getPort(port, False)
    if len(portNum) > 0:
        print(f'Animation {val+1} was sent.')
        setMode = f'mode {portNum} BAUD=9600 PARITY=n DATA=8'
        os.system(r"{}".format(setMode))
        # os.system(r'mode COM3 BAUD=9600 PARITY=n DATA=8')

        # The following lines make a raw string with a variable in it. 'string' is parsed as an f-string with special characters and a variable
        # Then it is converted to a raw string with the variable in place

        string = f'set /p x="{val}" <nul >\\\\.\{portNum}' # in f-strings, '\' is a special character, so '\\' becomes '\'
        os.system(r"{}".format(string)) # raw strings ignore otherwise special characters

        #Show a window that tells them what they can expect.
        messagebox.showinfo("Animation Sent", f"Animation #{val+1} was selected.\nEnjoy.")
    else:
        print(f'Animation {val+1} could not be sent.')

def animationsForHeader(animations: list[Animation], port:str):
    """This function writes a header file and then uploads the arduino code, which calls the header file"""
    
    portNum = com.getPort(port, False)
    if len(portNum) > 0:
        for i in range(len(animations)):
            animation = animations[i]
            frameCnt = animation.getNumFrames()
            speed = animation.getSpeed()

            print(f'Animation {i+1} has {frameCnt} frame{"s" if frameCnt > 1 else ""} and will be played at {speed} frame{"s" if speed > 1 else ""} per second.\n')

            print('Animation sent:')
            print(animation)

            if i < len(animations) - 1:
                print(":---------------:\n")
    
        writeFile(animations)

        uploadStr = f'arduino --upload --port {portNum} JuniorDesign_PreProgrammedAnimations\JuniorDesign_PreProgrammedAnimations.ino'
        # os.system(r'arduino --upload JuniorDesign_PreProgrammedAnimations\JuniorDesign_PreProgrammedAnimations.ino')
        os.system(r"{}".format(uploadStr))

        messagebox.showinfo("Animations uploaded", "Animations 4, 5, and 6 have been uploaded.\nTo play, go to the main menu and select an animation.")
    else:
        print('Animations could not be updated.')

def writeFile(animations: list[Animation]):
    """The function writes an animation to file."""
    headerFile = open("JuniorDesign_PreProgrammedAnimations\headerFile.h", 'w')
    headerFile.write("#ifndef headerFile\n#define headerFile\n\n")
    # in f-strings, '{' is a special character to open variables, so '{{' will become '{' in the header file
    headerFile.write(f"const PROGMEM uint16_t customLengths[3] = {{{animations[0].getNumFrames()}, {animations[1].getNumFrames()}, {animations[2].getNumFrames()}}};\n")
    headerFile.write(f"const PROGMEM unsigned long customSpeeds[3] = {{{framesToMicros(animations[0].getSpeed())}, {framesToMicros(animations[1].getSpeed())}, {framesToMicros(animations[2].getSpeed())}}};\n\n")
    headerFile.write("const PROGMEM uint16_t colorArr[3][2][30][35] = {")
    

    for i in range(len(animations)): # for each animation
            headerFile.write("\n{") # open animation array
            for color in range(2): # for each of the two color values to be passed
                headerFile.write("{") # open color array
                for frame in range(30): # for each frame
                    headerFile.write("{") # open frame array
                    for LED_row in range(35):
                        if frame < animations[i].getNumFrames(): # if this frame exists
                            headerFile.write(str(int(animations[i].getFrame(frame).getRowValue(LED_row,color))))
                        else:
                            headerFile.write("0") # if frame > number of frames, fill it with 0
                        if LED_row != 34:
                            headerFile.write(', ') # do not use a ',' after the last value in the array
                    # close frame arrays
                    if frame != 29:
                        headerFile.write('}, ')
                    else:
                        headerFile.write('}')
                # close color arrays
                if color != 1:
                    headerFile.write('},\n ')
                else:
                    headerFile.write('}')
            # close animation arrays
            if i != len(animations)-1:
                headerFile.write('}, ')
            else:
                headerFile.write('}')

    headerFile.write("};\n\n#endif") # close complete array
    headerFile.close()

def framesToMicros(fps: int):
    """This function converts a frames per second value to microseconds per frame"""
    return round(1000000 / fps)