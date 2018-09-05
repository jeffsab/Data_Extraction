import json
from pprint import pprint


shit=[]
with open('tester') as f:
    data = json.load(f)
    shit.append(data["maps"][0]["id"])
    shit.append(data["masks"]["id"])
    shit.append(data["om_points"])


pprint(shit)