import pigpio
import time
import pickle

#Extended NEC (https://www.sbprojects.net/knowledge/ir/nec.php)

MOD = 13
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
pi.set_mode(MOD, pigpio.OUTPUT)
pi.wave_clear()
wf = []

UPERIOD = 1000//38 # period in us
ONPERIOD = UPERIOD//2
OFFPERIOD = UPERIOD-ONPERIOD


#command numbers

#COMMAND_NUMBER = 0-9 # numbers
#COMMAND_NUMBER = 10 # CH+
#COMMAND_NUMBER = 11 # CH-
#COMMAND_NUMBER = 12 # VOL+
#COMMAND_NUMBER = 13 # VOL-
#COMMAND_NUMBER = 14 # MUTE
#COMMAND_NUMBER = 15 # POWER
#COMMAND_NUMBER = 16 # Last Channel
#COMMAND_NUMBER = 17 #nothing?
#COMMAND_NUMBER = 18 #TV / AV
#COMMAND_NUMBER = 19 #SLEEP CYCLE
#COMMAND_NUMBER = 20 #MENU
#COMMAND_NUMBER = 21 #MENU_NAV_UP
#COMMAND_NUMBER = 22 #MENU_NAV_DOWN

#from NEC specs
BASEU = 560

#from analysis 
ADDRESS = 0x8605 # (lsb first)
address_bytes = [(ADDRESS&0xff00) >> 8,ADDRESS&0xff]

def burst(wvfrm,on,off):
    global UPERIOD
    print(hex(on//UPERIOD),hex(off//UPERIOD))
    reps = on//UPERIOD
    for i in range(reps):
        wvfrm.append(pigpio.pulse(1<<MOD,0,ONPERIOD))
        wvfrm.append(pigpio.pulse(0,1<<MOD,OFFPERIOD))
    wvfrm.append(pigpio.pulse(0,1<<MOD,off))

def add_one(wvfrm):
    global BASEU
    burst(wvfrm,BASEU,3*BASEU)

def add_zero(wvfrm):
    global BASEU
    burst(wvfrm,BASEU,BASEU)

def add_byte(wvfrm,b):
    for i in range(8):
        if b & 1:
            add_one(wvfrm)
        else:
            add_zero(wvfrm)
        b >>= 1


def add_command(wvfrm,cmd):
    #start pulse
    burst(wvfrm,9000,4500)
    # address LSB
    add_byte(wvfrm,address_bytes[0])
    #address MSB
    add_byte(wvfrm,address_bytes[1])
    # command
    add_byte(wvfrm,cmd)
    add_byte(wvfrm,~cmd)
    #end pulse
    add_zero(wvfrm)

add_command(wf,COMMAND_NUMBER)
pi.wave_add_generic(wf)
wave_id = pi.wave_create()
pi.wave_send_once(wave_id)