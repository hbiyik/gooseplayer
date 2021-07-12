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
PROFILE = False
CHANA = "A"
CHANB = "B"
NONRED = "NONRED"

if not ISLIN:
    from scapy import interfaces
    from scapy.arch.libpcap import L2pcapSocket
    from scapy.libs.winpcapy import pcap_sendpacket

if PROFILE:
    import pprofile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("GooseSim")


class GooseSim:
    def __init__(self, filename, sendera, senderb, sendernonred, routea=False, routeb=False, srcmac=None, gooseappid=None, forcevlan=None):
        self.deltat = None
        self.firstts = None
        self.routea = routea
        self.routeb= routeb
        self.sendera = sendera
        self.senderb = senderb
        self.sendernonred = sendernonred
        self.lana = []
        self.lanb = []
        self.nonred = []
        self.threada = None
        self.threadb = None
        self.totaldelaya = 0
        self.totaldelayb = 0
        self.totaldelaynonred = 0
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
                if srcmac and srcmac != src:
                    continue
                isgoose, voffset = self.isgoose(data)
                if voffset and forcevlan is not None:
                    vlantag = (((data[14] & 0xF0) << 8) + (forcevlan & 0xFFF)).to_bytes(2, byteorder='big')
                    data = data[0:14] + vlantag + data[16:] 
                if isgoose: # goose
                    appid = data[voffset + 14: voffset + 16]
                    if gooseappid and gooseappid != appid:
                        continue
                    pdulen = int.from_bytes(data[voffset + 16: voffset + 18], "big")
                    endpdu = 14 + pdulen + voffset
                    suffixlen = len(data) - endpdu
                    if suffixlen == 6:
                        # seqnr = data[endpdu: endpdu + 2]
                        lanid =  int.from_bytes(data[endpdu + 2: endpdu + 3], "big") >> 4
                        suffix = data[endpdu + 4: endpdu + 6]
                        if b"\x88\xfb" == suffix:
                            #PRP:
                            if lanid == 10:
                                # LAN A
                                if self.routea and self.sendernonred.iface:
                                    self.addgoose(block.timestamp, data, self.nonred)
                                if self.sendera.iface:
                                    self.addgoose(block.timestamp, data, self.lana)
                            else:
                                # LAN B
                                if self.routeb and self.sendernonred.iface:
                                    self.addgoose(block.timestamp, data, self.nonred)
                                if self.senderb.iface:
                                    self.addgoose(block.timestamp, data, self.lanb)
                    else:
                        # non redundant gooses
                        self.addgoose(block.timestamp, data, self.nonred)

    def isgoose(self, data):
        voffset = 0
        typ = data[12:14]
        if typ == b"\x81\x00": #vlan
            voffset = 4
            typ = data[16:18]
        return b"\x88\xb8" == typ, voffset 
                        
                        
    def addgoose(self, timestamp, data, target):
        if not self.firstts or timestamp < self.firstts:
            self.firstts = timestamp
            logger.info("First Timestamp marked: %s", self.firstts)
        target.append((timestamp, data))
        
    def logger(self):
        stop = 0
        while True:
            if stop == 3:
                break
            channel, deltat, packet = self.logqueue.get()
            if channel is None:
                stop += 1
                continue
            isgoose, voffset = self.isgoose(packet)
            if isgoose:
                pdu = list(self.parsegoosepdu(packet[voffset + 14:]))
                appid = self._byte2int(packet[voffset + 14: voffset + 16])
                sq = pdu.pop()[1]
                st = pdu.pop()[1]
                logger.warning("%s: Delayed Packet %04.fms appid:%03i st:%04i sq:%04i pdu:%s",
                               channel,
                               deltat * 1000,
                               appid,
                               st,
                               sq,
                               " ".join("%s:%s" % (x, y) for x, y in pdu))
            
            
    
    def writer(self, packets, chan, accuracy=DEFACC):
        if PROFILE:
            prof = pprofile.Profile()
            prof.enable()
        channel = "Channel %s" % chan
        if chan == CHANA:
            sender = self.sendera
        elif chan == CHANB:
            sender = self.senderb
        else:
            sender = self.sendernonred
        totaldelay = 0
        if sender.iface is None:
            totaldelay = -1
        else:
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
        if chan == CHANA:
            self.totaldelaya = totaldelay
        elif chan == CHANB:
            self.totaldelayb = totaldelay
        else:
            self.totaldelaynonred = totaldelay
        if PROFILE:
            prof.disable()
            prof.dump_stats("stats.txt")

                        
    def run(self, accuracy=DEFACC):
        self.threada = threading.Thread(target=self.writer,
                                        args=(self.lana, CHANA, accuracy))
        self.threadb = threading.Thread(target=self.writer,
                                        args=(self.lanb, CHANB, accuracy))
        self.threadnonred = threading.Thread(target=self.writer,
                                        args=(self.nonred, NONRED, accuracy))
        self.loggerthread = threading.Thread(target=self.logger)

        self.threada.start()
        self.threadb.start()
        self.threadnonred.start()
        self.loggerthread.start()
        
        self.threada.join()
        self.threadb.join()
        self.threadnonred.join()
        self.loggerthread.join()
        
    def _byte2int(self, h):
        return int.from_bytes(h, byteorder="big")
    
    def _byte2ascii(self, h):
        return h.decode("ascii", "replace")
    
    def _byte2ts(self, h):
        seconds = int.from_bytes(h[:4], byteorder="big")
        fracs = int.from_bytes(h[4:7], byteorder="big") + 1
        return seconds + fracs / 16777216 # fractions / (2 ** 24)
        
    def parsegoosepdu(self, telegram):
        cursor = 10
        while True:
            if telegram[cursor + 1] != 128 and telegram[cursor] == 128:
                break
            cursor += 1
        for attr, callback in [("gcbref", self._byte2ascii), 
                               ("tal", self._byte2int),
                               ("datset", self._byte2ascii),
                               ("goid", self._byte2ascii),
                               ("timestamp", self._byte2ts),
                               ("st", self._byte2int),
                               ("sq", self._byte2int)]:
            itemsize = self._byte2int(telegram[cursor + 1:cursor + 2])
            item = callback(telegram[cursor + 2: cursor + 2 + itemsize])
            cursor += itemsize + 2
            yield attr, item
        
        
