#jeffrey Sabri 2018 Aug
from scapy_ssl_tls.ssl_tls import *
from scapy.layers import *


def getcts(pkts):
    a = []
    for pkt in pkts:
        if pkt.haslayer(SSL):
            a.append(pkt)
    return a


if __name__ =="__main__":
    pkts = rdpcap('google_check.pcapng')
    data=getcts(pkts)

