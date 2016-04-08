folders:

Android:
	the package is named "registration"
	to change the server ip addr -> edit AppConfig.java
	either create your account 
	or use email:p@p pwd:123

DynalitePHPServer:
	MySQL login information can be found in Config.php
	Usage:
	
	getBulbs:
		no parameter
		return:(json)
		ex:
			{"error": FALSE
			 "count": 1 (#bulbs)
			 "0": { "name": "(bulb_1's mac addr)"
				    "location": "mint" (mint|ice|blueberry)(beacons)
				    "color": "#00A089"
				    "isON": 1
				  }
			}
	
	updateLocation:
		POST: user_id, location
		no return

	updateColor:
		POST: location, color(hex)
		no return

MySQL_schema:
	under database "Dynalite"
	will create:
		bulbs
		location
		users

Python_code:
	see comments in codes
	updateLightColor.py