#!/usr/bin/python
import shlex
import subprocess
from subprocess import Popen, PIPE
import pytest
import time
import pty
import sys
import select
import os
import re
import pytest
import time
import json
import sys
import traceback
import requests
from ppadb.client import Client as AdbClient
import random
import string
import logging
client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037
devices = client.devices()
if len(devices) == 0:
    print('No devices')
    quit()

device = devices[0]

G_profile={
    "fn":"adam",
    "ln":"lokn",
    "b_day":11,
    "b_month":1,
    "b_year":1995,
    "sex":2

}

MobileHwawei_disp0={
    "Name":"HUAWEI SCL-L21",
    "ADB_ID":"3MSDU15C08006757",
    "rotation":0,
    "cleaner":[521,1258,0,360,1110,360,400],
    "action_touch":[665,1130],
    "Chrome_link":[300,105],
    "Focus_link":[300,107],
    "Chrome_fn":[331,517],
    "Focus_fn":[331,517],
    "Chrome_ca":[163,964],# click create account
    "Focus_ca":[163,964],# click create account
    "Chrome_cm":[120,765],# click me only
    "Focus_cm":[120,765],# click me only
    "Chrome_em":[346,536],
    "Focus_em":[346,536],
    "Chrome_last":[560,850],
    "Focus_last":[560,850],
    "swipe_pgend":[300,700,300,300],
    "accept":[561,877],
    "Speed":1,

}

MobileHwawei_disp1={
    "Name":"HUAWEI SCL-L21",
    "ADB_ID":"3MSDU15C08006757",
    "rotation":1,
    "cleaner":[521,1258,0,360,1110,360,400],
    "action_touch":[1101,678],
    "Chrome_link":[300,111],
    "Focus_link":[300,107],
    "Chrome_fn":[530,564],
    "Focus_fn":[530,564],
    "Chrome_ca":[186,447],# click create account
    "Focus_ca":[186,447],# click create account
    "Chrome_cm":[210,349],# click me only
    "Focus_cm":[210,349],# click me only
    "Chrome_em":[346,536],
    "Focus_em":[346,536],
    "Chrome_last":[560,850],
    "Focus_last":[560,850],
    "swipe_pgend":[235,560,241,231],
    "accept":[561,877],
    "Speed":1,

}

Mobile=MobileHwawei_disp0

def fixrotation(Mobile=Mobile):
    device.shell(f"content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0")
    if(Mobile["rotation"]==0):
        device.shell(f"content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:0")
    else:        
        device.shell(f"content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:1")

def reset_rotation():
    device.shell(f"content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:0")
    device.shell(f"content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0")


def rsleep(time_s,pec=50):
    x=(random.randrange(100)-49)*time_s/pec
    time.sleep(time_s+x)

def swipe_pgend(Mobile=Mobile):
    x1=Mobile["swipe_pgend"][0]
    y1=Mobile["swipe_pgend"][1]
    x2=Mobile["swipe_pgend"][2]
    y2=Mobile["swipe_pgend"][3]
    #for i in range(7):
    #    device.shell(f"input swipe {x1} {y1} {int(x2/2)} {int(y2/2)} &&  swipe {int(x2/2)} {int(y2/2)} {x2/2} {y2/2}")
    device.shell(f"input roll 15 15")


def mob_clean(Mobile=Mobile):
    x=Mobile["cleaner"][0]
    y=Mobile["cleaner"][1]
    x1=Mobile["cleaner"][3]
    y1=Mobile["cleaner"][4]
    x2=Mobile["cleaner"][5]
    y2=Mobile["cleaner"][6]
    if(Mobile["cleaner"][2]==0):
        #device.shell(f"input tap {x} {y}")
        device.shell(f"input keyevent KEYCODE_HOME")
        rsleep(1)
        device.shell(f"input keyevent KEYCODE_APP_SWITCH")
        rsleep(4)
        device.shell(f"input swipe {x1} {y1} {x2} {y2}")
        rsleep(0.2)
    if(Mobile["cleaner"][2]==1):
        #device.shell(f"input tap {x} {y}")
        device.shell(f"input keyevent KEYCODE_HOME")
        rsleep(1)
        device.shell(f"input keyevent KEYCODE_APP_SWITCH")
        rsleep(4)
        device.shell(f"input swipe {x1} {y1} {x2} {y2}")
        rsleep(1)
        device.shell(f"input swipe {x1} {y1} {x2} {y2}")
        rsleep(0.2)

def write_string(s):
    for c in s:
        rsleep(0.3,50)
        if c.isupper():
            device.shell('input text '+c)
        else:
            device.shell('input keyevent KEYCODE_'+c.upper())

def rtouch(x,y,rx=7,ry=10):
    x=x+random.randrange(rx)-int(rx/2)
    y=y+random.randrange(ry)-int(ry/2)
    device.shell(f"input tap {x} {y}")

