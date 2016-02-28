'''
Created on 8 de Nov de 2012
Cracker para passwords thompson..
@author: balhau
'''

import hashlib


def createDic():
    letters=[chr(ch) for ch in range(ord('A'),ord('Z')+1)]
    nums=[num for num in range(10)]
    alpha=letters+nums
    alpha=[str(ch) for ch in alpha]
    dic=[]
    for letter1 in alpha:
        for letter2 in alpha:
            for letter3 in alpha:
                dic.append(letter1+letter2+letter3)
    return dic

def prepWeek(week):
    if week<10:
        return "0"+str(week)
    return str(week)

def ascii2Hex(asc):
    strout=""
    for ch in asc:
        strout+="%x" % ord(ch)
    return strout

def genHashes(name):
    f=open(name,"w")
    years=["07","08","09","10"]
    weeks=[prepWeek(it) for it in range(0,53)]
    list=createDic()
    pref="CP"
    for year in years:
        for week in weeks:
            for item in list:
                m=hashlib.sha1()
                m.update("CP"+year+week+ascii2Hex(item))
                m.digest()
                sha1=m.hexdigest()
                f.write(sha1+"\n")
                
genHashes("hashes.dat")        