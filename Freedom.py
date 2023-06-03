class Freedom:
     def __init__(self,id,mp):
        self.MP = mp
        self.ID=id     
        self.currentTemperature=0.0
        self.currentHumidity=0.0
        self.currentLUX=0.0


    def __str__(self):
        return "Freedom: " + str(self.ID) + "--" +str(self.currentTemperature)+"   "+ str(self.currentHumidity)+"   "+ str(self.currentLUX)