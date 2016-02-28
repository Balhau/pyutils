# -*- coding: utf-8 -*-
'''
Created on 3 de Fev de 2013
Modulo para efectuar o download de dados do protal Base com os gastos publicos
@author: balhau
'''
import httplib,urllib
import simplejson
import mysql
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

class Base:
    #URLs Information
    HOST_BASE="www.base.gov.pt"
    URL_BASE="http://www.base.gov.pt/base2/html/pesquisas/contratos.shtml?tipo="
    URL_REFERER_AJUSTES_DIRECTOS=URL_BASE+"1"
    URL_REFERER_CONTRATOS=URL_BASE+"2"
    URL_REST_AJUSTES_DIRECTOS="/base2/rest/contratos?tipo=2&sort(-publicationDate)"
    URL_REST_CONTRATOS="/base2/rest/contratos?tipo=1&sort(-publicationDate)"
    MYSQL_CREATE_TABLE_QUERY="CREATE TABLE `base_data` (\
                            `id` INTEGER DEFAULT NULL ,\
                            `contracted` VARCHAR(200) DEFAULT NULL ,\
                            `contracting` VARCHAR(200) DEFAULT NULL ,\
                            `initialContractualPrice` FLOAT DEFAULT 0 ,\
                            `objectBriefDescription` VARCHAR(200) DEFAULT NULL ,\
                            `publicationDate` DATE DEFAULT NULL ,\
                            `signingDate` DATE DEFAULT NULL,\
                            `typeContract` int(11) DEFAULT NULL\
                        );"
    
    #MySQL Database Configurations
    MYSQL_USER_DB="root"
    MYSQL_USER_PASSWORD="gamma007"
    MYSQL_DATABASE_NAME="basePublicData"
    MYSQL_TABLE_NAME="base_data"
    MYSQL_HOST_NAME="localhost"
    MYSQL_HOST_PORT=3306
    
    TIPO_CONTRATO=1
    TIPO_AJUSTE_DIRECTO=2
    
    
    def makeHeaders(self,referer,start,end):
        headers={
                 "Accept":"application/javascript, application/json",
                 "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3",
                 "Accept-Language":"pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4",
                 "Connection":"close",
                 "Content-Type":"application/x-www-form-urlencoded",
                 "Cookie":"fontSize=small_font",
                 "Host":"www.base.gov.pt",
                 "Range":"items="+str(start)+"-"+str(end),
                 "Referer":referer,
                 "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11",
                 "X-Requested-With":"XMLHttpRequest"
                 }
        return headers
    
    def urlFromTipo(self,tipo):
        if tipo == Base.TIPO_CONTRATO:
            return Base.URL_REST_CONTRATOS
        if tipo == Base.TIPO_AJUSTE_DIRECTO:
            return Base.URL_REST_AJUSTES_DIRECTOS
    
    def getData(self,init,end,tipo):
        headers=self.makeHeaders(Base.URL_REFERER_CONTRATOS, init, end)
        conn=httplib.HTTPConnection(Base.HOST_BASE)
        conn.request("GET", self.urlFromTipo(tipo), "", headers)
        response=conn.getresponse()
        return response.read()
    
    
    
    def base2mysql(self,tipo,batchsize=100):
        step=batchsize
        start=0
        end=batchsize-1
        data=simplejson.loads(self.getData(start,end,tipo))
        while len(data)>0:
            #print data
            start+=batchsize
            end+=batchsize
            data=simplejson.loads(self.getData(start,end,tipo))
            self.__insertBatch(tipo,data)
        
    
    def __insertBatch(self,tipo,json_array):
        def s(str):
            return str.replace("\"", "\\\"")
        def m(money):
            return money.replace(".","").replace(",",".").replace("€","").replace(" ","")
        query="INSERT INTO "+Base.MYSQL_TABLE_NAME
        query+=" VALUES "
        try:
            for i in range(0,len(json_array)):
                jso=json_array[i]
                if i != 0:
                    query+=","
                query+="("
                query+=str(jso["id"])+",\""+s(jso["contracted"])+"\",\""
                query+=s(jso["contracting"])+"\","+m(jso["initialContractualPrice"])+",\""
                query+=s(jso["objectBriefDescription"])+"\",\""
                query+=self._formatData(jso["publicationDate"])+"\",\""
                query+=self._formatData(jso["signingDate"])+"\","
                query+=str(tipo)
                query+=")"
            con=self.createConn()
            cur=con.cursor()
            cur.execute(query)
            con.commit()
            con.close()
            print query
        except:
            print query 
    
    def _formatData(self,data):
        return "-".join(data.split("-")[::-1])
    
    def createConn(self):
        con=MySQLConnection()
        con.connect(Base.MYSQL_DATABASE_NAME, Base.MYSQL_USER_DB, Base.MYSQL_USER_PASSWORD, Base.MYSQL_HOST_NAME, Base.MYSQL_HOST_PORT)
        return con
    
    def createTable(self):
        con=self.createConn()
        cur=con.cursor()
        cur.execute(Base.MYSQL_CREATE_TABLE_QUERY)
        con.close()

#Importar contratos
b=Base()
b.base2mysql(Base.TIPO_CONTRATO,1000)
b.base2mysql(Base.TIPO_AJUSTE_DIRECTO,1000)