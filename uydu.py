#!/usr/bin/env python
#
#Baris DINC - TA7W - June 2017
#
#TODO : Add frequency change over HamLib or directly for Kenwood TS2000
#TODO : Add PTT keying for QRO operation
#

#imports section
import serial


mycall="TA7W  " #...... for BeEagleSAT and ...... for HavelSAT (SSIDs is 0)
stcall="ON02TR" #ON01TR for BeEagleSAT and ON02TR for HavelSAT (SSIDs is 1)
hasModem=True   #Do you have a modem connected : Ture/False 
modem_port ="/dev/ttyUSB0"
modem_speed=38400
modem_kiss ="1B 40 4B" #ESC@K
hasRadio=False  #Do you have a radio connected : True/False
radio_port="/dev/ttyUSB1"
radio_speed=9600
radio_command="" #insert command for Frequency change

###SETTINGS for SCS Modem
#
# Set flow-control (Hardware flow-control, no XON/XOFF)
#Z0
# Disable echoing of commands
#E0
# Misc
#X1  # Enable the PTT line
#W0  # Minimize the slottime
#T100 # Set the TX-Delay to x*10ms
# Configuration of specific TNC functions
#@D0 # Set full duplex transmission
#@F1 # Send flags during pauses
# Configuration of the Packet-Radio Mode
#%B9600 
# Disable TX frequency tracking (should not apply at 1200bps anyway)
#%T0
# AFSK amplitude %XA[30-30000] mV
#%XA2400
# All modulations amplitude %X[30-30000] mV
#%X9000
# Switch to KISS Mode
#@K
#C0 00 9E 9C 60 64 A8= A4 60 A8 82 64 9E 94 82 61 03 F0 DB DC 18 0A CA 26 00 05 19 08 01 60 B8 33 C0 
lookUpTable=[] #Array for CCIT CRC16 syndrome
dataToSend=[]  #Data to be send out to modem
if hasModem: modemPort=serial.Serial()
if hasRadio: radioPort=serial.Serial()


def CRC_Init():
#prepares the CCIT lookUpTable[]
    for i in range(256):
	tmp=0
	if (i & 1)   !=0: tmp = tmp ^ 0x1021
	if (i & 2)   !=0: tmp = tmp ^ 0x2042
	if (i & 4)   !=0: tmp = tmp ^ 0x4084
	if (i & 8)   !=0: tmp = tmp ^ 0x8108
	if (i & 16)  !=0: tmp = tmp ^ 0x1231
	if (i & 32)  !=0: tmp = tmp ^ 0x2462
	if (i & 64)  !=0: tmp = tmp ^ 0x48C4
	if (i & 128) !=0: tmp = tmp ^ 0x9188
	lookUpTable.append(tmp)
    return
def calc_csum():
    #Do CheckSum calculations
    #TODO

    return 0

def About():
    print "QB50 uplink tester..... by TA7W"
    return

def doChecks():
    retVal = []
    if len(mycall) !=6: retVal.append("source Callsign (mycall) must be 6 characters long... If not please fill with spaces.")
    if len(stcall) !=6: retVal.append("Destionation Callsign (stcall) must be 6 characters long... If not please fill with spaces.")
    return retVal
	
def putKISS():
    #Put modem into kiss mode
    #TODO


    return

def prepareHeader():
    #Prepare the header of the AX25 message
    dataToSend.append(0xC0) #first char FEND for KISS data start
    dataToSend.append(0x00) #kiss ode data identifier
    for data in stcall: dataToSend.append(2*ord(data))
    dataToSend.append(96) #append -0 as SSID
    for data in mycall: dataToSend.append(2*ord(data))
    dataToSend.append(97) #append -1 as SSID
    dataToSend.append(3)  #append 3 as FLAG
    dataToSend.append(240)#append F0 as protocol identifier
    dataToSend.append(219)#append DB : this is the ESCAPE character .. we want to send C0 as data start... DB DC replaces C0
    dataToSend.append(220)#append DC : look remarks of previous byte
    dataToSend.append(24) #append 18 : don't know the meaning yet  
    dataToSend.append(10) #append 0A : don't know the meaning yet

    return


def preparePayload():
    #Prepare the payload of the AX25 message
    #TODO: This is only for GET MODE... extend it for other commands
    dataToSend.append(0) # 0x00 0x05 0x019 0x08 0x01 0x60 
    dataToSend.append(5) 
    dataToSend.append(25)
    dataToSend.append(8) 
    dataToSend.append(1) 
    dataToSend.append(96) 

    return
def prepareCSUM():
    #Prepare the CSUM for the payload
    dataToSend.append(255) 
    dataToSend.append(255) 

    return

def prepareFooter():
    #Prepare the footer of the AX25 message
    dataToSend.append(192) #append C0 : last character for KISS data end
    return

def main():
    About()    #print header ads
    retVal=doChecks() #do definition checks
    if len(retVal)!=0:
	for Message in retVal: print "ERROR: ",Message
	return 0
    CRC_Init() #prepare the lookup table
    prepareHeader()   #prepare the first part of AX25 message

    preparePayload()  #prepare the payload part
    #TODO calculate the checksum here
    prepareCSUM()
    prepareFooter()
    print dataToSend

if __name__ == '__main__':
    main()




