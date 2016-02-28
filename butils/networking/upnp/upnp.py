
import sys
import os
import socket
from select import select
import struct
import urllib3
import requests
from bs4 import BeautifulSoup

class SSDPMessage():

    sdpMap={}

    def __init__(self,data):
        self.sdpMap=self.parseData(data)

    def parseData(self,data):
        dmap={}
        lines=data.split("\n")
        for line in lines:
            prop=line.split(":",1)
            if(len(prop)>1):
                dmap[prop[0].replace(":","")]=prop[1].replace("\r","")
        return dmap


class Upnp():

    SSDP_ADDR = "239.255.255.250";
    SSDP_PORT = 1900;
    bcastend=(SSDP_ADDR,SSDP_PORT)
    SSDP_MX = 3;
    GET_EXTERNAL_IP_XML_MESSAGE='''
<?xml version="1.0 ?>
    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <s:Body>
            <u:GetExternalIPAddress xmlns:u="urn:schemas-upnp-org:service:WANPPPConnection:1">
            </u:GetExternalIPAddress>
        </s:Body>
    </s:Envelope>
'''
    SSPD_STYPE="urn:schemas-upnp-org:service:WANPPPConnection:1"
    SSDP_ST = "urn:all";

    ssdpRequest = "M-SEARCH * HTTP/1.1\r\n" + \
                "HOST: %s:%d\r\n" % (SSDP_ADDR, SSDP_PORT) + \
                "MAN: \"ssdp:discover\"\r\n" + \
                "MX: %d\r\n" % (SSDP_MX, ) + \
                "ST: %s\r\n" % (SSDP_ST, ) + "\r\n";

    def broadcastRequest(self):

        # Create the socket
        sockr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to the server address
        sockr.bind(('',1900))
        ipmulticast,port=self.bcastend
        group = socket.inet_aton(ipmulticast)

        #pack the multicast address
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sockr.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,mreq)
        i=0
        sockr.sendto(self.ssdpRequest,self.bcastend)
        sockr.settimeout(2.0)

        sdpResp=[]

        try:
            while True:
                data,address=sockr.recvfrom(1024)
                sdpm=SSDPMessage(data).sdpMap
                if 'LOCATION' in sdpm.keys():
                    sdpResp.append(sdpm)
                    i=i+1
        except:
            pass

        return sdpResp



a=Upnp()
responses=a.broadcastRequest()
for resp in responses:
    print resp
    print '****************************'

link="http://192.168.1.1:1900/igd.xml"
http = urllib3.PoolManager()
r = http.request('GET', link)

soup=BeautifulSoup(r.data)

for service in soup.find_all('service'):
    print service

print "Posting xml soap command to retrieve the external IP"

GET_EXTERNAL_IP_XML_MESSAGE='''
<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <s:Body>
        <u:GetExternalIPAddress xmlns:u="urn:schemas-upnp-org:service:WANIPConnection:1">
        </u:GetExternalIPAddress>
    </s:Body>
</s:Envelope>'''

GET_GENERIC_PORTMAP_ENTRY='''
<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <s:Body>
        <u:GetGenericPortMappingEntry xmlns:u="urn:schemas-upnp-org:service:WANIPConnection:1">
            <NewPortMappingIndex>0</NewPortMappingIndex>
        </u:GetGenericPortMappingEntry>
    </s:Body>
</s:Envelope>
'''

HEADER_GENERIC_PORT_MAPPING='"urn:schemas-upnp-org:service:WANIPConnection:1#GetGenericPortMappingEntry"'

eiplink="http://192.168.1.1:1900/ipc"

HEADER_IPADDRESS='"urn:schemas-upnp-org:service:WANIPConnection:1#GetExternalIPAddress"'
heip={'SOAPACTION':HEADER_IPADDRESS,'CONTENT-TYPE':'text/xml; charset="utf-8"'}



r=requests.post(url=eiplink,data=GET_EXTERNAL_IP_XML_MESSAGE,headers=heip)

print "Response: ",r.text

ipxml=BeautifulSoup(r.text)

print ipxml.find_all('newexternalipaddress')[0].string


hgpm={'SOAPACTION':HEADER_GENERIC_PORT_MAPPING,'CONTENT-TYPE':'text/xml; charset="utf-8"'}
r=requests.post(url=eiplink,data=GET_GENERIC_PORTMAP_ENTRY,headers=hgpm)

print "Response: ",r.text

rhxml=BeautifulSoup(r.text)

print "Remote Host: ", rhxml.find('newremotehost').string
print "Internal Host: ",rhxml.find('newinternalclient').string
print "Description: ", rhxml.find('newportmappingdescription').string
print "External Port: ", rhxml.find('newexternalport').string
print "Internal Port: ", rhxml.find('newinternalport').string
