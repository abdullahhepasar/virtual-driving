import numpy as np
from help_grabscreen import grab_screen
import cv2
import time
from help_directkeys import PressKey,ReleaseKey, W, A, S, D, H, T, C
from help_models import inception_v3 as googlenet
from help_getkeys import key_check
from collections import deque, Counter
import random
from statistics import mode,mean
import numpy as np
import win32api as wapi
import win32con
#from motion import motion_detection

GAME_WIDTH = 80
GAME_HEIGHT = 60

how_far_remove = 800
rs = (20,15)
log_len = 25

motion_req = 800
motion_log = deque(maxlen=log_len)

WIDTH = 480
HEIGHT = 270
LR = 1e-3
EPOCHS = 30

choices = deque([], maxlen=5)
hl_hist = 250
choice_hist = deque([], maxlen=hl_hist)

#For the month 57 + 1 (null) = 58 variable keyboard combination
#single Combinations
w  = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
s  = [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
a  = [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
d  = [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lm = [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
rm = [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sh = [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ct = [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#Double Combinations
wa   = [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wd   = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wlm  = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wsh  = [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wct  = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
As   = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ad   = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
alm  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ash  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
act  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sd   = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
slm  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ssh  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sct  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
dlm  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
dsh  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
dct  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lmsh = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lmct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#Triple Combinations
walm  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wash  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wact  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wdlm  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wdsh  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wdct  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wlmrm = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wlmsh = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wlmct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
aslm  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
assh  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
asct  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
almrm = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
almsh = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
almct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sdlm  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sdsh  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sdct  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
slmsh = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
slmct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]
dlmsh = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
dlmct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0]

#Quadruple Combinations
walmsh = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
walmct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
wdlmsh = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]
wdlmct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
aslmsh = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
aslmct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
sdlmct = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
sdlmsh = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]

#Invalid Data Record Variation (for Null)
empty = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]


t_time = 0.25


def LeftMouse(isPress):
    if isPress == True:
        x,y = wapi.GetCursorPos()
        wapi.SetCursorPos((x, y))
        #Left click
        wapi.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0) 
        time.sleep(0.05) 
        wapi.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0) 

def RightMouse(isPress):
    if isPress == True:
        x,y = wapi.GetCursorPos()
        wapi.SetCursorPos((x, y))
        #Right click
        wapi.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0) 
        time.sleep(0.05) 
        wapi.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)


#single Combinations

#ileri
def forward():
    PressKey(W)
    
    ReleaseKey(S)
    ReleaseKey(A)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)
#slow
def slow():
    PressKey(S)
    
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

#left
def left():
    if random.randrange(0,4) == 1:
        PressKey(A)
    else:
        ReleaseKey(A)

    PressKey(W)
    PressKey(T)
    
    ReleaseKey(D)
    ReleaseKey(S)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)

#right
def right():
    if random.randrange(0,4) == 1:
        PressKey(D)
    else:
        ReleaseKey(D)

    PressKey(W)
    PressKey(T)
    
    ReleaseKey(A)
    ReleaseKey(S)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)

#Fire
def LM():
    LeftMouse(True)
    
    ReleaseKey(W)    
    ReleaseKey(S)
    ReleaseKey(A)
    ReleaseKey(D)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

#don't Right Mouse

def SH():
    PressKey(H)
    
    ReleaseKey(W)    
    ReleaseKey(S)
    ReleaseKey(A)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(T)

def CT():
    PressKey(T)
    
    ReleaseKey(W)    
    ReleaseKey(S)
    ReleaseKey(A)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)

######################################

#Double Combinations

def WA():
    PressKey(W)
    PressKey(A)
      
    ReleaseKey(S)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

def WD():
    PressKey(W)
    PressKey(D)
      
    ReleaseKey(S)
    ReleaseKey(A)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

def WLM():
    PressKey(W)
    LeftMouse(True)
    
    ReleaseKey(A)      
    ReleaseKey(S)
    ReleaseKey(D)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

def WSH():
    PressKey(W)
    PressKey(H)
      
    ReleaseKey(S)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(A)
    ReleaseKey(T)

def WCT():
    PressKey(W)
    PressKey(T)
      
    ReleaseKey(S)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(A)

def AS():
    PressKey(A)
    PressKey(S)
      
    ReleaseKey(W)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

#error Combinations
def AD():
    PressKey(A)
    PressKey(D)
      
    ReleaseKey(W)
    ReleaseKey(S)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

def ALM():
    PressKey(A)
    LeftMouse(True)
    
    ReleaseKey(W)
    ReleaseKey(S)
    ReleaseKey(D)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

