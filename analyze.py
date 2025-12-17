import pickle

#NEC Protocol:
#https://www.sbprojects.net/knowledge/ir/nec.php

with open('codes.pkl','rb') as file:
    codes = pickle.load(file)
print(codes)

# assuming NEC
for b in codes:
    burst_pairs1 = int(codes[b][2],16)
    pronto_freq = int(codes[b][1],16)
    freq = 1000000/(pronto_freq * 0.241246)
    uperiod = int(1000000/freq)
    print(b)
    print("===================")
    print(burst_pairs1)

    burst_pairs2 = int(codes[b][3],16)
    print(burst_pairs2)
    burst_pairs = burst_pairs1 + burst_pairs2
    written = []
    total_msg = []
    a = 0
    for i in range(burst_pairs):
        ind = 2*i+4
        on = int(codes[b][ind],16)
        off = int(codes[b][ind+1],16)
        
        if i != 0:
            a += 1
            if on != off:
                written.append(1)
            else:
                written.append(0)
        if len(written) == 8:
            out = 0
            for bit in written[::-1]:
                out <<= 1
                out |= bit
            total_msg.append(out)
            written = []
    print(a)
    print(total_msg)
    print(total_msg[0],255-total_msg[0])
    print(total_msg[2],255-total_msg[2])
    print("Address:",hex(total_msg[0]*256+total_msg[1]))


        
