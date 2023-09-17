from time import sleep
from random import randint
sleep(20)
import wifi
import os
from datetime import datetime
import datetime as datetimeo
import subprocess
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/2in13')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

basepath =os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
if os.path.exists(libdir):
    sys.path.append(libdir)
    
""" picdir = f'{basepath}/pic/2in13'
fontdir = f'{basepath}/pic'
libdir = f'{basepath}/lib'
"""
from TP_lib import gt1151
from TP_lib import epd2in13_V3
import time
import logging
from PIL import Image,ImageDraw,ImageFont
import traceback
import threading
from TP_lib import gt1151
from TP_lib import epd2in13_V3

fslu = 0
logging.basicConfig(level=logging.DEBUG)
flag_t = 1
scanTimes = 0
totalFinds = 0
logging.info("epd2in13_V3 Touch Demo")
epd = epd2in13_V3.EPD()
gt = gt1151.GT1151()
GT_Dev = gt1151.GT_Development()
GT_Old = gt1151.GT_Development()
#gt.GT_Init()
logging.info("init and Clear")
epd.init(epd.FULL_UPDATE)
def set_wlan0_up():
	try:
		subprocess.run(['sudo', 'ifconfig', 'wlan0', 'up'], check=True)
		subprocess.run(['sudo','iw','dev','wlan0','set','power_save','off'], check=True)
	except subprocess.CalledProcessError as e:
        	print(f"Failed to set wlan0 up: {e}")

def is_wlan0_up():
	try:
		output = subprocess.check_output(['ifconfig', 'wlan0'])
        	# You can also use the 'ip' command instead of 'ifconfig':
        	# output = subprocess.check_output(['ip', 'link', 'show', 'wlan0'])
		output = output.decode('utf-8')
		if "UP" in output:
			return True
		else:
			return False
	except subprocess.CalledProcessError:
        # This exception will be raised if 'ifconfig' or 'ip' command fails.
		return False 
localFinds = 0
def scan():
	global fslu
	global face
	global localFinds
	global scanTimes
	global totalFinds
	global commentary
	scanTimes += 1
	set_wlan0_up()
	now = datetime.now()
	current_time = now.strftime("%d/%m/%Y %H:%M:%S")
	current_date = now.strftime("%d/%m/%Y")
	try:
		out  = subprocess.run(['sudo','iwlist','wlan0','scan'], stdout=subprocess.PIPE,text=True)

	except Exception as e:
		with open(f'{basepath}/scripts/log.txt','a') as f:
			f.write('\n'+str(e)) 
			f.close()	
	networks =  out.stdout.split('\n')
	networks = [line for line in networks if 'ESSID' in line]
	print(networks) 
	newNetworks= []
	oldNetworks= []
	#with open(f'{basepath}/scripts/log.txt','a') as f:
	#	f.write(f'\n Scan Initiated at {current_time},wlan0 status= {is_wlan0_up()}')	
	#	f.close()
	for n in networks:
		n = n.replace('"','')
		n = n[26:]
		print(n)
		newNetworks.append(n)
	networks = newNetworks
	with open(f'{basepath}/scripts/address.txt','r') as f:
		file = f.read()
		values = file.split('\n')
		values.remove('')
		values.remove('SSIDs:')
		f.close()
	for n in networks:
		#now = datetime.now()
		#current_time = now.strftime("%H:%M:%S")
		with open(f'{basepath}/scripts/address.txt','r') as f:
			file = f.read()
			values = file.split('\n')
			values.remove('')
			values.remove('SSIDs:')
			totalFinds = str(len(values)+1)
			f.close()
		values2 = []
		for v in values:
			v = v.split(';')
			v = v[0]
			values2.append(v)
		values = values2
		if n not in values:
			with open(f'{basepath}/scripts/address.txt','a') as f:
				f.write('\n'+ str(n)+';'+str(current_date))
				print(n)
				f.close()
				localFinds += 1
				fslu += 1
		with open(f'{basepath}/scripts/log.txt','a') as f:
			if n != '':
				f.write('\n'+str(n)+', '+str(current_time))
			f.close()
	with open(f'{basepath}/scripts/address.txt','r') as f:
		unfiltered = f.read()
		unfiltered = unfiltered.split('\n')
		unfiltered.remove('')
		unfiltered.remove('SSIDs:')
		foundToday = 0
		print(current_date)
		for v in unfiltered:
			if v.split(';')[1] != current_date:
				unfiltered.remove(v)
				print("boo")
			else:
				print("yay")
				foundToday += 1
	
	if scanTimes > 0 and foundToday < 1:
		print("Hungry...")
		random = randint(1,3)
		if random == 1:
			commentary = "Hungry..."
		elif random == 2:
			commentary = "Feed... Me"
		elif random == 3:
			commentary = "Can we go for a walk?"
		face  = Image.open(os.path.join(picdir, 'lonely.bmp'))
	if scanTimes > 0 and foundToday > 0:
		print("Happy")
		commentary = "Happy!"
		face  = Image.open(os.path.join(picdir, 'awake.bmp'))
	if scanTimes > 0 and foundToday > 4:
                print("Friendly")
                commentary = "Yay!"
                face  = Image.open(os.path.join(picdir, 'friendly.bmp'))
                with open(f'{basepath}/scripts/loyalty.txt','r') as f:
                     file = f.read()
                     values = file.split('\n')
                if str(datetimeo.date.today()) not in values:
                     with open(f'{basepath}/scripts/loyalty.txt','a') as f:
                          f.write('\n'+str(datetimeo.date.today()))

	if scanTimes == 0:
	        print("Normal")
	        face  = Image.open(os.path.join(picdir, 'happy.bmp'))
	fslu = 0 #pls comment me out!
	if fslu < 1 and foundToday > 0:
		commentary = f"Nothing but found {foundToday} today."
	elif fslu < 1:
		commentary = "Nothing."
