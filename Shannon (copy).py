import json
import zlib
from math import log
import math


hex2bin_map = {
   "0":"0000",
   "1":"0001",
   "2":"0010",
   "3":"0011",
   "4":"0100",
   "5":"0101",
   "6":"0110",
   "7":"0111",
   "8":"1000",
   "9":"1001",
   "A":"1010",
   "B":"1011",
   "C":"1100",
   "D":"1101",
   "E":"1110",
   "F":"1111",
}
def entropy(string):
        "Calculates the Shannon entropy of a string"

        # get probability of chars in string
        prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]

        # calculate the entropy
        entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])

        return entropy


def entropy_ideal2(length):
        "Calculates the ideal Shannon entropy of a string with given length"

        prob = 1.0 / length

        return -1.0 * length * prob * math.log(prob) / math.log(2.0)


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
with open('json') as f:
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

x=0
for elem in tcp_data_ex:
    if x==1:
        g_data= g_data + (":").encode('latin-1')+elem.encode('latin-1')
        # print(elem.encode('latin1'))
        # g_data= g_data + elem.decode('utf-8').encode('latin1')

        # g_data.extend(elem)
    else:
        x=1
        g_data= elem.encode('latin-1')
        # g_data=bytearray()
        print (type(g_data),"this is it")

f.close()
newstr = g_data.replace(":", "")
# newstr=g.data(replace("0b"))
print(len(newstr))
# print(newst(r)
# newstr=("16030100")
bin_data=(bin(int(newstr, 16))[2:]).zfill(len(newstr*4))



print("length of binary data", len(bin_data))

# print("correct data",bin_data)



value= shannon(bin_data)
value2= entropy_ideal(len(bin_data))
value3=kolmogorov(bin_data) 
print (value)
print("second value of shannon", entropy(bin_data))
print ("ideal shannon entropy",value2)
print ("kolmogorov entropy calculation", value3)

# print("this is prior to conversion", newstr)
""""#
print("this is test of part 2")
file = open("pi","rb")
stringer=b''


try:
    byte =f.read(1)
    while byte != "":
        stringer=stringer+byte
        print(stringer)
        byte=f.read(1)
finally:
    print (stringer)
    f.close()

"""