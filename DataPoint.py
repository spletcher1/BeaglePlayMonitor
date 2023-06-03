import datetime
class DataPoint:
    def __init__(self,temp,humid,lux):        
        self.Time=datetime.now()
        self.Temperature = temp
        self.Humidity=humid
        self.LUX=lux

    def IsComplete(self):
        if(self.Temperature == -1.0 or self.Humidity == -1.0 or self.LUX == -1.0):
            return False
        return True