def ASH():
    PressKey(A)
    PressKey(H)
    
    ReleaseKey(W)
    ReleaseKey(S)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(T)

def ACT():
    PressKey(A)
    PressKey(T)
    
    ReleaseKey(W)
    ReleaseKey(S)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)

def SD():
    PressKey(S)
    PressKey(D)
      
    ReleaseKey(A)
    ReleaseKey(W)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

def SLM():
    PressKey(S)
    LeftMouse(True)
    
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

def SSH():
    PressKey(S)
    PressKey(H)
    
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(T)

def SCT():
    PressKey(S)
    PressKey(T)
    
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)

def DLM():
    PressKey(D)
    LeftMouse(True)
    
    ReleaseKey(W)
    ReleaseKey(S)
    ReleaseKey(A)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)

def DSH():
    PressKey(D)
    PressKey(H)
    
    ReleaseKey(W)
    ReleaseKey(S)
    ReleaseKey(A)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(T)

def DCT():
    PressKey(D)
    PressKey(T)
    
    ReleaseKey(W)
    ReleaseKey(S)
    ReleaseKey(A)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)

def LMSH():
    LeftMouse(True)
    PressKey(H)
    
    ReleaseKey(W)
    ReleaseKey(S)
    ReleaseKey(A)
    RightMouse(False)
    ReleaseKey(D)
    ReleaseKey(T)

def LMCT():
    LeftMouse(True)
    PressKey(T)
    
    ReleaseKey(W)
    ReleaseKey(S)
    ReleaseKey(A)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(D)


######################################

#Triple Combinations

def WALM():
    PressKey(W)
    PressKey(A)
    LeftMouse(True)
    
    ReleaseKey(H)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(D)

#asagi_sol
def WASH():
    if random.randrange(0,2) == 1:
        PressKey(A)
    else:
        ReleaseKey(A)

    PressKey(W)
    PressKey(H)
    
    ReleaseKey(D)
    ReleaseKey(S)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(T)

#yukarı_sol
def WACT():
    if random.randrange(0,2) == 1:
        PressKey(A)
    else:
        ReleaseKey(A)

    PressKey(W)
    PressKey(T)
    
    ReleaseKey(D)
    ReleaseKey(S)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)

def WDLM():
    PressKey(W)
    PressKey(D)
    LeftMouse(True)
    
    ReleaseKey(H)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(D)

#asagi_sag
def WDSH():
    if random.randrange(0,2) == 1:
        PressKey(D)
    else:
        ReleaseKey(D)

    PressKey(W)
    PressKey(H)
    
    ReleaseKey(A)
    ReleaseKey(S)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(T)

#yukarı_sag
def WDCT():
    if random.randrange(0,2) == 1:
        PressKey(D)
    else:
        ReleaseKey(D)

    PressKey(W)
    PressKey(T)
    
    ReleaseKey(A)
    ReleaseKey(S)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)

def WLMRM():
    PressKey(W)
    LeftMouse(True)
    RightMouse(True)
    
    ReleaseKey(A)    
    ReleaseKey(H)
    ReleaseKey(S)
    ReleaseKey(T)
    ReleaseKey(D)

def WLMSH():
    PressKey(W)
    LeftMouse(True)
    PressKey(H)
    
    ReleaseKey(A)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(D)

def WLMCT():
    PressKey(W)
    LeftMouse(True)
    PressKey(T)
    
    ReleaseKey(H)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(A)
    ReleaseKey(D)

def ASLM():
    PressKey(A)
    PressKey(S)
    LeftMouse(True)
    
    ReleaseKey(H)
    ReleaseKey(W)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(D)

def ASSH():
    PressKey(A)
    PressKey(S)
    PressKey(H)
    
    LeftMouse(False)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(D)

def ASCT():
    PressKey(A)
    PressKey(S)
    PressKey(T)
    
    LeftMouse(False)
    ReleaseKey(H)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(D)

def ALMRM():
    PressKey(A)
    LeftMouse(True)
    RightMouse(True)
    
    ReleaseKey(H)
    ReleaseKey(S)
    ReleaseKey(W)
    ReleaseKey(T)
    ReleaseKey(D)

def ALMSH():
    PressKey(A)
    PressKey(H)
    LeftMouse(True)
    
    ReleaseKey(W)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(D)

def ALMCT():
    PressKey(A)
    PressKey(T)
    LeftMouse(True)
    
    ReleaseKey(H)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(W)
    ReleaseKey(D)

def SDLM():
    PressKey(S)
    PressKey(D)
    LeftMouse(True)
    
    ReleaseKey(H)
    ReleaseKey(W)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(A)

