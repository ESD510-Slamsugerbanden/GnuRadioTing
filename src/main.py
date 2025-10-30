from Rotax import ez_comm #Uart controller for the motor
from beacon_serde import Beacon_decoder








if __name__ == "__main__":
    tarm = ez_comm("/dev/ttyUSB0")
    
    