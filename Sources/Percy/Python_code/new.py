import requests
import json

IP = '127.0.0.1'
SERVERIP = 'http://'+IP+'/DynalitePHPServer/'

def set_lightColor(location, color):
# locations are estimote labels which includes like mint, ice, blueberry
# color stored in hex format, other format data should be converted before making this function call

	request = requests.post(SERVERIP+"updateColor.php", data={'location': location, 'color':color})
	response = json.loads(request.text)



def get_users():
# Makes call to Users table to get list of all enrolled userIDS
# Note: userIDS should be the IDs given by Project Oxford
	users = []

	request = requests.post(SERVERIP+"getUsers.php", data={})
	response = json.loads(request.text)

	for i in range(0,int(response['count'])):
		users.append(str(response[str(i)]['p_o_id']))

	return users



def get_occupants():
# Makes call to Location table to get a list of (userID, locationID) tuples
# If a location has nobody present, userID should be returned as NULL (or something like that)
# Note: userIDS should be the IDs given by Project Oxford
	occupants = []

	request = requests.post(SERVERIP+"getOccupants.php", data={})
	response = json.loads(request.text)

	for i in range(0,int(response['count'])):
		occupants.append((str(response[str(i)]['p_o_id']), str(response[str(i)]['location'])))


	return occupants
