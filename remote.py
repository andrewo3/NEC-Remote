import pigpio
import time
import pickle

#Taken from remotecentral.com, in IR Pronto hex format:
#https://www.remotecentral.com/cgi-bin/codes/
with open('codes.pkl','rb') as file:
    codes = pickle.load(file)

buttons = list(codes.keys())

for button in buttons:
    if codes[button][0] != '0000':
        print("Problem with",key,"button. Failed to parse code.")
        del codes[button]

print("Buttons")
print("============")
for button in buttons:
    print(button)
print("============")


MOD = 13
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon")
pi.set_mode(MOD, pigpio.OUTPUT)
pi.wave_clear()

while True:
    press = input("")
    hold_time = input("Hold: ")
    if hold_time == '':
        hold_time = 0
    else:
        try:
            hold_time = float(hold_time)
        except ValueError as e:
            print("Hold time must be a float, or nothing!")
            continue
    if not press in buttons:
        print("Invalid option.")
        continue
    print(hold_time)
    #decoding process from https://www.remotecentral.com/features/irdisp2.htm
    print(codes[press])
    pi.wave_clear()
    wf = []

    pronto_freq = int(codes[press][1],16)
    freq = 1000000/(pronto_freq * 0.241246)
    uperiod = int(1000000/freq)
    onperiod = uperiod//2
    offperiod = uperiod-onperiod
    print(freq,"Hz")
    print(uperiod,"us")

    burst_pairs1 = int(codes[press][2],16)
    print(burst_pairs1)

    burst_pairs2 = int(codes[press][3],16)
    print(burst_pairs2)

    burst_pairs = burst_pairs1 + burst_pairs2
    burst_pair2_start = 2*burst_pairs1 + 4
    for w in range(burst_pairs):
        ind = 2*w+4
        on_time = int(codes[press][ind],16)
        off_time = int(codes[press][ind+1],16)
        for p in range(on_time):
            wf.append(pigpio.pulse(1<<MOD,0,onperiod))
            wf.append(pigpio.pulse(0,1<<MOD,offperiod))
        wf.append(pigpio.pulse(0,1<<MOD,off_time*uperiod))

    pi.wave_add_generic(wf)
    wave_id = pi.wave_create()
    pi.wave_send_once(wave_id)

    if hold_time == 0:
        continue
    #hold down
    pi.wave_clear()
    wf = []
    burst_pairs2_start = 2*burst_pairs1 + 4
    for w in range(burst_pairs2):
        ind = 2*w+burst_pairs2_start
        on_time = int(codes[press][ind],16)
        off_time = int(codes[press][ind+1],16)
        for p in range(on_time):
            wf.append(pigpio.pulse(1<<MOD,0,onperiod))
            wf.append(pigpio.pulse(0,1<<MOD,offperiod))
        wf.append(pigpio.pulse(0,1<<MOD,off_time*uperiod))

    pi.wave_add_generic(wf)
    wave_id = pi.wave_create()
    pi.wave_send_repeat(wave_id)

    print("Begin button hold...")
    time.sleep(hold_time)
    pi.wave_tx_stop()
    print("End Hold.")
        
    