def nav_open(browser_type=0,Mobile=Mobile):
    x=Mobile["Chrome_link"][0]
    y=Mobile["Chrome_link"][1]
    device.shell("am force-stop com.hsv.privatebrowser")
    device.shell("am force-stop com.android.chrome")
    device.shell("am force-stop org.mozilla.focus")
    if browser_type==0:
        device.shell("am force-stop com.android.chrome")
        device.shell("am start -n com.android.chrome/org.chromium.chrome.browser.incognito.IncognitoTabLauncher")
        rsleep(4)
        device.shell(f"input tap {x} {y}")
        rsleep(2)
        device.shell("input text 'console.cloud.google.com'")
        rsleep(0.3)
        device.shell('input keyevent "KEYCODE_ENTER" ')
        rsleep(2)
    elif browser_type==1:
        device.shell("am force-stop com.hsv.privatebrowser")
        device.shell("am start -n com.hsv.privatebrowser/com.google.android.apps.chrome.Main -d console.cloud.google.com")
    elif browser_type==2:
        device.shell("am start -n org.mozilla.focus/org.mozilla.focus.activity.MainActivity ")
        rsleep(2)
        device.shell(f"input tap {x} {y}")
        rsleep(2)
        device.shell("input text 'console.cloud.google.com'")
        rsleep(0.3)
        device.shell('input keyevent "KEYCODE_ENTER" ')
    rsleep(7)    


def click_create_acc(Mobile=Mobile):
    ca_x=Mobile["Chrome_ca"][0]
    ca_y=Mobile["Chrome_ca"][1]
    cm_x=Mobile["Chrome_cm"][0]
    cm_y=Mobile["Chrome_cm"][1]
    if(Mobile["rotation"]!=0):
        swipe_pgend(Mobile)
    rtouch(ca_x,ca_y) # click create account
    rsleep(2)
    rtouch(cm_x,cm_y) # click me only
    rsleep(5)



def action_touch(Mobile=Mobile):
    x=Mobile["action_touch"][0]
    y=Mobile["action_touch"][1]
    rtouch(x,y)

def first_step(fn='amine',ln='zazil',incerment=10001 ,Mobile=Mobile):
    fn_x=Mobile["Chrome_fn"][0]
    fn_y=Mobile["Chrome_fn"][1]
    gid=f"{fn}{ln}{incerment}"
    rtouch(fn_x,fn_y) #first name
    rsleep(0.7)
    #rtouch(fn_x,fn_y)
    write_string(fn) #first name
    rsleep(0.1)
    action_touch(Mobile) #next to ln
    rsleep(0.1)
    write_string(ln) #last name
    rsleep(0.1)
    action_touch(Mobile) #next to email
    device.shell('input keyevent "KEYCODE_TAB" ') #or  333 566
    rsleep(0.1)
    device.shell('input keyevent "KEYCODE_ENTER" ') #or 333 566
    rsleep(0.3)
    write_string(gid)
    rsleep(0.2)
    action_touch(Mobile) #next to pass
    rsleep(0.1)
    write_string('Ms123456789') #last name
    rsleep(0.2)
    action_touch(Mobile) #next to confirm pass
    rsleep(0.1)
    write_string('Ms123456789') #last name
    rsleep(0.2)
    action_touch(Mobile) #next to step
    rsleep(7)


def se_step(sex=2,day=7,month=1,year=1995,Mobile=Mobile):
    x_em=Mobile["Chrome_em"][0]
    y_em=Mobile["Chrome_em"][1]
    rsleep(0.1)
    rtouch(x_em,y_em)
    rsleep(0.1)
    device.shell('input keyevent "KEYCODE_TAB" ')
    rsleep(0.1)
    device.shell('input keyevent "KEYCODE_TAB" ')
    rsleep(0.1)
    write_string(str(day)) #day of birth 
    rsleep(0.1)
    device.shell('input keyevent "KEYCODE_TAB" ')
    rsleep(0.1)
    for i in range(month):
        device.shell('input keyevent "KEYCODE_DPAD_DOWN" ')
        rsleep(0.1)
    device.shell('input keyevent "KEYCODE_TAB" ')
    rsleep(0.1)
    write_string(str(year)) #last name
    rsleep(0.1)
    device.shell('input keyevent "KEYCODE_TAB" ')
    for i in range(sex):
        device.shell('input keyevent "KEYCODE_DPAD_DOWN" ')
        rsleep(0.1)    
    device.shell('input keyevent "KEYCODE_TAB" ')
    rsleep(0.1)
    device.shell('input keyevent "KEYCODE_TAB" ')
    rsleep(0.1)
    device.shell('input keyevent "KEYCODE_ENTER" ')
    rsleep(7)

def tird_step(Mobile=Mobile):
    #for i in range(8):
    #    device.shell('input keyevent "KEYCODE_TAB" ')
    #    rsleep(0.1)
    #device.shell('input keyevent "KEYCODE_ENTER" ')
    for i in range(4):
        device.shell('input roll 15 15')
    rsleep(0.5)
    rtouch(Mobile['accept'][0],Mobile['accept'][1])

def newip():
    print(device.shell('curl https://api.myip.com --insecure -4'))
    os.system("ssh root@10.10.0.3 ifup DSL2")
    rsleep(5)
    print(device.shell('curl https://api.myip.com --insecure -4'))

if __name__ == '__main__':
    #device = client.device("3MSDU15C08006757")
    strpp=f'Connected to :{device}'
    print(strpp)
    #newip()
    mob_clean(Mobile)
    fixrotation(Mobile)
    nav_open(0) 
    rsleep(5)
    click_create_acc(Mobile)
    rsleep(5)
    first_step(fn='marwan',ln='malok',incerment=10008 ,Mobile=Mobile)

    ########### non critical step
    reset_rotation()
    rsleep(5)
    se_step(sex=2,day=7,month=1,year=1995,Mobile=Mobile)
    rsleep(5)
    tird_step()
    rsleep(5)