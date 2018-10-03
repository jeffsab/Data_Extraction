import json
import zlib
from math import log
import math
import os
import csv
import numpy
import pandas
import operator
from scipy.stats import chisquare
import scipy.special as spc
import scipy.fftpack as sff
import scipy.stats as sst
def serial(bin_data, pattern_length=16, method="both"):

    bin_data="11101111011"
    """
    Note that this description is taken from the NIST documentation [1]
    [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf

    The focus of this test is the frequency of all possible overlapping m-bit patterns across the entire
    sequence. The purpose of this test is to determine whether the number of occurrences of the 2m m-bit
    overlapping patterns is approximately the same as would be expected for a random sequence. Random
    sequences have uniformity; that is, every m-bit pattern has the same chance of appearing as every other
    m-bit pattern. Note that for m = 1, the Serial test is equivalent to the Frequency test of Section 2.1.

    :param bin_data: a binary string
    :param pattern_length: the length of the pattern (m)
    :return: the P value
    """
    n = len(bin_data)
    # Add first m-1 bits to the end
    bin_data += bin_data[:pattern_length - 1:]

    # Get max length one patterns for m, m-1, m-2
    max_pattern = ''
    for i in range(pattern_length + 1):
        max_pattern += '1'

    # Keep track of each pattern's frequency (how often it appears)
    vobs_one = numpy.zeros(int(max_pattern[0:pattern_length:], 2) + 1)
    vobs_two = numpy.zeros(int(max_pattern[0:pattern_length - 1:], 2) + 1)
    vobs_thr = numpy.zeros(int(max_pattern[0:pattern_length - 2:], 2) + 1)

    for i in range(n):
        # Work out what pattern is observed
        vobs_one[int(bin_data[i:i + pattern_length:], 2)] += 1
        vobs_two[int(bin_data[i:i + pattern_length - 1:], 2)] += 1
        vobs_thr[int(bin_data[i:i + pattern_length - 2:], 2)] += 1

    vobs = [vobs_one, vobs_two, vobs_thr]
    sums = numpy.zeros(3)
    for i in range(3):
        for j in range(len(vobs[i])):
            sums[i] += pow(vobs[i][j], 2)
        sums[i] = (sums[i] * pow(2, pattern_length - i) / n) - n

    # Calculate the test statistics and p values
    del1 = sums[0] - sums[1]
    del2 = sums[0] - 2.0 * sums[1] + sums[2]
    p_val_one = spc.gammaincc(pow(2, pattern_length - 1) / 2, del1 / 2.0)
    p_val_two = spc.gammaincc(pow(2, pattern_length - 2) / 2, del2 / 2.0)

    # For checking the outputs
    if method == "first":
        return p_val_one
    elif method == "both":
        return p_val_one, p_val_two
    else:
        # I am not sure if this is correct, but it makes sense to me.
        return min(p_val_one, p_val_two)


def monobit(bin_data):
    """
    Note that this description is taken from the NIST documentation [1]
    [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf

    The focus of this test is the proportion of zeros and ones for the entire sequence. The purpose of this test is
    to determine whether the number of ones and zeros in a sequence are approximately the same as would be expected
    for a truly random sequence. This test assesses the closeness of the fraction of ones to 1/2, that is the number
    of ones and zeros ina  sequence should be about the same. All subsequent tests depend on this test.

    :param bin_data: a binary string
    :return: the p-value from the test
    If P-value is less than 0.01, then it is non-random, else data is random
    """
    # bin_data="1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000" #example given by nist documentation p val 0.109599
    count = 0
    # If the char is 0 minus 1, else add 1
    for char in bin_data:
        if char == '1':
            count -= 1
        else:
            count += 1
    # Calculate the p value
    sobs = count / math.sqrt(len(bin_data))
    p_val = spc.erfc(math.fabs(sobs) / math.sqrt(2))
    return p_val

def chi_squared(data):

    #null hypothesis is that the data is not random, threfore p value has to be less than 0.05 to reject it
    freq={}
    for c in map(operator.add, data[::2], data[1::2]):
        if freq.get(c):
            freq[c] += 1
        else:
            freq[c] = 1


    dataset= [0]*256
    a=0
    for key in freq.keys():
        dataset[a]= freq[key]
        a+=1

    chi_square = chisquare(dataset)
    # print(dataset)
    # print(chi_square)
    return chi_square
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
