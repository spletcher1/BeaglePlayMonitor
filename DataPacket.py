from Enums import DATAPACKETTYPE

class DataPacket:
  
    def __init__(self,data,sender):
        self.freedomID=0
        self.address = ""
        self.thirdInt=0
        self.lastInt=0
        self.temperature=0.0
        self.humidity=0.0
        self.lux=0.0

        self.address = sender[0]
        self.freedomID=sender[1]
        self.thirdInt=sender[2]
        self.lastInt=sender[3]

        ## Now parse the data which seems to be a string
        ## of ascii characters
        dataString = data.decode("utf-8")

        databits=dataString.split(';')
        if(len(databits)==2):
            tmp = databits[0].split(':')
            self.lux = float(tmp[1])
            self.temperature=-1.0
            self.humidity = -1.0
            self.packetType = DATAPACKETTYPE.LUX
            ## This is a lux packet
        elif(len(databits)==3):
             ## This is a temp humidity packet
            tmp = databits[0].split(':')
            self.humidity = float(tmp[1])
            tmp = databits[1].split(':')
            self.temperature = float(tmp[1])
            self.packetType = DATAPACKETTYPE.TEMPHUMID
            self.lux=-1.0
        else:
            self.temperature=-1.0
            self.humidity=-1.0
            self.lux=-1.0
            self.packetType = DATAPACKETTYPE.NONE
            ## Nonsense packet

    def __str__(self):
        if(self.packetType==DATAPACKETTYPE.TEMPHUMID):
            s = "\nFreedom: " + str(self.freedomID) +"\n" + "Temp: " + str(self.temperature) +"\n" + "Humid: " + str(self.humidity) +"\n"
        elif(self.packetType==DATAPACKETTYPE.LUX):
            s = "\nFreedom: " + str(self.freedomID) +"\n" + "LUX: " + str(self.lux)
        else:
            s="\nUnkown packetType."
        return s
    
