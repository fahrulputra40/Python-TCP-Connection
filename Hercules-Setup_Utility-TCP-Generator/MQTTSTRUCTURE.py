MQTTHOST = "tailor.cloudmqtt.com"
MQTTPORT = 15715
MQTTCLIENT = "ABCDEF"
MQTTTOPIC = "ddddd"
MQTTPROTOCOLNAME = "MQIsdp"
MQTTLVL = 3
MQTTFLAGS = 0xC2
MQTTKEEPALIVE = 60
MQTTUSERNAME = "cyvtuetu"
MQTTPASSWORD = "B3i7k9kX86pJ"
MQTTOS = 0
MQTTPACKETID = 1
MQTTPAYLOAD= "45"

















dataOutput = ""

def stringToHex(str):
	x = len(str)
	sstr = ""
	for i in range(x):
		sstr += hex(ord(str[i])).lstrip("0x").rstrip("L") or "0"
	return sstr

def intToHex(Int):
	return hex(Int).lstrip("0x").rstrip("L") or "0"
	
def connectionPacket():
	global dataOutput
	dataOutput += "10"
	#+len(MQTTCLIENT)
	X = len(MQTTUSERNAME)+len(MQTTPASSWORD)+len(MQTTPROTOCOLNAME)+len(MQTTCLIENT)+12
	
	while True:
		encodeByte = X % 128
		
		X = X / 128
		if X >= 1:
			encodeByte = encodeByte | 128
		
		c = ""
		if encodeByte > 9:
			c = "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
		
		else:
			c = "0"
			c += "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
		
		dataOutput += c
		if X < 1:
			break
			
	a = intToHex((len(MQTTPROTOCOLNAME) & 0xF000) >> 16)
	b = intToHex((len(MQTTPROTOCOLNAME) & 0x0F00) >> 8)
	c = intToHex((len(MQTTPROTOCOLNAME) & 0x00F0) >> 4)
	d = intToHex((len(MQTTPROTOCOLNAME) & 0x000F))
	e = "{}{}{}{}{}".format(a,b,c,d,stringToHex(MQTTPROTOCOLNAME))
	dataOutput += e
	c = "{}{}".format(intToHex((MQTTLVL & 0xF0) >> 4), intToHex(MQTTLVL  & 0x0F))
	dataOutput += c	
	c = "{}{}".format(intToHex((MQTTFLAGS & 0xF0) >> 4), intToHex(MQTTFLAGS  & 0x0F))
	dataOutput += c	
	a = intToHex((MQTTKEEPALIVE& 0xF000) >> 16)
	b = intToHex((MQTTKEEPALIVE & 0x0F00) >> 8)
	c = intToHex((MQTTKEEPALIVE & 0x00F0) >> 4)
	d = intToHex((MQTTKEEPALIVE& 0x000F))
	e = "{}{}{}{}".format(a,b,c,d)
	dataOutput += e
	a = intToHex((len(MQTTCLIENT) & 0xF000) >> 16)
	b = intToHex((len(MQTTCLIENT) & 0x0F00) >> 8)
	c = intToHex((len(MQTTCLIENT) & 0x00F0) >> 4)
	d = intToHex((len(MQTTCLIENT) & 0x000F))
	e = "{}{}{}{}{}".format(a,b,c,d,stringToHex(MQTTCLIENT))
	dataOutput += e
	a = intToHex((len(MQTTUSERNAME) & 0xF000) >> 16)
	b = intToHex((len(MQTTUSERNAME) & 0x0F00) >> 8)
	c = intToHex((len(MQTTUSERNAME) & 0x00F0) >> 4)
	d = intToHex((len(MQTTUSERNAME) & 0x000F))
	e = "{}{}{}{}{}".format(a,b,c,d,stringToHex(MQTTUSERNAME))
	dataOutput += e
	a = intToHex((len(MQTTPASSWORD) & 0xF000) >> 16)
	b = intToHex((len(MQTTPASSWORD) & 0x0F00) >> 8)
	c = intToHex((len(MQTTPASSWORD) & 0x00F0) >> 4)
	d = intToHex((len(MQTTPASSWORD) & 0x000F))
	e = "{}{}{}{}{}".format(a,b,c,d,stringToHex(MQTTPASSWORD))
	dataOutput += e
	print("dataLength: {}\n".format(len(dataOutput)))
	return dataOutput
	
def sendPacketData(value):
	global dataOutput
	dataOutput = "30"
	data = "{}{}".format(MQTTTOPIC,value)
	X = len(data) + 2
	topicLength = len(MQTTTOPIC)
	
	while True:
		encodeByte = X % 128
		
		X = X / 128
		if X >= 1:
			encodeByte = encodeByte | 128
		
		c = ""
		if encodeByte > 9:
			c = "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
		
		else:
			c = "0"
			c += "{}".format(hex(encodeByte).lstrip("0x").rstrip("L") or "0")
		
		dataOutput += c
		if X < 1:
			break
	a = intToHex((len(MQTTTOPIC) & 0xF000) >> 16)
	b = intToHex((len(MQTTTOPIC) & 0x0F00) >> 8)
	c = intToHex((len(MQTTTOPIC) & 0x00F0) >> 4)
	d = intToHex((len(MQTTTOPIC) & 0x000F))
	e = "{}{}{}{}{}".format(a,b,c,d,stringToHex(data))
	dataOutput += e		
	#dataOutput += intToHex((MQTTOS & 0xF0) >> 4)
	#dataOutput += intToHex((MQTTOS & 0x0F))
	return dataOutput
	
def subscribePacketData():
	global dataOutput
	dataOutput = "82"
	
	X = 5 + len(MQTTTOPIC)
	print("len: {}".format(X))
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
	
	a = intToHex((MQTTPACKETID & 0xF000) >> 16)
	b = intToHex((MQTTPACKETID & 0x0F00) >> 8)
	c = intToHex((MQTTPACKETID & 0x00F0) >> 4)
	d = intToHex((MQTTPACKETID & 0x000F))
	e = "{}{}{}{}".format(a,b,c,d)
	dataOutput += e	
	a = intToHex((len(MQTTTOPIC) & 0xF000) >> 16)
	b = intToHex((len(MQTTTOPIC) & 0x0F00) >> 8)
	c = intToHex((len(MQTTTOPIC) & 0x00F0) >> 4)
	d = intToHex((len(MQTTTOPIC) & 0x000F))
	e = "{}{}{}{}{}".format(a,b,c,d,stringToHex(MQTTTOPIC))
	dataOutput += e	
	dataOutput += intToHex((MQTTOS & 0xF0) >> 4)
	dataOutput += intToHex((MQTTOS & 0x0F))
	return dataOutput
	
	
	
	
print("Connection PacketData: \n{}".format(connectionPacket()))
print("send PacketData: \n{}".format(sendPacketData(MQTTPAYLOAD)))
print("Subscribe PacketData: \n{}".format(subscribePacketData()))



