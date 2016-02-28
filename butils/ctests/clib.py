'''
Created on 3 de Fev de 2013
@author: balhau
'''
from ctypes import *
import ctypes


class ponto(Structure):
    _fields_=[("x",c_int),("y",c_int),("z",c_int)]

l=CDLL("/home/balhau/workspace/cpplib/target/libcpplib.so");
cpuinfo=getattr(l, "cpuinfo")
l.cpuinfo(1);
print l.eax()
soma=l.somaPonto
soma.restype=ponto
p1=ponto(3,2,3)
p2=ponto(3,3,5)
p3=soma(p1,p2)
print p3.x,p3.y,p3.z