def SDSH():
    PressKey(S)
    PressKey(D)
    PressKey(H)
    
    LeftMouse(False)
    ReleaseKey(W)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(A)

def SDCT():
    PressKey(S)
    PressKey(D)
    PressKey(T)
    
    LeftMouse(False)
    ReleaseKey(W)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(A)

def SLMSH():
    PressKey(S)
    LeftMouse(True)
    PressKey(H)
    
    ReleaseKey(A)
    ReleaseKey(W)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(D)

def SLMCT():
    PressKey(S)
    LeftMouse(True)    
    PressKey(T)
    
    ReleaseKey(A)
    ReleaseKey(W)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(D)

def DLMSH():
    PressKey(D)
    LeftMouse(True)
    PressKey(H)
    
    ReleaseKey(W)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(A)

def DLMCT():
    PressKey(D)
    LeftMouse(True)
    PressKey(T)
    
    ReleaseKey(A)
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(W)


######################################

#Quadruple Combinations

def WALMSH():
    PressKey(W)
    PressKey(A)
    LeftMouse(True)
    PressKey(H)
    
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(D)

def WALMCT():
    PressKey(W)
    PressKey(A)
    LeftMouse(True)
    PressKey(T)
    
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(D)

def WDLMSH():
    PressKey(W)
    PressKey(D)
    LeftMouse(True)
    PressKey(H)
    
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(A)

def WDLMCT():
    PressKey(W)
    PressKey(D)
    LeftMouse(True)
    PressKey(T)
    
    ReleaseKey(S)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(A)

def ASLMSH():
    PressKey(A)
    PressKey(S)
    LeftMouse(True)
    PressKey(H)
    
    ReleaseKey(W)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(D)

def ASLMCT():
    PressKey(A)
    PressKey(S)
    LeftMouse(True)
    PressKey(T)
    
    ReleaseKey(W)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(D)

def SDLMCT():
    PressKey(S)
    PressKey(D)
    LeftMouse(True)
    PressKey(T)
    
    ReleaseKey(A)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(W)

def SDLMSH():
    PressKey(S)
    PressKey(D)
    LeftMouse(True)
    PressKey(H)
    
    ReleaseKey(W)
    RightMouse(False)
    ReleaseKey(T)
    ReleaseKey(A)


######################################

def no_keys():
    PressKey(W)
    PressKey(C)
    
    ReleaseKey(S)
    ReleaseKey(A)
    ReleaseKey(D)
    LeftMouse(False)
    RightMouse(False)
    ReleaseKey(H)
    ReleaseKey(T)
    


model = googlenet(WIDTH, HEIGHT, 3, LR, output=58)
MODEL_NAME = 'warplane-{}-{}-{}-epochs.model'.format(LR, 'alexnetv2',EPOCHS)
model.load(MODEL_NAME)

print('We have loaded a previous model!')

