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
	fp = open(file_path, "rb")
	ecef_str=fp.read()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1',port))
	os.system("clear")

except Exception as e:
	print ERROR,e
	exit()

lon = lon_in/180.0*math.pi
lat = lat_in/180.0*math.pi

while 1:
	timestamp = time.time()
	now = datetime.now()
	print "\033[0;0H"
	print now,"     "

	matchObj = re.search('%d (.*) (.*) (.*) (.*) (.*) (.*)'%timestamp,ecef_str)
	
	try:
		rx = float(matchObj.group(1))
		ry = float(matchObj.group(2))
		rz = float(matchObj.group(3))	

	except Exception as e:
		print ERROR,"Tracking File is wrong."
		exit()

	r1x = math.cos(lon)*rx + math.sin(lon)*ry
	r1y = -math.sin(lon)*rx + math.cos(lon)*ry
	r1z = rz

	r2x = math.cos(-lat)*r1x - math.sin(-lat)*r1z
	r2y = r1y
	r2z = math.sin(-lat)*r1x + math.cos(-lat)*r1z

	el = math.atan(r2x / math.sqrt(r2y*r2y + r2z*r2z))
	az = math.acos(r2z / math.sqrt(r2y*r2y + r2z*r2z))
	
	if(r2y < 0):
		az = 2*math.pi - az
	
	print "\n[Clac Az/El]: \n",az*180.0/math.pi,"     ","\n",el*180.0/math.pi,"     "
	
	if (el*180.0/math.pi)<0:
		el = 0

	s.send("P %.2f %.2f\n\n"%(az*180.0/math.pi+delta_az,el*180.0/math.pi+delta_el))
	d = s.recv(1024)

	time.sleep(1)
	s.send("p\n")
	time.sleep(0.1)
	d = s.recv(1024)
	print "\n[Rotor Az/El]: \n",d,"     "
	
	time.sleep(1)
