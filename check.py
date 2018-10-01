import urllib.request
import urllib.parse
#import RPi.GPIO as GPIO
#import serial
import string
#import mainloop
import re
#import logging
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import socket
import urllib.request

# timeout in seconds
timeout = 8                                                                                                                                                                                  
socket.setdefaulttimeout(timeout)

#http://www.wisoft.com.tw/wibattery/pass_result.jsp?b_id=0&b_address=247&b_t=28.5&b_i=1.5&v0=12.3&r0=4.3&v1=12.3&r1=4.32&v2=12&t0=0..
def callServer(b_ti,b_vr,b_temp,b_address,b_id):


		print("checkServer.............")


		urlstr = []
		
		urlstr ="http://www.wisoft.com.tw/wibattery/pass_result.jsp?b_id=%s"%str(b_id)+\
		          "&b_address=%s"%str(b_address)+\
		          "&b_t=%.1f"%(b_ti[1]*0.1)+"&b_i=%.1f"%(b_ti[0]*0.01)+\
                  "&v0=%.1f"%(b_vr[0]*0.01)+"&r0=%.1f"%(b_vr[1] << 32 + b_vr[2])+\
                  "&v1=%.1f"%(b_vr[3]*0.01)+"&r1=%.1f"%(b_vr[4] << 32 + b_vr[5])+\
                  "&v2=%.1f"%(b_vr[6]*0.01)+"&r2=%.1f"%(b_vr[7] << 32 + b_vr[8])+\
                  "&v3=%.1f"%(b_vr[9]*0.01)+"&r3=%.1f"%(b_vr[10] << 32 + b_vr[11])+\
                  "&v4=%.1f"%(b_vr[12]*0.01)+"&r4=%.1f"%(b_vr[13] << 32 + b_vr[14])+\
                  "&v5=%.1f"%(b_vr[15]*0.01)+"&r5=%.1f"%(b_vr[16] << 32 + b_vr[17])+\
                  "&v6=%.1f"%(b_vr[18]*0.01)+"&r6=%.1f"%(b_vr[19] << 32 + b_vr[20])+\
                  "&v7=%.1f"%(b_vr[21]*0.01)+"&r7=%.1f"%(b_vr[22] << 32 + b_vr[23])+\
                  "&t0=%.1f"%(b_temp[0]*0.1)+"&t1=%.1f"%(b_temp[1]*0.1)+\
                  "&t2=%.1f"%(b_temp[0]*0.1)+"&t3=%.1f"%(b_temp[1]*0.1)+\
                  "&t4=%.1f"%(b_temp[0]*0.1)+"&t5=%.1f"%(b_temp[1]*0.1)+\
                  "&t6=%.1f"%(b_temp[0]*0.1)+"&t7=%.1f"%(b_temp[1]*0.1)
                  
		#print(urlstr)
		try:
		    f = urllib.request.urlopen(urlstr ,timeout=5)
		except HTTPError as e:
		    print('The server couldn\'t fulfill the request.')
		    print('Error code: ', e.code)
		    #logging.info('the server could not be reached!')
		except URLError as e:
		    print('We failed to reach a server.')
		    print('Reason: ', e.reason)
		    #logging.info('we failed to readch server!!!!!'):
		except:    
		    print("except")
		else:
		        readback_server = f.read().decode('utf-8')
		        print("show = %s."%(readback_server) )
		        #print(readback_server.find("OK"))
		        if readback_server.find("OK") >= 0:
		            print("web server is live")
		            #print ("%s is on the list! SET GATE%d (GPIO%d) to OPEN"%(readback,GATE,GATEIO))
		            #GPIO.output(GATEIO, mainloop.OPEN)
		            #logging.info('%s is on the list! SET GATE%d (GPIO%d) to OPEN'%(readback,GATE,GATEIO))
		            #logging.info('Hello world again!')
		        else:
		            #GPIO.output(GATEIO, mainloop.CLOSE)
		            #print ("%s is not on the list! SET GATE%d (GPIO%d) to LOW"%(readback,GATE,GATEIO))
		            #logging.info('%s isnt on the list! SET GATE%d (GPIO%d) to CLOSE'%(readback,GATE,GATEIO))
		            print("die!!!")
           
                    
