from multiprocessing import Queue, Process
import queue
import datetime
import math
import time
import sys
from Enums import COMMANDTYPE
import socket
import struct
import DataPacket

class MP_Message:
    def __init__(self,message):
        self.time = datetime.datetime.today()
        self.message=message

class MP_Command:
    def __init__(self,ctype,arg):
        self.commandType = ctype
        self.arguments=arg
    def __str__(self):
        return str(self.commandType) + ":" + str(self.arguments)


class DataGetter:
    def __init__(self):                  
        self.message_q=Queue()
        self.command_q=Queue()               
        self.answer_q=Queue()      
        self.data_q=Queue()          
        self.verbose=False
        self.theReader=None                
        self.startTime = datetime.datetime.today()
        self.currentReadIndex=1
        self.continueRunning = False
        self.isPaused = False        
        self.InitializeCommunication()
        self.theReader = Process(target=self.ReadWorker)
        self.theReader.start()
        self.QueueMessage("Reader started.")     
    
                         
    def InitializeCommunication(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        print("Initializing Data Getter Communication")
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
        self.sock.bind(('', 9999))
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::1"), (chr(0) * 16).encode('utf-8'))
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
        print("Done")  
    
    def StopReading(self):   
        self.QueueMessage("Reader termination requested.")         
        self.command_q.put(MP_Command(COMMANDTYPE.STOP_READING,''))              \
   
    def ClearQueues(self):
        self.command_q.put(MP_Command(COMMANDTYPE.CLEAR_DATAMESSQ,''))
    def PauseReading(self):
        self.command_q.put(MP_Command(COMMANDTYPE.PAUSE_READING,''))
    def ResumeReading(self):
        self.command_q.put(MP_Command(COMMANDTYPE.RESUME_READING,''))
    def StartReading(self):        
        self.command_q.put(MP_Command(COMMANDTYPE.PAUSE_READING,''))
        self.command_q.put(MP_Command(COMMANDTYPE.CLEAR_DATAMESSQ,''))
        self.command_q.put(MP_Command(COMMANDTYPE.RESET_COUNTER,''))
        self.command_q.put(MP_Command(COMMANDTYPE.RESUME_READING,''))      
    def SetStartTime(self):
        self.command_q.put(MP_Command(COMMANDTYPE.SET_STARTTIME,[datetime.datetime.today()]))
                  
    #endregion   

    def ClearAnswerQueueInternal(self):
        try:
            while True:
                self.answer_q.get_nowait()
        except queue.Empty:
            pass        
        
    def ClearQueuesInternal(self):
        try:
            while True:
                self.message_q.get_nowait()
        except queue.Empty:
            pass
        try:
            while True:
                self.data_q.get_nowait()
        except queue.Empty:
            pass       
        try:
            while True:
                self.answer_q.get_nowait()
        except queue.Empty:
            pass        
        
    def ProcessCommand(self):        
        try:            
            tmp=self.command_q.get(False)           
        except:          
            return False        
        if (tmp is not None):  
            #print(tmp)          
            if(tmp.commandType==COMMANDTYPE.STOP_READING):                            
                self.isPaused=True
            elif(tmp.commandType==COMMANDTYPE.PAUSE_READING):                    
                self.isPaused=True
            elif(tmp.commandType==COMMANDTYPE.RESUME_READING):                    
                self.isPaused=False            
            elif(tmp.commandType==COMMANDTYPE.RESET_COUNTER):                    
                self.currentReadIndex=1                           
            elif(tmp.commandType==COMMANDTYPE.CLEAR_DATAMESSQ):
                self.ClearQueuesInternal()                                        
            elif(tmp.commandType==COMMANDTYPE.SET_VERBOSE):
                self.verbose=True
            elif(tmp.commandType==COMMANDTYPE.CLEAR_VERBOSE):
                self.verbose=False   
            elif(tmp.commandType==COMMANDTYPE.SET_STARTTIME):
                self.startTime=tmp.arguments[0]                                 
            else:
                print("Unknown Command")
                return False 
        else:
            return False
        return True

    def ReadWorker(self):
        self.currentReadIndex=1        
        CommandsInARow=0
        self.isPaused=True      
        self.QueueMessage("Read worker started.")   
        print("Read worker started.")                  
        while(True):  
            if(CommandsInARow>12 or self.ProcessCommand()==False):                                   
                CommandsInARow=0
                if(self.isPaused==False):                   
                    self.ReadValues()                                                                                                                                                               
            else:
                CommandsInARow+=1
            time.sleep(0.002)
        self.QueueMessage("Read worker ended.")                
        print("Read workder ended.")
        return
    
    def ReadValues(self): 
        currentTime = datetime.datetime.today()                          
        data, sender = self.sock.recvfrom(1024)
        packet=DataPacket.DataPacket(data,sender)
        print(packet)
        #self.data_q.put(packet)     
        #print (str(sender) + '  ' + repr(data))   
        
        #for info in self.focalFreedoms:
        #    try:                                       
        #        data, sender = sock.recvfrom(1024)
        #        print (str(sender) + '  ' + repr(data))                    
        #    except:                        
        #        ss = "Get status exception (" + str(info.ID) +")."                                
        #        self.QueueMessage(ss)
        #    time.sleep(0.002)        

    def QueueMessage(self,message):
        if(self.verbose and self.message_q.qsize()<1000):
            self.message_q.put(MP_Message(message))

    def QueueCommand(self,command):        
        self.command_q.put(command)
        if(self.verbose):
            ss = "Command queued (" + str(command.arguments[0])+"): " +str(command.commandType)
            self.QueueMessage(ss)              

def ModuleTest():
    mp=DataGetter()
    mp.StartReading()
    
    

if __name__=="__main__" :
    ModuleTest()
    