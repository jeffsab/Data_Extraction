import json
import zlib
from math import log
import unicodedata

def byte_entropy(flow):
    if flow.has_key("be"):
        flow_info = {}
        flow_info["source address"] = flow["sa"]
        flow_info["destination address"] = flow["da"]
        flow_info["source port"] = flow["sp"]
        flow_info["destination port"] = flow["dp"]
        flow_info["Byte Entropy"] = flow["be"]
    else:
        return
    return flow_info

def shannon (data):
    # Whithin the for statement, we determine the frequency of each byte
    # in the dataset and if this frequency is not null we use it for the
    # entropy calculation

    dataSize = len(data)
    ent = 0.0
    freq={}
    for c in data:
        if freq.has_key(c):
            freq[c] += 1
        else:
            freq[c] = 1

   # a byte can take 256 values from 0 to 255. Here we are looping 256 times
   # to determine if each possible value of a byte is in the dataset
    for key in freq.keys():
        f = float(freq[key])/dataSize+0.0
        if f > 0: # to avoid an error for log(0)
            ent = ent + f * log(f, 2)
    return -ent  if ent else 0.00


def entropy_ideal(length):
    if length == 0: return 0.0
    prob = 1.0 / length + 0.0
    return -1.0 * length * prob * log(prob) / log(2.0)


# Reasonable approximation to the Kolmogorov Complexity
# using the compression rate
# ref.: http://lorenzoriano.wordpress.com/tag/python/
def kolmogorov(data):
    if data == None or data == '':

        return 0

    l = float(len(data))
    compr = zlib.compress(data)
    c = float(len(compr))/l
    if c > 1:
        return 1.0
    else:
        return c

flow=[]
byte_entropy_per_flow = []
with open('tester2') as f:
    data = json.load(f);

total_flows= len(data)
# pprint(data)
tcp_data_ex=[]

    # print(data['layers']['frame']['tcp.payload'])
for packet in data:
     try:
             # print(packet[u'_source'][u'layers'][u'tcp'][u'tcp.payload'])
             tcp_data_ex.append(packet[u'_source'][u'layers'][u'tcp'][u'tcp.payload'])
     except KeyError:
            continue

g_data=""
x=0
for elem in tcp_data_ex:
    if x==1:
        g_data= g_data + (":").encode('latin-1')+elem.encode('latin-1')
    else:
        x=1
        g_data=elem.encode('latin-1')

print("this is the data")
# tcp_data_ex=tcp_data_ex.encode('latin-1')
print(g_data)
print(tcp_data_ex)
val_prior_convert= shannon(tcp_data_ex[2])
tcp_data_ex2 = tcp_data_ex

print(len(g_data))
value= shannon(tcp_data_ex2)
value2= entropy_ideal(len(tcp_data_ex2))
value3=kolmogorov(g_data)
print (value)
print (value2)
print (value3)

print("this is prior to conversion", val_prior_convert)

print("this is test of part 2")
file = open("pi","rb")
stringer=b''
edsx try:
    byte =f.read(1)
    while byte != "":
        stringer=stringer+byte
        print(stringer)
        byte=f.read(1)
finally:
    print (stringer)
    f.close()