class Sender:
    def __init__(self, interface, chan):
        self.iface = None
        if ISLIN:
            try:
                self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
                self.socket.bind((interface, 0))
                self.iface = interface
            except Exception:
                pass
            
        else:
            found = None
            for iface in interfaces.get_working_ifaces():
                if interface.lower() == iface.name.lower():
                    found = iface
            self.iface = found
            if self.iface:
                self.socket = L2pcapSocket(self.iface)
        if not self.iface:
            logger.info("Channel %s can not use interface %s. Interface not found", chan, interface)
        else:
            logger.info("Channel %s is using interface %s.", chan, interface)
    
    def send(self, pkt):
        if ISLIN:
            self.socket.sendall(pkt)
        else:
            pcap_sendpacket(self.socket.outs.pcap, pkt, len(pkt))

    def close(self):
        if ISLIN:
            self.socket.close()
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play goose telegrams over network interfaces')
    parser.add_argument('filename', metavar='filename.pcapng', type=str,  help='pcapng file to process')
    parser.add_argument('ifa', metavar='interface-a', type=str,  help='network interface name to play PRP Lan A Goose Telegrams')
    parser.add_argument('ifb', metavar='interface-b', type=str,  help='network interface name to play PRP Lan A Goose Telegrams')
    parser.add_argument('ifnonred', metavar='interface-nonred', type=str,  help='network interface name to play Non Redundant Goose Telegrams')
    parser.add_argument('--appid', metavar='appid', type=int,  help='filter goose telegrams according to appid', default=None)
    parser.add_argument('--forcevlan', metavar='force vlan id', type=int,  help='force vlan id of the published goose telegrams', default=None)
    parser.add_argument('--srcmac', metavar='source mac address', type=str,  help='filter goose telegrams according source mac address', default=None)
    parser.add_argument('--routea', help='route lana telegrams to non redundant interface', action="store_true")
    parser.add_argument('--routeb', help='route lanb telegrams to non redundant interface', action="store_true")
    parser.add_argument('--acc', metavar='accuracy', type=float,  help='raise a warning message when accuracy is above the threshold', default=DEFACC)
    
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        logger.error("Filename: %s does not exist", args.filename)
        sys.exit()
        
    if args.appid is not None:
        args.appid = (args.appid).to_bytes(2, byteorder="big")
        
    if args.srcmac is not None:
        args.srcmac = bytearray.fromhex(args.srcmac.replace(":", ""))

    
    sendera = Sender(args.ifa, CHANA)
    senderb = Sender(args.ifb, CHANB)
    sendernonred = Sender(args.ifnonred, NONRED)
    sim = GooseSim(args.filename, sendera, senderb, sendernonred,
                   args.routea, args.routeb, args.srcmac, args.appid, args.forcevlan)
    logger.info("Started Playing %s", args.filename)
    sim.run(args.acc)
    
    logger.info("Succesfully Played %s, LAN A: %s telegrams with %.fms delay, LAN B: %s telegrams with %.fms delay, NONRED: %s telegrams with %.fms delay",
                args.filename,
                0 if sim.totaldelaya == -1 else len(sim.lana),
                0 if sim.totaldelaya == -1 else sim.totaldelaya * 1000,
                0 if sim.totaldelayb == -1 else len(sim.lanb),
                0 if sim.totaldelayb == -1 else sim.totaldelayb * 1000,
                0 if sim.totaldelaynonred == -1 else len(sim.nonred),
                0 if sim.totaldelaynonred == -1 else sim.totaldelaynonred * 1000)