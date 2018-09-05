import json
import urllib

import json
from pprint import pprint


with open('tester') as f:
    data = json.load(f);

total_flows= len(data)
pprint(data)

    # print(data['layers']['frame']['tcp.payload'])
print (total_flows)
flow=[]
flow_counter = 0

byte_entropy_per_flow = []

for g in data:
    # print("abc")
    try:
        print("dsadsadsa")
        if flow_counter != 3:
            print("44234324")
            byte_entropy_per_flow.append(g['om_points'])
    except:
        pass
#		print byte_entropy_per_flow
#		quit()
    flow_counter += 1

print("abc")
pprint(total_flows)
pprint(flow)
pprint (byte_entropy_per_flow)
# f = gzip.open(output[7:],"rb")
# file = f.readlines()
# total_flows = len(file)