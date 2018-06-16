import re,time,math,socket,os,ConfigParser
from datetime import datetime

cp = ConfigParser.SafeConfigParser()
cp.read('./config.ini')
file_path = cp.get('rotor','file_path')
port = cp.getint('rotor','port')
lon_in = cp.getfloat('rotor','lon')
lat_in = cp.getfloat('rotor','lat')

fp = open(file_path, "rb")
ecef_str=fp.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',port))
os.system("clear")

lon = lon_in/180.0*math.pi
lat = lat_in/180.0*math.pi

while 1:
	timestamp = time.time()
	now = datetime.now()
	print "\033[0;0H"
	print now,"     "

	matchObj = re.search('%d (.*) (.*) (.*) (.*) (.*) (.*)'%timestamp,ecef_str)
	
	rx = float(matchObj.group(1))
	ry = float(matchObj.group(2))
	rz = float(matchObj.group(3))	

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

	s.send("P %.2f %.2f\n\n"%(az*180.0/math.pi,el*180.0/math.pi))
	d = s.recv(1024)

	time.sleep(1)
	s.send("p\n")
	time.sleep(0.1)
	d = s.recv(1024)
	print "\n[Rotor Az/El]: \n",d,"     "
	
	time.sleep(1)