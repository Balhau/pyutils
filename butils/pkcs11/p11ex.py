
from pkcs11 import *

def printInfo(info):
	print "PKCS11 Info"
	print "Major: ",str(ord(info.cryptokiVersion.major)), "Minor: ",str(ord(info.cryptokiVersion.minor))
	print "Manufacturer: ",info.manufacturerID
	print "Flags: ",str(info.flags)
	print "Library Description: ",info.libraryDescription
	print "Library Version: ",str(ord(info.libraryVersion.major)),"Minor: ",str(ord(info.libraryVersion.minor))

pinfo=CK_INFO()
pinfo.cryptokiVersion.major=chr(0x50)
pinfo.cryptokiVersion.minor=chr(0x51)
print "Initialize PKCS11"
print p11.C_Initialize(c_void_p(0))
print "Get PKCS11 Information"
p11.C_GetInfo(byref(pinfo))
printInfo(pinfo)
print "Get Slot List"
#Malloc 10 ulongs
slotIds=(CK_ULONG*10)()
#Crete a pointer to ULONG
slotCount=pointer(c_ulong(10))
p11.C_GetSlotList(CK_TRUE, byref(slotIds),slotCount)
print "Number of Available Slots: ",slotCount.contents
print "Slot id: ",slotIds[0]
handle=pointer(c_ulong(0))
print "Opening Session"
rv=p11.C_OpenSession(slotIds[0],CK_FLAGS(CKF_SERIAL_SESSION),None,None,handle)
print "Open session Result: ", rv
print handle
res=p11.C_Login(handle.contents,CK_USER_TYPE(CKU_USER),c_char_p('1111'),c_ulong(4))
print "Resultado do login: ",res
keyClass=CK_OBJECT_CLASS(CKO_PRIVATE_KEY)
print "KeyClass: ",keyClass
id=CK_BYTE_PTR("Ola mundo")
print id
template=(CK_ATTRIBUTE*2)()
template[0]=CK_ATTRIBUTE(CK_ATTRIBUTE_TYPE(CKA_CLASS),cast(byref(keyClass),CK_VOID_PTR),CK_ULONG(sizeof(keyClass)))
cptr=cast(CK_CHAR_PTR(chr(0x45)),CK_VOID_PTR)
template[1]=CK_ATTRIBUTE(CK_ATTRIBUTE_TYPE(CKA_ID),cptr,CK_ULONG(1))
print CK_ATTRIBUTE_PTR(template)
print handle
print handle.contents
rs=p11.C_FindObjectsInit(handle.contents,CK_ATTRIBUTE_PTR(template),CK_ULONG(1))
print "C_FindObjectsInit Result: ",rs

def getPrivateKey(hsession,idBP=None,idBPLen=0):
	keyClass=CK_OBJECT_CLASS(CKO_PRIVATE_KEY)
	template=(CK_ATTRIBUTE*2)()
	template[0]=CK_ATTRIBUTE(CK_ATTRIBUTE_TYPE(CKA_CLASS),cast(byref(keyClass),CK_VOID_PTR),CK_ULONG(sizeof(keyClass)))
	if idBP!=None:
		cptr=cast(CK_CHAR_PTR(chr(idBP)),CK_VOID_PTR)
		cptr_len=CK_ULONG(1)
	else:
		cptr=None
		cptr_len=CK_ULONG(0)
	template[1]=CK_ATTRIBUTE(CK_ATTRIBUTE_TYPE(CKA_ID),cptr,cptr_len)
	rv=p11.C_FindObjectsInit(hsession.contents,CK_ATTRIBUTE_PTR(template),CK_ULONG(1))
	print "Find Objects Init: ",rv
	ohandle=CK_OBJECT_HANDLE(0)
	ocount=CK_ULONG(0)
	rv=p11.C_FindObjects(hsession.contents,byref(ohandle),CK_ULONG(1),byref(ocount))
	if ocount > 0:
		print "Private Key found: ",ohandle
		return ohandle
	else:
		print "Private Key not found"
		return -1

def getPublicKey(hsession,idBP=None,iBPLen=0):
	keyClass=CK_OBJECT_CLASS(CKO_PUBLIC_KEY)
	template=(CK_ATTRIBUTE*2)()
	template[0]=CK_ATTRIBUTE(CK_ATTRIBUTE_TYPE(CKA_CLASS),cast(byref(keyClass),CK_VOID_PTR),CK_ULONG(sizeof(keyClass)))
	if idBP!=None:
		cptr=cast(CK_CHAR_PTR(chr(idBP)),CK_VOID_PTR)
		cptr_len=CK_ULONG(1)
	else:
		cptr=None
		cptr_len=CK_ULONG(0)
	template[1]=CK_ATTRIBUTE(CK_ATTRIBUTE_TYPE(CKA_ID),cptr,cptr_len)
	rv=p11.C_FindObjectsInit(hsession.contents,CK_ATTRIBUTE_PTR(template),CK_ULONG(1))	
	print "Find Objects Init: ",rv
	ohandle=CK_OBJECT_HANDLE(0)
	ocount=CK_ULONG(0)
	rv=p11.C_FindObjects(hsession.contents,byref(ohandle),CK_ULONG(1),byref(ocount))
	if ocount > 0:
		print "Public Key found: ",ohandle
		return ohandle
	else:
		print "Public Key not found"
		return -1

def digest_data(hsession,dataPointer,digest,digestLen):
	digestmechanism=CK_MECHANISM(CK_MECHANISM_TYPE(CKM_SHA_1),None,CK_ULONG(0))
	rv=p11.C_DigestInit(handle,byref(digestmechanism))

def sign_data(hsession,inputFile,outputFile):
	cinput=CK_CHAR_PTR(inputFile)
	coutput=CK_CHAR_PTR(outputFile)
	privkey=get_private_key(hsession)
	signmechanism=CK_MECHANISM(CK_MECHANISM_TYPE(CKM_RSA_PKCS),None,CK_ULONG(0))
	
print template
#('type',CK_ATTRIBUTE_TYPE),
#('pValue',CK_VOID_PTR),
#('ulValueLen',CK_ULONG),
#template[0]=CK_ATTRIBUTE(CK_ATTRIBUTE_TYPE(),CK_VOID_PTR(0),CK_ULONG(0))
print "Get Private Key"
ohandle=CK_OBJECT_HANDLE(0)
ocount=CK_ULONG(0)
print "POhandle: ",byref(ohandle)
print "POcount: ",byref(ohandle)
rs=p11.C_FindObjects(handle.contents,byref(ohandle),CK_ULONG(1),byref(ocount))
print "C_FindObjects Result: ",rs
rs=p11.C_FindObjectsFinal(handle.contents)
print "C_FindObjectsFinal Result: ",rs
print "Object count value: ",ocount
print "Object Value: ",ohandle

print "Private Key: ",getPrivateKey(handle)
print "Public Key: ",getPublicKey(handle)

digest=cast((CK_BYTE*20)(),CK_BYTE_PTR)
signature=cast((CK_BYTE*512)(),CK_BYTE_PTR)
digestmechanism=CK_MECHANISM(CK_MECHANISM_TYPE(CKM_SHA_1),None,CK_ULONG(0))
print digestmechanism
print "Handle: ",handle
print "Digest Init: ",p11.C_DigestInit(handle.contents,byref(digestmechanism))
slotList=(CK_SLOT_ID*1)()
slotCount=(CK_ULONG*1)()
print hex(p11.C_GetSlotList(CK_BBOOL(chr(0)),slotList,slotCount))
print slotList[0]
9999