def pthread_irq() :
    global flag_t
    print("pthread running")
    while flag_t == 1 :
        if(gt.digital_read(gt.INT) == 0) :
            GT_Dev.Touch = 1
        else :
            GT_Dev.Touch = 0
    print("thread:exit")
 
def displayUpdate(fullUpdate):

    global fslu
    global localFinds
    global face
    global totalFinds
    global commentary
    global wardriving
    global image
    global t
    print(fslu)
    with open(f'{basepath}/scripts/log.txt','r') as f:
        values = f.read()
        values = values.split('\n')
        values.remove('')
        totalLog = str(len(values)-1)
    streak = 0 
    with open(f'{basepath}/scripts/loyalty.txt','r') as f:
        file = f.read()
        values = file.split('\n')
        for d in values:
            if d != "":
                streak += 1
        if str(datetimeo.date.today()-datetimeo.timedelta(days=1)) not in values and str(datetimeo.date.today()) not in values:
            print("STREAK BROKEN!")
            print(str(datetimeo.date.today()))
            with open(f'{basepath}/scripts/loyalty.txt','w') as f:
                f.write("")
            streak = 0
    print(f'streak:{streak}')
    print(f'totalLog:{totalLog}')
    logging.info("epd2in13_V3 Touch Demo")
    epd = epd2in13_V3.EPD()
    gt = gt1151.GT1151()
    GT_Dev = gt1151.GT_Development()
    GT_Old = gt1151.GT_Development()
    
    logging.info("init and Clear")
