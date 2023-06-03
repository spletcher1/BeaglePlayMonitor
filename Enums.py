from enum import Enum

class STATUSREQUESTTYPE(Enum):
    LATESTONLY=1
    NORMAL=2

class COMMANDTYPE(Enum):    
    STOP_READING=1
    PAUSE_READING=2
    RESUME_READING=3
    RESET_COUNTER=4
    CLEAR_DATAQ=5
    CLEAR_DATAMESSQ=6
    SET_VERBOSE=7
    CLEAR_VERBOSE=8
    SET_STARTTIME=9    
    SET_GET_LATESTSTATUS=10
    SET_GET_NORMALSTATUS=11
    
class CURRENTSTATUS(Enum):
    READING=1
    RECORDING=2
    ERROR=3
    MISSING=4
    UNDEFINED=5

class PASTSTATUS(Enum):
    ALLCLEAR=1
    PASTERROR=2
    
class REPORTEDERRORSTATUS(Enum):
    CURRENT=1
    PAST=2
    NEVER=3

class PROCESSEDPACKETRESULT(Enum):
    WRONGID=1
    CHECKSUMERROR=2
    WRONGNUMBYTES=3
    NOANSWER=4
    INCOMPLETEPACKET=5
    OKAY=6

class DATAPACKETTYPE(Enum):
    LUX=1
    TEMPHUMID=2
    NONE=3