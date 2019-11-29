import socket
import select
import sys
from time import sleep

class MQTT:    
    def __init__(self):
        self.__mqttUsername = ""
        self.__mqttPassword = ""
        self.__mqttClient = ""
        self.__mqttProtocol = "MQIsdp"
        self.__mqttLvl = 0x03
        self.__mqttFlags = 0xC2
        self.__mqttQOS = 0x00
        self.__mqttPacketID = 0x0001
        self.__mqttKeepAlive = 60
        self.__timeOutReceive = 1 #in seconds
        self.__Connect = False
        self.__mqtthost = None
        self.__mqttPort = 0
        self.ip = None

    def setUsername(self,userName):
        self.__mqttUsername = userName

    def setClientID(self,ID):
        self.__mqttClient = ID

    def setHost(self,host):
        self.__mqtthost = host

    def setPassword(self,password):
        self.__mqttPassword = password

    def setPort(self,port):
        self.__mqttPort = port

    def setTimeOutReceiveData(self, s):
        self.__timeOutReceive = s

    def publish(self, mqttTopic, payload):
        dataOutput = "30"
        data = "{}{}".format(mqttTopic,payload)
        X = len(data) + 2
        
        while True:
            encodeByte = X % 128
            
            X = X / 128
            if X >= 1:
                encodeByte = encodeByte | 128
            
            c = ""
            if encodeByte > 15:
                c = "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
            
            else:
                c = "0"
                c += "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
            
            dataOutput += c
            if X < 1:
                break
        a = self.__intToHex((len(mqttTopic) & 0xF000) >> 16)
        b = self.__intToHex((len(mqttTopic) & 0x0F00) >> 8)
        c = self.__intToHex((len(mqttTopic) & 0x00F0) >> 4)
        d = self.__intToHex((len(mqttTopic) & 0x000F))
        e = "{}{}{}{}{}".format(a,b,c,d,self.__stringToHex(data))
        dataOutput += e		
        message = bytes.fromhex(dataOutput)
        if(self.__Connect):
            try:
                self.s.send(message)
                return True
            except:
                return False
        else:
            return False

    def connect(self,host = None, port = None):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host != None and port != None:
            self.__mqtthost = host
            self.__mqttPort = port

        if self.__mqttPort == 0 or self.__mqtthost == None:
            return False

        print(self.__mqtthost)
        print(self.__mqttPort)

        if(type(self.__mqtthost) == int):
            self.ip = self.__mqtthost
        else:
            self.ip = socket.gethostbyname(self.__mqtthost)
            print(self.ip)
        try:
            self.s.connect((self.ip, self.__mqttPort))
            self.__Connect = True
            return True
        except:
            return False

    def __intToHex(self,Int):
	    return hex(Int).lstrip("0x").rstrip("L") or "0"
	
    def __stringToHex(self,str):
        x = len(str)
        sstr = ""
        for i in range(x):
            sstr += hex(ord(str[i])).lstrip("0x").rstrip("L") or "0"
        return sstr
    
    def close(self):
        self.__Connect = False
        self.s.close()

    def connectionPacket(self):
        dataOutput = ""
        dataOutput += "10"
        X = len(self.__mqttUsername)+len(self.__mqttPassword)+len(self.__mqttProtocol)+len(self.__mqttClient)+12
        
        while True:
            encodeByte = X % 128
            
            X = X / 128
            if X >= 1:
                encodeByte = encodeByte | 128
            
            c = ""
            if encodeByte > 15:
                c = "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
            
            else:
                c = "0"
                c += "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
            
            dataOutput += c
            if X < 1:
                break
                
        a = self.__intToHex((len(self.__mqttProtocol) & 0xF000) >> 16)
        b = self.__intToHex((len(self.__mqttProtocol) & 0x0F00) >> 8)
        c = self.__intToHex((len(self.__mqttProtocol) & 0x00F0) >> 4)
        d = self.__intToHex((len(self.__mqttProtocol) & 0x000F))
        e = "{}{}{}{}{}".format(a,b,c,d,self.__stringToHex(self.__mqttProtocol))
        dataOutput += e
        c = "{}{}".format(self.__intToHex((self.__mqttLvl & 0xF0) >> 4), self.__intToHex(self.__mqttLvl  & 0x0F))
        dataOutput += c	
        c = "{}{}".format(self.__intToHex((self.__mqttFlags & 0xF0) >> 4), self.__intToHex(self.__mqttFlags  & 0x0F))
        dataOutput += c	
        a = self.__intToHex((self.__mqttKeepAlive& 0xF000) >> 16)
        b = self.__intToHex((self.__mqttKeepAlive & 0x0F00) >> 8)
        c = self.__intToHex((self.__mqttKeepAlive & 0x00F0) >> 4)
        d = self.__intToHex((self.__mqttKeepAlive& 0x000F))
        e = "{}{}{}{}".format(a,b,c,d)
        dataOutput += e
        a = self.__intToHex((len(self.__mqttClient) & 0xF000) >> 16)
        b = self.__intToHex((len(self.__mqttClient) & 0x0F00) >> 8)
        c = self.__intToHex((len(self.__mqttClient) & 0x00F0) >> 4)
        d = self.__intToHex((len(self.__mqttClient) & 0x000F))
        e = "{}{}{}{}{}".format(a,b,c,d,self.__stringToHex(self.__mqttClient))
        dataOutput += e
        a = self.__intToHex((len(self.__mqttUsername) & 0xF000) >> 16)
        b = self.__intToHex((len(self.__mqttUsername) & 0x0F00) >> 8)
        c = self.__intToHex((len(self.__mqttUsername) & 0x00F0) >> 4)
        d = self.__intToHex((len(self.__mqttUsername) & 0x000F))
        e = "{}{}{}{}{}".format(a,b,c,d,self.__stringToHex(self.__mqttUsername))
        dataOutput += e
        a = self.__intToHex((len(self.__mqttPassword) & 0xF000) >> 16)
        b = self.__intToHex((len(self.__mqttPassword) & 0x0F00) >> 8)
        c = self.__intToHex((len(self.__mqttPassword) & 0x00F0) >> 4)
        d = self.__intToHex((len(self.__mqttPassword) & 0x000F))
        e = "{}{}{}{}{}".format(a,b,c,d,self.__stringToHex(self.__mqttPassword))
        dataOutput += e
        message = bytes.fromhex(dataOutput)
        if(self.__Connect):
            try:
                self.s.send(message)
                return True
            except:
                return False
        else:
            return False

    def subscribe(self,mqttTopic):
        dataOutput = "82"
        topicLength = len(mqttTopic)
        X = topicLength + 5

        while True:
            encodeByte = X % 128
            
            X = X / 128
            if X >= 1:
                encodeByte = encodeByte | 128
            
            c = ""
            if encodeByte > 15:
                c = "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
            
            else:
                c = "0"
                c += "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
            
            dataOutput += c
            if X < 1:
                break
        
        a = self.__intToHex((self.__mqttPacketID & 0xF000) >> 16)
        b = self.__intToHex((self.__mqttPacketID & 0x0F00) >> 8)
        c = self.__intToHex((self.__mqttPacketID & 0x00F0) >> 4)
        d = self.__intToHex((self.__mqttPacketID & 0x000F))
        e = "{}{}{}{}".format(a,b,c,d)
        dataOutput += e	
        a = self.__intToHex((len(mqttTopic) & 0xF000) >> 16)
        b = self.__intToHex((len(mqttTopic) & 0x0F00) >> 8)
        c = self.__intToHex((len(mqttTopic) & 0x00F0) >> 4)
        d = self.__intToHex((len(mqttTopic) & 0x000F))
        e = "{}{}{}{}{}".format(a,b,c,d,self.__stringToHex(mqttTopic))
        dataOutput += e	
        dataOutput += self.__intToHex((self.__mqttQOS & 0xF0) >> 4)
        dataOutput += self.__intToHex((self.__mqttQOS & 0x0F))
        message = bytes.fromhex(dataOutput)
        if(self.__Connect):
            try:
                self.s.send(message)
                return True
            except:
                return False
        else:
            return False

    def receiveData(self):
        response = ""
        data = ""
        self.s.settimeout(self.__timeOutReceive)
        try:
            response = self.s.recv(300)
            data = response.decode('UTF-8')
        except:
            data = "none"
        self.s.settimeout(None)
        if data == "none":
            return data
        elif len(data)>4:
            return data[4:]

    def checkConnection(self):
        result = self.s.connect_ex((self.ip,self.port))
        if result == 0:
            return False
        else:
            return True

if __name__ == "__main__":
    Host = "tailor.cloudmqtt.com"
    Port = 15715
    #"cyvtuetu","B3i7k9kX86pJ","ABCDEF"
    mqtt = MQTT()
    mqtt.setClientID("ABCDEF")
    mqtt.setHost(Host)
    mqtt.setPort(Port)
    mqtt.setPassword("B3i7k9kX86pJ")
    mqtt.setUsername("cyvtuetu")
    mqtt.connect()
    sleep(2)
    mqtt.connectionPacket()
    sleep(2)
    mqtt.subscribe("aaa")
    sleep(2)
    
    for i in range(5):
        i = mqtt.publish("aaa",12)
        if i:
            print("ok")
        else:
            print("false")
        print(mqtt.receiveData())
        sleep(2)

    mqtt.close()
    