#    epd.init(epd.FULL_UPDATE)

    gt.GT_Init()
    #epd.Clear(0xFF)
    t = threading.Thread(target = pthread_irq)
    t.setDaemon(True)
    t.start()
    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(fontdir, 'RobotoMonoBold.ttf'), 15)
    font24 = ImageFont.truetype(os.path.join(fontdir, 'RobotoMono.ttf'), 24)
  
    epd = epd2in13_V3.EPD()
    image = Image.open(os.path.join(picdir, 'face.bmp'))
    DrawImage = ImageDraw.Draw(image)
    
    name =  os.getlogin()
    with open(f'{basepath}/scripts/name.txt','r') as f:
       readText = f.read()
       print(readText)
       if readText != '':
          name = str(readText.split('\n')[0])
          print(f'Name = {name}')
    ip = subprocess.run(['hostname','-I'], stdout=subprocess.PIPE,text=True)
    ip = ip.stdout.replace('\n','')
    ip = ""
    ipFont = font15
    if ip == "":
       ip = commentary
       ipFont = ImageFont.truetype(os.path.join(fontdir, 'RobotoMonoBold.ttf'), 12)
    print(ip)
    finds = str(totalFinds)
    streak = str(streak)
    s_height, s_width = DrawImage.textsize(streak,font=font15)
    name_height, name_width = DrawImage.textsize(name, font=font24)
    finds_height, finds_width = DrawImage.textsize(finds, font=font15)
    ip_height, ip_width = DrawImage.textsize(ip, font=ipFont)    
    total_height, total_width = DrawImage.textsize(totalLog, font=font15)
    name_x = 95
    name_y = 10
    finds_x = 75
    finds_y = 180
    ip_x = 10
    ip_y = 110
    if ip == commentary:
       ip_y = 50
    total_x,total_y = 45,180
    alteration = len(streak)*-4
    s_x, s_y = 65, 144+alteration

    offImage = Image.open(os.path.join(picdir, 'off.png'))
    nameImage = Image.new("1", (name_height, name_width), 0xFF)
    findsImage = Image.new("1", (finds_height, finds_width), 0xFF)
    ipImage = Image.new("1", (ip_height, ip_width), 0xFF)    
    totalImage = Image.new("1",(total_height,total_width),0xFF)
    sImage = Image.new("1",(s_height,s_width),0)
    draw_total = ImageDraw.Draw(totalImage)
    draw_name = ImageDraw.Draw(nameImage)
    draw_finds = ImageDraw.Draw(findsImage)
    draw_ip = ImageDraw.Draw(ipImage)    
    draw_s = ImageDraw.Draw(sImage)
    draw_total.text((0,0),totalLog,font=font15,fill = 0)
    draw_name.text((0,0),name,font=font24,fill = 0)
    draw_finds.text((0,0),finds,font=font15,fill = 0)
    draw_ip.text((0,0),ip,font=ipFont,fill = 0)
    draw_s.text((0,0),streak,font=font15,fill = 255)    
    nameImage = nameImage.transpose(Image.ROTATE_270)
    findsImage = findsImage.transpose(Image.ROTATE_270)
    totalImage = totalImage.transpose(Image.ROTATE_270)
    face = face.resize((120,74))
    face = face.transpose(Image.ROTATE_270)
    offImage = offImage.resize((30,30))
    offImage = offImage.transpose(Image.ROTATE_270)
    sImage = sImage.transpose(Image.ROTATE_270)
    heart = Image.open(os.path.join(picdir, '100+.jpg'))
    heart = heart.resize((315,111))
    heart = heart.transpose(Image.ROTATE_270)
    if fullUpdate:
        image.paste(heart,(20,-20))
        image.paste(sImage,(s_x,s_y))
        image.paste(face,(30,0))
        ipImage = ipImage.transpose(Image.ROTATE_270)    
        image.paste(nameImage,(name_x,name_y))
        image.paste(findsImage,(finds_x,finds_y))
        image.paste(ipImage,(ip_x,ip_y))
        image.paste(totalImage,(total_x,total_y))
        image.paste(offImage,(10,10))
        epd.displayPartBaseImage(epd.getbuffer(image))
    if fullUpdate:
    	epd.init(epd.FULL_UPDATE)
#    else:
        #image.paste(wImage,(wardriving_x,wardriving_y))
        #epd.displayPartBaseImage(epd.getbuffer(image))
       # epd.init(epd.PART_UPDATE)
    fslu = 0
    i = j = k = ReFlag = SelfFlag = Page = Photo_L = Photo_S = 0
#scan()
#displayUpdate()
refresh = 4
wardriving = False
update = 0
scan()
displayUpdate(fullUpdate = False)
awake = True
while True and awake:
        sleep(1)
        if update == 30:
             scan()
             update = 0
             refresh += 1
        # Read the touch input
        gt.GT_Scan(GT_Dev, GT_Old)
#        if(GT_Old.X[0] == GT_Dev.X[0] and GT_Old.Y[0] == GT_Dev.Y[0] and GT_Old.S[0] == GT_Dev.S[0]):
 #           continue
        
        if(GT_Dev.TouchpointFlag):
#            i += 1
             GT_Dev.TouchpointFlag = 0
                 #main menu
             if(GT_Dev.X[0] > 0 and GT_Dev.X[0] < 50 and GT_Dev.Y[0] > 0 and GT_Dev.Y[0] < 50):
#                    wardriving = not wardriving
#                    print(f'wardriving:{wardriving}')
#                    displayUpdate(fullUpdate = False)
                     awake = False
                     flag_t = 0
                     epd.Clear(0xFF)
                     epd.sleep()
                     time.sleep(2)
                     t.join()
                     epd.Dev_exit()
                     os.system("sudo shutdown now -h")
#marker
        if refresh == 6:
                displayUpdate(fullUpdate = True)
                refresh = 0  


        update += 1
