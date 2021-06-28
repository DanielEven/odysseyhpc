# Packet Analysis with scapy

Scapy is a library made in Python, with its own command line interpreter (CLI), which allows to create, modify, send and capture network packets.

It can be used interactively through the command line interface or as a library by importing it into Python programs. It can also run on Linux, Mac OS X and Windows systems.

There are a *lot* of references about scapy out there. We will shortly cover how to inspect packets with scapy. Try it in your own Python shell!

```python
from scapy.packet import Raw
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, UDP

# build an example packet
packet = (
    Ether(src="20:00:00:00:00:00", dst="20:00:00:00:00:02")
    / IP(src="10.0.0.1", dst="10.0.0.2")
    / UDP(dport=1337, sport=13337)
    / Raw("A" * 10)
)
# get Ethernet header (L2)
packet.fields
# output: {'dst': '20:00:00:00:00:02', 'src': '20:00:00:00:00:00'}
# get IP header (L3)
packet[IP]
# output: <IP  frag=0 proto=udp src=10.0.0.1 dst=10.0.0.2 |<UDP  sport=13337 dport=1337 |<Raw  load='AAAAAAAAAA' |>>>
# get UDP header (L4)
packet[UDP]
# output: <UDP  sport=13337 dport=1337 |<Raw  load='AAAAAAAAAA' |>>
```

For more information and APIs, read the [official docs](https://scapy.readthedocs.io/en/latest/).
