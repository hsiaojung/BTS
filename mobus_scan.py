'''
2018/09/25 made by Cyril Chang 
code for RS485 reader to BTS01 BAT monitor
v0.1
'''

import subprocess
import decimal
import re
import sys
from time import sleep

from threading import Thread
import os
import check


import sys, signal



def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



hostname = "8.8.8.8" #example

v1_index = 20
r1_indexh = 21
r1_indexl = 22
bvrctotal = 24

ti_index = 20
temp_index = 20
time_index = 20

parameter_vr = []
parameter_ti = []
parameter_ta = []


ticmd = ['mbpoll', '-1', '-P N', '-b 9600', '-a 247','-r 49', '-t 3:hex','-c 2','/dev/ttyUSB0']
testmd = ['mbpoll', '-1']
bvrcmd =  ['mbpoll','-1','-P N', '-b 9600', '-a 247', '-r 1', '-t 3:hex', '-c 24',  '/dev/ttyUSB0']
timecmd = ['mbpoll','-1','-P N', '-b 9600', '-a 247', '-r 81', '-t 3:hex', '-c 4',  '/dev/ttyUSB0']
btempcmd = ['mbpoll','-1','-P N', '-b 9600', '-a 247', '-r 17', '-t 3:hex', '-c 8',  '/dev/ttyUSB0']

# out_bytes = subprocess.call(cmd)
# out_bytes = response = subprocess.check_output(cmd, shell=True)
# out_bytes = response = subprocess.check_output(cmd2, shell=False)
# https://stackoverflow.com/questions/32942207/python-subprocess-calledprocesserror-command-returned-non-zero-exit-s

#  Python cookbook  https://python3-cookbook.readthedocs.io/zh_CN/latest/chapters/p02_strings_and_text.html
#  Python tutorial  http://www.runoob.com/python/python-tutorial.html
#  Python string:   https://www.tutorialspoint.com/python3/python_strings.htm

outbvr= b"mbpoll 1.4 - FieldTalk(tm) Modbus(R) Master Simulator\nCopyright \xc2\xa9 2015-2018 Pascal JEAN, https://github.com/epsilonrt/mbpoll\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type 'mbpoll -w' for details.\n\nProtocol configuration: Modbus RTU\nSlave configuration...: address = [247]\n                        start reference = 1, count = 24\nCommunication.........: /dev/ttyUSB1,       9600-8N1 \n                        t/o 1.00 s, poll rate 1000 ms\nData type.............: 16-bit register, input register table\n\n-- Polling slave 247...\n[1]: \t0x0002\n[2]: \t0x0000\n[3]: \t0x0000\n[4]: \t0x0002\n[5]: \t0x0000\n[6]: \t0x0000\n[7]: \t0x0002\n[8]: \t0x0000\n[9]: \t0x0000\n[10]: \t0x0002\n[11]: \t0x0000\n[12]: \t0x0000\n[13]: \t0x0002\n[14]: \t0x0000\n[15]: \t0x0000\n[16]: \t0x0001\n[17]: \t0x0000\n[18]: \t0x0000\n[19]: \t0x0002\n[20]: \t0x0000\n[21]: \t0x0000\n[22]: \t0x0002\n[23]: \t0x0000\n[24]: \t0x0000\n\n"
outtime = b"mbpoll 1.4 - FieldTalk(tm) Modbus(R) Master Simulator\nCopyright \xc2\xa9 2015-2018 Pascal JEAN, https://github.com/epsilonrt/mbpoll\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type 'mbpoll -w' for details.\n\nProtocol configuration: Modbus RTU\nSlave configuration...: address = [247]\n                        start reference = 81, count = 4\nCommunication.........: /dev/ttyUSB1,       9600-8N1 \n                        t/o 1.00 s, poll rate 1000 ms\nData type.............: 16-bit register, input register table\n\n-- Polling slave 247...\n[81]: \t0x07E1\n[82]: \t0x0103\n[83]: \t0x061B\n[84]: \t0x2000\n\n"
outbtemp = b"mbpoll 1.4 - FieldTalk(tm) Modbus(R) Master Simulator\nCopyright \xc2\xa9 2015-2018 Pascal JEAN, https://github.com/epsilonrt/mbpoll\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type 'mbpoll -w' for details.\n\nProtocol configuration: Modbus RTU\nSlave configuration...: address = [247]\n                        start reference = 17, count = 8\nCommunication.........: /dev/ttyUSB1,       9600-8N1 \n                        t/o 1.00 s, poll rate 1000 ms\nData type.............: 16-bit register, input register table\n\n-- Polling slave 247...\n[17]: \t0x0005\n[18]: \t0x0004\n[19]: \t0x0005\n[20]: \t0x0005\n[21]: \t0x0005\n[22]: \t0x0006\n[23]: \t0x0005\n[24]: \t0x0006\n\n"
outti = b"mbpoll 1.4 - FieldTalk(tm) Modbus(R) Master Simulator\nCopyright \xc2\xa9 2015-2018 Pascal JEAN, https://github.com/epsilonrt/mbpoll\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type 'mbpoll -w' for details.\n\nProtocol configuration: Modbus RTU\nSlave configuration...: address = [247]\n                        start reference = 49, count = 2\nCommunication.........: /dev/ttyUSB1,       9600-8N1 \n                        t/o 1.00 s, poll rate 1000 ms\nData type.............: 16-bit register, input register table\n\n-- Polling slave 247...\n[49]: \t0x0017\n[50]: \t0x0147\n\n"

