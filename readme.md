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
INFO:GooseSim:Channel A: Clock Synched: first ts of capture: 1614003243.1967368, Actual deltat: 11483018.281332493 s
WARNING:GooseSim:Channel A: Delayed Packet 0010ms appid:058 st:2279 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003255.199737
WARNING:GooseSim:Channel B: Delayed Packet 0011ms appid:058 st:2310 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003383.310439
WARNING:GooseSim:Channel A: Delayed Packet 0011ms appid:058 st:2312 sq:0001 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.7344823
WARNING:GooseSim:Channel A: Delayed Packet 0021ms appid:058 st:2314 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.7439027
WARNING:GooseSim:Channel A: Delayed Packet 0025ms appid:058 st:2316 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.7462208
WARNING:GooseSim:Channel A: Delayed Packet 0016ms appid:058 st:2317 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.746354
WARNING:GooseSim:Channel A: Delayed Packet 0011ms appid:058 st:2318 sq:0001 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.7464015
WARNING:GooseSim:Channel A: Delayed Packet 0012ms appid:058 st:2318 sq:0003 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.7464015
WARNING:GooseSim:Channel A: Delayed Packet 0020ms appid:058 st:2319 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.7702327
WARNING:GooseSim:Channel A: Delayed Packet 0015ms appid:058 st:2319 sq:0001 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.7702327
WARNING:GooseSim:Channel A: Delayed Packet 0011ms appid:058 st:2319 sq:0002 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.7702327
WARNING:GooseSim:Channel A: Delayed Packet 0029ms appid:058 st:2321 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.8213756
WARNING:GooseSim:Channel A: Delayed Packet 0030ms appid:058 st:2322 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.821419
WARNING:GooseSim:Channel A: Delayed Packet 0014ms appid:058 st:2322 sq:0001 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.821419
WARNING:GooseSim:Channel A: Delayed Packet 0016ms appid:058 st:2322 sq:0002 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.821419
WARNING:GooseSim:Channel A: Delayed Packet 0016ms appid:058 st:2322 sq:0004 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.821419
WARNING:GooseSim:Channel A: Delayed Packet 0018ms appid:058 st:2323 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.8932483
WARNING:GooseSim:Channel A: Delayed Packet 0027ms appid:058 st:2324 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.8933744
WARNING:GooseSim:Channel A: Delayed Packet 0033ms appid:058 st:2325 sq:0000 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.893419
WARNING:GooseSim:Channel A: Delayed Packet 0023ms appid:058 st:2325 sq:0001 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.893419
WARNING:GooseSim:Channel A: Delayed Packet 0021ms appid:058 st:2325 sq:0002 pdu:gcbref:M2E01_BEV1_LD0/LLN0$GO$gcb1 tal:11000 datset:M2E01_BEV1_LD0/LLN0$ds_gcb1 goid:M2E01_BEV1_LD0/LLN0gcb1 timestamp:1614003449.893419
INFO:GooseSim:Succesfully Played test.pcapng, LAN A: 150 telegrams, LAN B: 150, telegrams
INFO:GooseSim:Total Delay for Channel A: 571.566104888916 ms
INFO:GooseSim:Total Delay for Channel B: 148.20122718811035 ms
```

Both linux and Windows is supported, but linux plays better since python can directly write raw packets withut the need of pcap.
The performance is not optimized, it may lag here and there.
VLAN tags are not supported.
This tool may crash anytime
Works with python3 should work with python2 as well but not tested.