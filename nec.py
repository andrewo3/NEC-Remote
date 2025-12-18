import pigpio, sys

GPIO = 13
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
pi.set_mode(GPIO, pigpio.OUTPUT)
#Extended NEC (https://www.sbprojects.net/knowledge/ir/nec.php)

UPERIOD = 1000//38 # period in us
ONPERIOD = UPERIOD//2
OFFPERIOD = UPERIOD-ONPERIOD

#from NEC specs
BASEU = 560

#from analysis 
ADDRESS = 0x8605 # (lsb first)
address_bytes = [(ADDRESS&0xff00) >> 8,ADDRESS&0xff]

def burst(wvfrm,on,off):
    global UPERIOD
    t = 0
    reps = on//UPERIOD
    for i in range(reps):
        wvfrm.append(pigpio.pulse(1<<GPIO,0,ONPERIOD))
        wvfrm.append(pigpio.pulse(0,1<<GPIO,OFFPERIOD))
    t += on + off
    wvfrm.append(pigpio.pulse(0,1<<GPIO,off))
    return t

def add_one(wvfrm):
    global BASEU
    return burst(wvfrm,BASEU,3*BASEU)

def add_zero(wvfrm):
    global BASEU
    return burst(wvfrm,BASEU,BASEU)

def add_byte(wvfrm,b):
    t = 0
    for i in range(8):
        if b & 1:
            t += add_one(wvfrm)
        else:
            t += add_zero(wvfrm)
        b >>= 1
    return t


def add_command(wvfrm,cmd):
    global BASEU
    t = 0
    #start pulse
    t += burst(wvfrm,9000,4500)
    # address LSB
    t += add_byte(wvfrm,address_bytes[0])
    #address MSB
    t += add_byte(wvfrm,address_bytes[1])
    # command
    t += add_byte(wvfrm,cmd)
    t += add_byte(wvfrm,~cmd)
    #end pulse (should go to 110 ms)
    burst(wvfrm,BASEU,110000-t-BASEU)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python nec.py [command_number]")
        quit()
    try:
        COMMAND_NUMBER = int(sys.argv[1])
        if not(0 <= COMMAND_NUMBER <= 25):
            print("Not a valid command number!")
            quit()
    except ValueError as e:
        print("Argument must be a valid integer!")
        quit()
    #command numbers
    
    pi.wave_clear()

    wf = []
    add_command(wf,COMMAND_NUMBER)
    pi.wave_add_generic(wf)

    wave_id = pi.wave_create()
    pi.wave_send_once(wave_id)