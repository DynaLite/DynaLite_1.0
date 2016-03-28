from socket import *
import sys
from lifxlan import *


def main(argv):
	islifx=False
	try:
		print "Discovering LIFX bulbs..."
		lifx = LifxLAN()
		devices = lifx.get_lights()
		bulb = devices[0]
		bulb.set_power("on")
		islifx = True
	except e:
		islifx=False

	try:
		PORT = int(argv[0])
	except error:
		PORT = 12345

	PORT = 12345
	HOST = ''
	ADDR = (HOST, PORT)
	BUFSIZE = 4096

	server = socket(AF_INET, SOCK_STREAM)
	server.bind((ADDR))
	print "Server IP: ", server.getsockname()[0]

	server.listen(5)
	print 'listening...'
	conn,addr = server.accept()
	print 'Connected by', addr

	conn.settimeout(15.0)
	while True:
		try:
			msg = conn.recv(BUFSIZE)
			if msg.find("ON")>=0:
				if msg.find("Ice")>=0 and islifx==True:
					bulb.set_power("on")
				else:
					bulb.set_power("off")
			else:
				bulb.set_power("off")
		except timeout, e:
			conn.close();
			server.close();
			break
	sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])