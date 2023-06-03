import DataPoint

class Freedom:
    def __init__(self,id):        
        self.ID=id     
        self.currentTemperature=0.0
        self.currentHumidity=0.0
        self.currentLUX=0.0
        self.lastDataPoint = DataPoint(0,-1,-1,-1)
        self.theData=[]           

                

    def AddData(self,packet):
        if(packet.freedomID==self.ID):
            if(packet.temperature>=0):
                self.lastDataPoint.Temperature = packet.temperature
                self.currentTemperature = packet.temperature
            if(packet.humidity>=0):
                self.lastDataPoint.Humidity = packet.humidity
                self.currentHumidity = packet.humidity
            if(packet.lux>=0):
                self.lastDataPoint.LUX = packet.lux
                self.currentLUX = packet.lux

            if(self.lastDataPoint.IsComplete):  
                self.lastDataPoint.Time=packet.time
                self.theData.append(self.lastDataPoint)
                self.lastDataPoint = DataPoint(0,-1,-1,-1)
                            




    def __str__(self):
        return "Freedom: " + str(self.ID) + "--" +str(self.currentTemperature)+"   "+ str(self.currentHumidity)+"   "+ str(self.currentLUX)