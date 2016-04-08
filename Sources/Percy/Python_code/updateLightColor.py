#
# 
# Get the first bulb and
# update light color every 2 secs
#
#

from lifxlan import *
from colorsys import rgb_to_hsv
from colorConvert import hex_to_rgb
from mysql import connector
from time import sleep

# database config
config = {
  'user': 'root',
  'password': 'enjoy',
  'host': '127.0.0.1',
  'database': 'Dynalite',
  'raise_on_warnings': True,
}

# LIFX bulb_1's mac addr as its name in the database(bulbs)
mac_1 = '\'d0:73:d5:12:4f:1e\''

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
		print "Can not discover any LIFX bulb"
		return

	print "Updating LIFX color..."
	while True:
		try:
			cnn = connector.connect(**config)
			cursor = cnn.cursor()
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print "Something is wrong with your user name or password"
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print "Database does not exist"
			else:
				print err
			return

		query = "SELECT color FROM bulbs WHERE name=\'"+bulb.get_mac_addr()+"\'"
		cursor.execute(query)
		result = cursor.fetchone()
		cnn.close()
		
		#convert color
		rgbColor = hex_to_rgb(str(result[0]))
		hsvColor = rgb_to_hsv(float(rgbColor[0])/255, float(rgbColor[1])/255, float(rgbColor[2])/255)
		hsbkColor = (int(hsvColor[0]*65535), int(hsvColor[1]*65535), int(hsvColor[2]*65535), 3500)

		#update color
		bulb.set_color(hsbkColor)
		sleep(2)
		
	return






if __name__ == "__main__":
    main(sys.argv[1:])