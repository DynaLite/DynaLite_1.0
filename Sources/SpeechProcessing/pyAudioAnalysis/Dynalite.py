import threading 
import Queue
import time
import datetime
import logging
import random
from mysql import connector

# Below are the imports needed for pyAudioAnalysis adapted code
import sys, os, alsaaudio, time, audioop, numpy, glob
import scipy, subprocess, wave, mlpy, cPickle, shutil
import scipy.io.wavfile as wavfile
from scipy.fftpack import rfft
import dynaliteSpeakerDiarization as dSD
from scipy.fftpack import fft


# ~~~ CONSTANTS ~~~~~~~~~

MIN  = 60
HOUR = 60 * MIN
DAY  = 24 * HOUR

BUF_SIZE      = 10
UPDATE_PERIOD = 1 * MIN

RECORDING_LEN = 3.0
RECORD_PATH = "/tmp/yolo/"

WAIT_FOR_OCCUPANT_TIME = 5

# Needed for pyAudioAnalysis adapted code
Fs = 16000

#MySQL config
config = {
  'user': 'root',
  'password': 'enjoy',
  'host': '127.0.0.1',
  'database': 'Dynalite',
  'raise_on_warnings': True,
}

# ~~~ FUNC DEFS ~~~~~~~~~

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

# ~~~ GLOBALS ~~~~~~~~~

unprocessed_files = Queue.Queue(BUF_SIZE)
logging.basicConfig(level=logging.DEBUG,
					format='(%(threadName)-9s) %(message)s',)


# ~~~ THREAD SUBCLASS DEFS ~~~~~~~~~

class audioRecordThread(threading.Thread):
	def __init__(self, group=None, target=None, name=None,
				 args=(), kwargs=None, verbose=None):
		super(audioRecordThread,self).__init__()
		self.target = target
		self.daemon = True
		self.name = name

	def run(self):
	# Adapted from pyAudioAnalysis
	# git@github.com:tyiannak/pyAudioAnalysis.git 
	# 
	# Funtion records an audio segment of len RECORDING LEN
	# and stores it in record_path  
		RecordPath = RECORD_PATH

		RecordPath += os.sep
		d = os.path.dirname(RecordPath)
		if os.path.exists(d) and RecordPath!=".":
			shutil.rmtree(RecordPath)   
		os.makedirs(RecordPath) 

		inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
		inp.setchannels(1)
		inp.setrate(Fs)
		inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
		inp.setperiodsize(512)
		midTermBufferSize = int(Fs*RECORDING_LEN)
		midTermBuffer = []
		curWindow = []
		elapsedTime = "%08.3f" % (time.time())

		# Main event loop
		while True:
			while len(get_occupants()) == 0:
				logging.debug('Waiting for occupants')
				time.sleep(WAIT_FOR_OCCUPANT_TIME)

			logging.debug("Starting recording")
			while len(midTermBuffer) < midTermBufferSize:
				l,data = inp.read()
				if l:
					for i in range(len(data)/2):
						curWindow.append(audioop.getsample(data, 2, i))

					if (len(curWindow)+len(midTermBuffer)>midTermBufferSize):
						samplesToCopyToMidBuffer = midTermBufferSize \
												   - len(midTermBuffer)
					else:
						samplesToCopyToMidBuffer = len(curWindow)

					midTermBuffer = midTermBuffer \
									+ curWindow[0:samplesToCopyToMidBuffer];
					del(curWindow[0:samplesToCopyToMidBuffer])

			logging.debug("Finnished recording")
			end_datetime = datetime.datetime.now()

			# allData = allData + midTermBuffer             
			curWavFileName = RecordPath + os.sep + str(elapsedTime) + ".wav"                
			midTermBufferArray = numpy.int16(midTermBuffer)
			wavfile.write(curWavFileName, Fs, midTermBufferArray)
			midTermBuffer = []
			
			elapsedTime = "%08.3f" % (time.time())  

			# See who's in the room now
			occupants = get_occupants()
			if len(occupants) == 0:
				# Delete the recording, nobody present
				logging.debug('No occupants, deleting: ' + str(recording))
				os.remove(recording)
			else:
				# Enqueue the file to be processed
				unprocessed_files.put((curWavFileName, occupants))
				logging.debug('Enqueuing ' + str(curWavFileName) + ' : ' \
							  + str(unprocessed_files.qsize()) + ' items in queue')
			pass


if __name__ == '__main__':
	
	print "Press Ctr+C to stop Dynalite"

	# Create a audioRecordThread that runs till main thread exits
	producer = audioRecordThread( name='Rec-Thread')
	producer.start()

	while True:
		if not unprocessed_files.empty():
			# Get Audio Recording
			recording, occupants = unprocessed_files.get()
			logging.debug('Getting ' + str(recording) + ' : ' 
						  + str(unprocessed_files.qsize()) + ' items in queue')                
						
			# [1] Segment Recording by Speaker (Speaker Diarization)
			speaker_files = []

			if(len(occupants) >= 2):
				segments = dSD.speakerDiarization(recording, len(occupants))
				# segments.sort(key=lambda seg: seg[1])
				speaker_files.append(recording)

			else:
				speaker_files.append(recording)


			# [2] Remove Silence 
			# TODO
			for file in speaker_files:
				# file = remove_silence(file)
				pass

			# [3] Identify each file using Project Oxford			
			for file in speaker_files:
				pass

			# [4] Classify the emotion for each user

			# user_states = []
			# for user in identified_user_segments:
			# 	# classify returns a ( (userID, userLOC), emotion) tuple
			# 	user_states.append( classify(user) )

			# [5] Get a decision

			# user_decisions = []
			# for user in user_states:
			# 	# decide returns a color value for a user, ( (userID, userLOC), color) tuples
			# 	user_decisions.append( decide(user) )

			# # [6] Set lights
			# for user in user_decisions:
			# 	set_light(user[0][1], user[1])



		pass
