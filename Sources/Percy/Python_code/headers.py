from mysql import connector

#MySQL config
config = {
  'user': 'root',
  'password': 'enjoy',
  'host': '127.0.0.1',
  'database': 'Dynalite',
  'raise_on_warnings': True,
}

def set_lightColor(location, color):
# locations are estimote labels which includes like mint, ice, blueberry
# color stored in hex format, other format data should be converted before making this function call

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
		return False

	# Do query
	query = "UPDATE bulbs SET color=\'"+color+"\' WHERE location=\'"+location+"\'"
	cursor.execute(query)

	return



def get_users():
# Makes call to Users table to get list of all enrolled userIDS
# Note: userIDS should be the IDs given by Project Oxford
	users = []

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
		return False
	
	# Do stuff
	query = "SELECT p_o_id FROM users"
	cursor.execute(query)
	result = cursor.fetchall()
	cnn.close()

	for item in result:
		users.append(str(item[0]))

	return users



def get_occupants():
# Makes call to Location table to get a list of (userID, locationID) tuples
# If a location has nobody present, userID should be returned as NULL (or something like that)
# Note: userIDS should be the IDs given by Project Oxford
	occupants = []

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
		return False

	# Do stuff
	query = "SELECT users.p_o_id, location.location FROM users INNER JOIN location ON users.id=location.user_id"
	cursor.execute(query)
	result = cursor.fetchall()
	cnn.close()

	for item in result:
		occupants.append((str(item[0]), str(item[1])))


	return occupants




# while (True):
	
# 	# Record Audio
# 	recording = record()

# 	# Segment by speaker
# 	segments = sement_by_speaker(recording)

# 	# Identify the segments by user using the segments and list of our userIDs
# 	users = get_occupants()

# 	# identified_user_segments will be a list of ( (userID, userLOC), .wavfile) tuples
# 	identified_user_segments = identify_speakers(segments, users)

# 	# Classify emotions for each user
# 	user_states = []
# 	for user in identified_user_segments:
# 		# classify returns a ( (userID, userLOC), emotion) tuple
# 		user_states.append( classify(user) )

# 	user_decisions = []
# 	for user in user_states:
# 		# decide returns a color value for a user, ( (userID, userLOC), color) tuples
# 		user_decisions.append( decide(user) )

# 	# Set the light for each user
# 	for user in user_decisions:
# 		set_light(user)

