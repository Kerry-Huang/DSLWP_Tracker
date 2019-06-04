import re,time,math,socket,os,ConfigParser
from datetime import datetime

################ Mark ################
INFO = "[\033[32mINFO\033[0m]"
ERROR = "[\033[31mERROR\033[0m]"
SUCCESS = "[\033[32mSUEECSS\033[0m]"
WARNING = "[\033[33mWARNING\033[0m]"
######################################

############### Config ###############
cp = ConfigParser.SafeConfigParser()
cp.read('./config.ini')
file_path = cp.get('rotor','file_path')
port = cp.getint('rotor','port')
lon_in = cp.getfloat('rotor','lon')
lat_in = cp.getfloat('rotor','lat')
delta_el = cp.getfloat('rotor','delta_el')
delta_az = cp.getfloat('rotor','delta_az')
######################################

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1',port))
	os.system("clear")

except Exception as e:
	print ERROR,e
	exit()
	
az = input("AZ:")
el = input("EL:")
os.system("clear")

while 1:
	timestamp = time.time()
	now = datetime.now()
	print "\033[0;0H"
	print now,"     "

	print "\n[Input Az/El]: \n",az,"     ","\n",el,"     "
	
	if (el*180.0/math.pi)<0:
		el = 0

	s.send("P %.2f %.2f\n\n"%(az+delta_az,el+delta_el))
	d = s.recv(1024)

	time.sleep(1)
	s.send("p\n")
	time.sleep(0.1)
	d = s.recv(1024)
	print "\n[Rotor Az/El]: \n",d,"     "
	
	time.sleep(1)
