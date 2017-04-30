import yaml
from kazoo.client import KazooClient
import threading
import hashlib
import socket

def synchronized(func):
    func.__lock__ = threading.Lock()
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)
    return synced_func


class MapServer():
    def __init__(self,num_slots,properties):
        self.cache = {}
        self.state=None
        self.props = properties
        self.num_slots=num_slots
        self.zk_root=self.props['zookeeper']['root']
        self.zk = KazooClient(hosts=self.props['zookeeper']['path'])
        self.id = self.props['server']['ip']+"-"+str(self.props['server']['port'])
        print self.id
        self.zk.start()
        self.zk.ensure_path(self.zk_root)
        self.zkState = self.zk.get_children(self.zk_root,watch=self.watchForPeers)

    def register(self):
        self.zk.create(self.zk_root+"/"+self.id,ephemeral = True)

    def hashKey(self,key):
        hkey=hashlib.sha224(key).hexdigest()
        chs=[ord(c) for c in hkey]
        v=sum(chs) % self.num_slots
        slot=[s[0] for s in self.state if(s[1]<v and v < s[2])]
        return slot


    def watchForPeers(self,children):
        self.zkState = self.zk.get_children(self.zk_root,watch=self.watchForPeers)
        self.updateState()

    def updateState(self):
        print self.zkState
        l = len(self.zkState)
        #compute slots
        self.state=[(self.zkState[x],self.num_slots/(l-x+1) if x != 0 else 0,self.num_slots/(l-x)) for x in range(l)]

    def stop(self):
        self.zk.stop()
        self.zk.close()

    def setKey(self,key,val,raw):
        slotId=self.hashKey(key)[0]
        if(slotId==self.id):
            print "Saved locally"
            self.cache[key]=val
        else:
            print "Sending to other node", slotId
            (host,port)=slotId.split("-")
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((host,int(port)))
            s.sendall(raw)
            s.close()

    #s@synchronized
    def processMessage(self,msg,con):
        try:
            print "processing message"
            l = msg.split(" ")
            if l[0].strip() == "set":
                (op,key,value)=l
                self.setKey(key.strip(),value.strip(),msg)
            if l[0].strip() == "get":
                if(len(l)==2):
                    (op,key)=l
                    con.sendall(self.cache[key.strip()]+"\n")
                else:
                    con.sendall(str(self.cache)+"\n")
            if l[0].strip() == "del":
                (op,key)=l
                del self.cache[key.strip()]
        except:
            pass


    def getPeers():
        print "Getting peers"
