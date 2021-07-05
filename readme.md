This tool opens a pcacpng file and replays the goose packets in it in resprective PRP networks.

The LANA and LANB interfaces can be selected as regular network interface, so there is no need for a PRP enabled PC to use it.

usage:

```
usage: gooseplayer.py [-h] [--appid appid] [--srcmac source mac address]
                [--acc accuracy]
                filename interface-a interface-b
```
				
example:

```
python3 gooseplayer.py test.pcapng wi-fi-a Network-b --appid 58 -acc 0.01
```

output:

```
INFO:GooseSim:First Timestamp marked: 1614003243.1967368
INFO:GooseSim:Started Playing test.pcapng
INFO:GooseSim:Channel A: Clock Synched: first ts of capture: 1614003243.1967368, Actual deltat: 11485408.648139477 s
WARNING:GooseSim:Channel B: Delayed Packet 0016ms appid:058 st:2285 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003305.603345
WARNING:GooseSim:Channel B: Delayed Packet 0013ms appid:058 st:2288 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003305.606279
INFO:GooseSim:Succesfully Played test.pcapng, LAN A: 150 telegrams with 212ms delay, LAN B: 150 telegrams with 196ms delay 
```

Both linux and Windows is supported, but linux plays better since python can directly write raw packets without the need of pcap. On linux you may need to run script as root to write raw sockets

The performance is not optimized, it may lag here and there.

VLAN tags are not supported.

This tool may crash anytime

Works with python3 should work with python2 as well but not tested.
