from pcapng import FileScanner
import logging
import time
import sys
import threading
import platform
import socket
import queue
import argparse
import os


ISLIN = "linux" in platform.system().lower()
DEFACC = 0.01

if not ISLIN:
    from scapy import sendrecv
    from scapy import interfaces


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("GooseSim")


class GooseSim:
    def __init__(self, filename, srcmac=None, gooseappid=None):
        self.deltat = None
        self.firstts = None
        self.lana = []
        self.lanb = []
        self.nonred = []
        self.threada = None
        self.threadb = None
        self.totaldelaya = 0
        self.totaldelayb = 0
        self.logqueue = queue.Queue()
        with open(filename, 'rb') as fp:
            scanner = FileScanner(fp)
            for block in scanner:
                try:
                    data = block.packet_data
                except AttributeError:
                    continue
                src = data[0:6]
                # dst = data[6:12]
                typ = data[12:14]
                if srcmac and srcmac != src:
                    continue
                if typ == b"\x88\xb8": # goose
                    appid = data[14:16]
                    if gooseappid and gooseappid != appid:
                        continue
                    pdulen = int.from_bytes(data[16:18], "big")
                    endpdu = 14 + pdulen
                    suffixlen = len(data) - endpdu
                    if suffixlen == 6:
                        # seqnr = data[endpdu: endpdu + 2]
                        lanid =  int.from_bytes(data[endpdu + 2: endpdu + 3], "big") >> 4
                        suffix = data[endpdu + 4: endpdu + 6]
                        if b"\x88\xfb" == suffix:
                            #PRP:
                            if lanid == 10:
                                self.addgoose(block.timestamp, data, self.lana)
                            else:
                                self.addgoose(block.timestamp, data, self.lanb)
                    else:
                        pass
                        # non redundant gooses
                        
    def addgoose(self, timestamp, data, target):
        if not self.firstts or timestamp < self.firstts:
            self.firstts = timestamp
            logger.info("First Timestamp marked: %s", self.firstts)
        target.append((timestamp, data))
        
    def logger(self):
        stop = 0
        while True:
            if stop == 2:
                break
            channel, deltat, packet = self.logqueue.get()
            if channel is None:
                stop += 1
                continue
            pdu = list(self.parsegoosepdu(packet))
            appid = self._byte2int(packet[14:16])
            sq = pdu.pop()[1]
            st = pdu.pop()[1]
            logger.warning("%s: Delayed Packet %04.fms appid:%03i st:%04i sq:%04i pdu:%s",
                           channel,
                           deltat * 1000,
                           appid,
                           st,
                           sq,
                           " ".join("%s:%s" % (x, y) for x, y in pdu))
            
            
    
    def writer(self, packets, iface, ischana=True, accuracy=DEFACC):
        if ischana:
            channel = "Channel A"
        else:
            channel = "Channel B"
        sender = Sender(iface)
        totaldelay = 0
        for timestamp, packet in packets:
            if not self.deltat:
                while True:
                    if timestamp == self.firstts:
                        self.deltat = time.time() - timestamp
                        logger.info("%s: Clock Synched: first ts of capture: %s, Actual deltat: %s s",
                                    channel,
                                    self.firstts,
                                    self.deltat)
                        break
                    elif self.deltat:
                        break
            targetts = timestamp + self.deltat + totaldelay
            while True:
                deltatpacket = time.time() - targetts
                if deltatpacket >= 0:
                    totaldelay += deltatpacket
                    sender.send(packet)
                    """
                    # most likely this is slower
                    threading.Thread(target=sender.send, args=(packet,)).start()
                    """
                    if deltatpacket >= accuracy:
                        self.logqueue.put((channel, deltatpacket, packet))
                    break
        self.logqueue.put((None, None, None))
        sender.close()
        if ischana:
            self.totaldelaya = totaldelay
        else:
            self.totaldelayb = totaldelay

                        
    def run(self, targetifa, targetifb, accuracy=DEFACC):
        self.threada = threading.Thread(target=self.writer, args=(self.lana, targetifa, True, accuracy))
        self.threadb = threading.Thread(target=self.writer, args=(self.lanb, targetifb, False, accuracy))
        self.loggerthread = threading.Thread(target=self.logger)
        self.threada.start()
        self.threadb.start()
        self.loggerthread.start()
        self.threada.join()
        self.threadb.join()
        self.loggerthread.join()
        
    def _byte2int(self, h):
        return int.from_bytes(h, byteorder="big")
    
    def _byte2ascii(self, h):
        return h.decode()
    
    def _byte2ts(self, h):
        seconds = int.from_bytes(h[:4], byteorder="big")
        fracs = int.from_bytes(h[4:7], byteorder="big") + 1
        return seconds + fracs / 16777216 # fractions / (2 ** 24)
        
    def parsegoosepdu(self, packet):
        cursor = 24
        while True:
            if packet[cursor] == 128:
                break
            cursor += 1
        for attr, callback in [("gcbref", self._byte2ascii), 
                               ("tal", self._byte2int),
                               ("datset", self._byte2ascii),
                               ("goid", self._byte2ascii),
                               ("timestamp", self._byte2ts),
                               ("st", self._byte2int),
                               ("sq", self._byte2int)]:
            itemsize = self._byte2int(packet[cursor + 1:cursor + 2])
            item = callback(packet[cursor + 2: cursor + 2 + itemsize])
            cursor += itemsize + 2
            yield attr, item
        
        
class Sender:
    def __init__(self, interface):
        if ISLIN: 
            self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
            self.socket.bind((interface, 0))
        else:
            found = None
            for iface in interfaces.get_working_ifaces():
                if interface.lower() == iface.name.lower():
                    found = iface
            if not found:
                logger.error("Can not find interface %s", interface)
                sys.exit()
            self.iface = found
    
    def send(self, pkt):
        if ISLIN:
            self.socket.sendall(pkt)
        else:
            sendrecv.sendp(pkt, iface=self.iface, verbose=False)

    def close(self):
        if ISLIN:
            self.socket.close()
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play goose telegrams over network interfaces')
    parser.add_argument('filename', metavar='filename', type=str,  help='pcap file to process')
    parser.add_argument('ifa', metavar='interface-a', type=str,  help='network interface name to play PRP Lan A Goose Telegrams')
    parser.add_argument('ifb', metavar='interface-b', type=str,  help='network interface name to play PRP Lan A Goose Telegrams')
    parser.add_argument('--appid', metavar='appid', type=int,  help='filter goose telgrams according to appid', default=None)
    parser.add_argument('--srcmac', metavar='source mac address', type=str,  help='filter goose telegrams according source mac address', default=None)
    parser.add_argument('--acc', metavar='accuracy', type=float,  help='raise a warning message when accuracy is above the threshold', default=DEFACC)
    
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logger.error("Filename: %s does not exist", args.filename)
        sys.exit()
        
    if args.appid is not None:
        args.appid = (args.appid).to_bytes(2, byteorder="big")
        
    if args.srcmac is not None:
        args.srcmac = bytearray.fromhex(args.srcmac.replace(":", ""))

    
    sim = GooseSim(args.filename, args.srcmac, args.appid)
    logger.info("Started Playing %s", args.filename)
    sim.run(args.ifa, args.ifb, args.acc)
    logger.info("Succesfully Played %s, LAN A: %s telegrams with %.fms delay, LAN B: %s telegrams with %.fms delay ",
                args.filename,
                len(sim.lana),
                sim.totaldelaya * 1000,
                len(sim.lanb),
                sim.totaldelayb * 1000)
