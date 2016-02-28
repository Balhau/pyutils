'''
Created on 2 de Fev de 2014

@author: balhau
'''


def log(f):
    def inner(args):
        print "Function: "+str(f)+" called"
        res=f(args)
        print "Function ended"
        return res;
    return inner

@log
def ex1(args):
    print args

@log
def ex2(args):
    print args
    
ex1("ola mundo")
ex2("HELLO")
