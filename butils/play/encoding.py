import sys


def tostr(list):
    return "".join([chr(x) for x in list])

def utfy(offseta,string):
    offsetb=0x80-ord('a')
    g_letters =[tostr(offseta+[ord(l)+offsetb]) if(l!=' ') else ' ' for l in string.lower()]
    return "".join(g_letters)


#print tostr([0xcf,0x40])
print utfy([0xcf],"Hacking UTF eight")
print utfy([0xd5],"Deves ter a mania que es fixe")
print utfy([0xe3,0x82],"Eu gosto e do verao de passear com a piroca na mao")
print utfy([0xe2,0xb2],"Eu gosto muito de codigos")
print utfy([0xe2,0xb4],"Precos fantasticos na primark")
print utfy([0xe2,0xb0],"Poe tudo no minimo que fazes")
print utfy([0xf0,0x9f,0x80],"A minha mae de fato de treino")
print utfy([0xf0,0x90,0xa4],"Tu es rumbalibable")
print utfy([0xd5],"Hello World")
print utfy([0xde],"Hacking UTF eight")
print utfy([0xe2,0xb4],"Eu gosto imenso de couve de bruxelas")
