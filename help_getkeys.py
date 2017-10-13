#help_getkeys

import win32api as wapi
import time

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)

def key_check():
    keys = []

    #If you want to add more characters -> https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx
    #Special Character and Mouse Event
    #Left Mouse
    left = wapi.GetAsyncKeyState(0x01)
    if left < 0:
        keys.append("LM")
        print('LM')

    #Right Mouse
    right = wapi.GetAsyncKeyState(0x02)
    if right < 0:
        keys.append("RM")
        print('RM')

    #Shift Mouse
    shift = wapi.GetAsyncKeyState(0x10)
    if shift < 0:
        keys.append("SH")
        print('SH')

    #Ctrl Mouse
    ctrl = wapi.GetAsyncKeyState(0x11)
    if ctrl < 0:
        keys.append("CT")
        print('CT')
###########################################################

    #Keyboard Event
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            print('Key is {}'.format(key))
            keys.append(key)
    return keys
 