def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    mode_choice = 0

    screen = grab_screen(region=(0,100,GAME_WIDTH,GAME_HEIGHT+40))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    prev = cv2.resize(screen, (WIDTH,HEIGHT))

    t_minus = prev
    t_now = prev
    t_plus = prev

    while(True):
        
        if not paused:
            screen = grab_screen(region=(0,100,GAME_WIDTH,GAME_HEIGHT+40))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            last_time = time.time()
            screen = cv2.resize(screen, (WIDTH,HEIGHT))

            #delta_count_last = motion_detection(t_minus, t_now, t_plus)

            t_minus = t_now
            t_now = t_plus
            t_plus = screen
            t_plus = cv2.blur(t_plus,(4,4))

            prediction = model.predict([screen.reshape(WIDTH,HEIGHT,3)])[0]
            prediction = np.array(prediction) * np.array([3.0,0.1,0.1,0.1,0.5,0.1,0.5,0.5,0.1,0.1,0.5,0.5,0.5,0.1,0.1,0.1,0.5,0.5,0.1,0.1,0.5,0.5,0.1,0.1,0.1,0.5,0.5,0.1,0.5,0.5,0.1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.1,0.5,0.5,0.1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5])

            mode_choice = np.argmax(prediction)

            if mode_choice == 0:
                forward()
                choice_picked = 'Full Power'             
            elif mode_choice == 1:
                slow()
                choice_picked = 'slow'
            elif mode_choice == 2:
                left()
                choice_picked = 'left'
            elif mode_choice == 3:
                right()
                choice_picked = 'right'
            elif mode_choice == 4:
                LM()
                choice_picked = 'Fire'
            elif mode_choice == 5:
                RM()
                choice_picked = 'RM'
            elif mode_choice == 6:
                SH()
                choice_picked = 'Flap Asagi'
            elif mode_choice == 7:
                CT()
                choice_picked = 'Flap Yukari'
            elif mode_choice == 8:
                WA()
                choice_picked = 'WA'  
            elif mode_choice == 9:
                WD()
                choice_picked = 'WD'
            elif mode_choice == 10:
                WLM()
                choice_picked = 'WLM'
            elif mode_choice == 11:
                WSH()
                choice_picked = 'WSH'
            elif mode_choice == 12:
                WCT()
                choice_picked = 'WCT'
            elif mode_choice == 13:
                AS()
                choice_picked = 'AS'
            elif mode_choice == 14:
                AD()
                choice_picked = 'AD'
            elif mode_choice == 15:
                ALM()
                choice_picked = 'ALM'
            elif mode_choice == 16:
                ASH()
                choice_picked = 'ASH'
            elif mode_choice == 17:
                ACT()
                choice_picked = 'ACT'
            elif mode_choice == 18:
                SD()
                choice_picked = 'SD'
            elif mode_choice == 19:
                SLM()
                choice_picked = 'SLM'
            elif mode_choice == 20:
                SSH()
                choice_picked = 'SSH'
            elif mode_choice == 21:
                SCT()
                choice_picked = 'SCT'
            elif mode_choice == 22:
                DLM()
                choice_picked = 'DLM'  
            elif mode_choice == 23:
                DSH()
                choice_picked = 'DSH'
            elif mode_choice == 24:
                DCT()
                choice_picked = 'DCT'
            elif mode_choice == 25:
                LMSH()
                choice_picked = 'LMSH'
            elif mode_choice == 26:
                LMCT()
                choice_picked = 'LMCT'
            elif mode_choice == 27:
                WALM()
                choice_picked = 'WALM'
            elif mode_choice == 28:
                WASH()
                choice_picked = 'WASH'
            elif mode_choice == 29:
                WACT()
                choice_picked = 'WACT'
            elif mode_choice == 30:
                WDLM()
                choice_picked = 'WDLM'
            elif mode_choice == 31:
                WDSH()
                choice_picked = 'WDSH'
            elif mode_choice == 32:
                WDCT()
                choice_picked = 'WDCT'
            elif mode_choice == 33:
                WLMRM()
                choice_picked = 'WLMRM'
            elif mode_choice == 34:
                WLMSH()
                choice_picked = 'WLMSH'
            elif mode_choice == 35:
                WLMCT()
                choice_picked = 'WLMCT'
            elif mode_choice == 36:
                ASLM()
                choice_picked = 'ASLM'  
            elif mode_choice == 37:
                ASSH()
                choice_picked = 'ASSH'
            elif mode_choice == 38:
                ASCT()
                choice_picked = 'ASCT'
            elif mode_choice == 39:
                ALMRM()
                choice_picked = 'ALMRM'
            elif mode_choice == 40:
                ALMSH()
                choice_picked = 'ALMSH'
            elif mode_choice == 41:
                ALMCT()
                choice_picked = 'ALMCT'
            elif mode_choice == 42:
                SDLM()
                choice_picked = 'SDLM'
            elif mode_choice == 43:
                SDSH()
                choice_picked = 'SDSH'
            elif mode_choice == 44:
                SDCT()
                choice_picked = 'SDCT'
            elif mode_choice == 45:
                SLMSH()
                choice_picked = 'SLMSH'
            elif mode_choice == 46:
                SLMCT()
                choice_picked = 'SLMCT'
            elif mode_choice == 47:
                DLMSH()
                choice_picked = 'DLMSH'
            elif mode_choice == 48:
                DLMCT()
                choice_picked = 'DLMCT'
            elif mode_choice == 49:
                WALMSH()
                choice_picked = 'WALMSH'
            elif mode_choice == 50:
                WALMCT()
                choice_picked = 'WALMCT'  
            elif mode_choice == 51:
                WDLMSH()
                choice_picked = 'WDLMSH'
            elif mode_choice == 52:
                WDLMCT()
                choice_picked = 'WDLMCT'
            elif mode_choice == 53:
                ASLMSH()
                choice_picked = 'ASLMSH'
            elif mode_choice == 54:
                ASLMCT()
                choice_picked = 'ASLMCT'
            elif mode_choice == 55:
                SDLMCT()
                choice_picked = 'SDLMCT'
            elif mode_choice == 56:
                SDLMSH()
                choice_picked = 'SDLMSH'
            elif mode_choice == 57:
                no_keys()
                choice_picked = 'nokeys'

            print('loop took {} seconds. Choice: {}'.format( round(time.time()-last_time, 3) , choice_picked))
    
        keys = key_check()

        # p pauses game
        if 'P' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)

main()       
