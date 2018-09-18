import json
from pprint import pprint
import binascii
import bitarray

"""
shit=[]
with open('tester') as f:
    data = json.load(f)
    shit.append(data["maps"][0]["id"])
    shit.append(data["masks"]["id"])
    shit.append(data["om_points"])


pprint(shit)
"""

abcd=b''
print (type(abcd))
unicodestring = u"Hello world"
# Convert Unicode to plain Python string: "encode"
unicodestring = u"Hello world"
# Convert Unicode to plain Python string: "encode"
utf8string = unicodestring.encode("utf-8")
asciistring = unicodestring.encode("ascii")
isostring = unicodestring.encode("ISO-8859-1")
utf16string = unicodestring.encode("utf-16")
# Convert plain Python string to Unicode: "decode"
plainstring1 = unicode(utf8string, "utf-8")
plainstring2 = unicode(asciistring, "ascii")
plainstring3 = unicode(isostring, "ISO-8859-1")
plainstring4 = unicode(utf16string, "utf-16")
assert plainstring1 == plainstring2 == plainstring3 == plainstring4

print (utf8string,asciistring,isostring,utf16string,plainstring1,plainstring2,plainstring3,plainstring4)

st = "hello world"
abc=''
print(abc.join(format(ord(x), 'b') for x in st))

item = u'usomestring'
decoded_value = item.decode('utf-8')
# decoded_value=decoded_value.decode('utf-8')
print(decoded_value)
decoded_value=decoded_value.encode('utf-8')
print(decoded_value,"fasdsa")
b = bitarray.bitarray()
b.fromstring(decoded_value)
