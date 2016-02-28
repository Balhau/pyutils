'''
Created on 9 de Mar de 2013
@author: balhau
'''

from pkcs11 import *

class PyPKCS11:
    EXIT_FAILURE=1
    EXIT_OK=0
    
    def __init__(self,clib):
        self.p11=clib;
        
    def check_return_value(self,rv,msg):
        if rv!=CKR_OK:
            print "Error ",rv,": ",msg
            exit(PyPKCS11.EXIT_FAILURE)
    
    def Initialize(self):
        return self.p11.C_Initialize(CK_VOID_PTR(0))
    
    def getSlot(self):
        rv=0
        maxSlots=10
        slotCount=CK_ULONG(maxSlots)
        slotIds=(CK_SLOT_ID*maxSlots)(0)
        
        rv=self.p11.C_GetSlotList(CK_TRUE,slotIds,byref(slotCount))
        self.check_return_value(rv, "Error while geting the slot list")
        
        print slotCount
        


common=CDLL('./libpteidcommon.so.2.0.0')
qtdialogs=CDLL('./libpteiddialogsQT.so.2.0.0')
cardlayer=CDLL('./libpteidcardlayer.so.2.0.0')
libp11=CDLL('./libpteidpkcs11.so.2.0.0')

p11=PyPKCS11(libp11)
p11.Initialize()
p11.getSlot()