def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except OSError:
        return False
    return 1


def readBTS():

   ret = 1
   ans = exists('/dev/ttyUSB0')

   if ans == 1:
        ret = 1
   else :
        print("Check ttyUSB0 !,it does not exist")
        os._exit(0)

        
   #process =  subprocess.Popen(ticmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   process =  subprocess.Popen(ticmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   returncode = process.wait()
   outti_485 = process.stdout.read().decode("utf-8")
   if outti_485.find("failed:") >= 0:
      ret = 0
   #outti_485 = process.stdout.read()    
   print ("outti_485=%s"%outti_485)

   
   process =  subprocess.Popen(bvrcmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   returncode = process.wait()
   outbvr_485 = process.stdout.read().decode("utf-8")
   if outbvr_485.find("failed:") >= 0:
      ret = 0
   #outbvr_485 = process.stdout.read()   
   print ("outbvr_485=%s"%outbvr_485)


   process =  subprocess.Popen(btempcmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   returncode = process.wait()
   outbtemp_485 = process.stdout.read().decode("utf-8")
   if outbtemp_485.find("failed:") >= 0:
      ret = 0
   #outbtemp_485 = process.stdout.read().decode("utf-8")outbtemp_485 = process.stdout.read()   
   print ("outbtemp_485=%s"%outbtemp_485)

   
   return outti_485,outbvr_485,outbtemp_485,ret
   
	
def parseBTS(command,parameter,index):

  
	#output = command.decode("utf-8")
	output = command
	output = output.replace('\t',' ')
	output = output.replace('\n',':')
	#print(output)
	output = output.split(':')
	a = output

	#print( "START DEBUF=%s"%a)    
	#print( len(a))                        
	for x  in range(index, len(a) -1,2): 
		totalCount = a[x]
		totalCount = totalCount[2:]
		#print ('totalCount:', totalCount)
		hextoint = int(totalCount,16) 
		#print ('hextoint:', hextoint)
		parameter.append(hextoint)

	print (parameter) 



def main():

   #logging.info('Hello pi!')
   while(1):
        response = os.system("ping -c 1 " + hostname)

        #and then check the response...
        if response == 0:
            print ("host is up!")
            break
        else:
            print ("host is down!")
            sleep(5)
   while(1):
        try:
         parameter_vr = []
         parameter_ti = []
         parameter_ta = []
         outti485,outbvr485,outbtemp485,ret = readBTS()
         if ret == 0 :
            print('mobus error !!!!!!, we are going to retry!!')
            sleep(25)
         else :	
          	parseBTS(outbvr485,parameter_vr,v1_index)
          	parseBTS(outbtemp485,parameter_ta,temp_index)
          	parseBTS(outti485,parameter_ti,ti_index)
          	check.callServer(parameter_ti,parameter_vr,parameter_ta,247,0)
          	sleep(29);
        except KeyboardInterrupt:
          print('interrupted!')

          

if __name__ == "__main__":
    main()

