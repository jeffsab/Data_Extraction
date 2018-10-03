import json
import zlib
from math import log
import math
import os
import csv
import numpy
import pandas
import operator

# import RandomnessTester


def arithmatic(data):
    # Whithin the for statement, we determine the frequency of each byte
    # in the dataset and if this frequency is not null we use it for the
    # entropy calculation

    dataSize = len(data)/2 #divided by 2 as it is taking a byte not 4 bits
    ent = 0.0
    freq = {}
    # for c in data:
    for c in map(operator.add, data[::2], data[1::2]):
        if freq.get(c):
            freq[c] += 1
        else:
            freq[c] = 1
    mean=0
    # a byte can take 256 values from 0 to 255. Here we are looping 256 times
    # to determine if each possible value of a byte is in the dataset
    for key in freq.keys():
        total= int(key,16)* freq[key]
        mean=mean+total

    return mean/dataSize

def shannon(data):
    # Whithin the for statement, we determine the frequency of each byte
    # in the dataset and if this frequency is not null we use it for the
    # entropy calculation

    dataSize = len(data)/2 #divided by 2 as it is taking a byte not 4 bits
    ent = 0.0
    freq = {}
    # for c in data:
    for c in map(operator.add, data[::2], data[1::2]):
        if freq.get(c):
            freq[c] += 1
        else:
            freq[c] = 1

    # a byte can take 256 values from 0 to 255. Here we are looping 256 times
    # to determine if each possible value of a byte is in the dataset
    for key in freq.keys():
        f = float(freq[key]) / dataSize + 0.0
        if f > 0:  # to avoid an error for log(0)
            ent = ent + f * log(f, 2)
    return -ent if ent else 0.00


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
    my_str_as_bytes = bytearray.fromhex(data)
    l = float(len(data))
    compr = zlib.compress(my_str_as_bytes)
    c = float(len(compr)) / l
    if c > 1:
        return 1.0
    else:
        return c


if __name__ == "__main__":

    flow = []
    byte_entropy_per_flow = []
    with open('json') as f:
        data = json.load(f);

    total_flows = len(data)
    # pprint(data)
    tcp_data_ex = []
    # print(data['layers']['frame']['tcp.payload'])
    tcp_data_ex2 = []

    # this is for cipher suite the data is saved as an integer, got to convert this back to hex and check with file if recommended
    # the code for it is packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][ssl.handshake.ciphersuite]

    for packet in data:
        try:

            # print(packet[u'_source'][u'layers'][u'frame'][u'frame.number'][0:])
            # print(type(packet[u'_source'][u'layers'][u'tcp'][u'tcp.payload']))
            # print((packet[u'_source'][u'layers'][u'ssl'][u'ssl.record']))

            # tcp_data_ex.append(packet[u'_source'][u'layers'][u'tcp'][u'tcp.payload'])

            # print(packet[u'_source'][u'layers'][u'tcp'][u'tcp.payload'])
            # print(packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.app_data'])
            # print("this is the length", len(packet[u'_source'][u'layers'][u'ssl']))

            if (len(packet[u'_source'][u'layers'][u'ssl']) == 1):

                if (
                int(packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.record.content_type']) == 22 and int(
                        packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.record.length']) > 45):

                    # print ("length of ssl", (packet[u'_source'][u'layers'][u'ssl']))

                    print(int(
                        packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.handshake'][u'ssl.handshake.type']))

                    print(type(int(
                        packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.handshake'][u'ssl.handshake.type'])))

                    if (int(packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.handshake'][
                                u'ssl.handshake.type']) == 2):
                        print(("type of encryption" , hex(int(packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.handshake'][u'ssl.handshake.ciphersuite']))))

                # print("this is the length", len(packet[u'_source'][u'layers'][u'ssl']))
                # print(packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.app_data'])
                # print(type(packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.app_data']))


                # tcp_data_ex.append(packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.app_data'][24:]) #remove first 24 as they are always same, but shouldnt be this way
                tcp_data_ex.append(packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.app_data'])


                # print((packet[u'_source'][u'layers'][u'ssl']))

                # if (len(packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'])==1):
                # print("the code for it is", packet[u'_source'][u'layers'][u'ssl'][u'ssl.record'][u'ssl.record.content_type'])


        except KeyError:
            continue

    # print(tcp_data_ex)

    # print ("abcdsadsa", tcp_data_ex )
    print("length of ssl strip", len(tcp_data_ex))
    x = 0

    for elem in tcp_data_ex:
        if x == 1:
            # g_data= g_data + (":").encode('latin-1')+elem.encode('latin-1')
            # print(elem.encode('latin1'))
            g_data = g_data + elem

            # g_data.extend(elem)
        else:
            x = 1
            # g_data= elem.encode('latin-1')
            g_data = elem
            # g_data=bytearray()
            print(type(g_data), "this is it")
            print(elem)

    f.close()
    newstr = g_data.replace(":", "")
    # newstr=g.data(replace("0b"))

    print(len(newstr))
    # print(newst(r)
    # newstr=("16030100")
    bin_data = (bin(int(newstr, 16))[2:]).zfill(len(newstr * 4))

    print("length of binary data", len(bin_data))

    # print("correct data",bin_data)
    print("arithmatic mean", arithmatic(newstr))
    value = shannon(newstr)
    value2 = entropy_ideal(16)
    value3 = kolmogorov(newstr)

    print("second value of shannon", value)
    print("ideal shannon entropy", value2)
    print("kolmogorov entropy calculation", value3)
    # print("this is prior to conversion", newstr)

    """
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
