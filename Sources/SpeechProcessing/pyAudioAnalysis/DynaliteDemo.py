import threading 
from lifxlan import *
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
import dynaliteAudioSegmentation as dAS
import audioTrainTest as aT
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
midTermBufferSize = int(Fs*RECORDING_LEN)

#MySQL config
config = {
  'user': 'dynalite',		# Might need to change
  'password': 'eecs498',	# Might need to change
  'host': '127.0.0.1',
  'database': 'Dynalite',
  'raise_on_warnings': True,
}

lifxlan = LifxLAN()
lifxlan.set_power_all_lights("on", rapid=True)

RED = 			[62978, 65535, 65535, 3500]
ORANGE = 		[5525,  65535, 65535, 3500]
YELLOW = 		[7615,  65535, 65535, 3500]
GREEN = 		[16173, 65535, 65535, 3500]
CYAN = 			[29814, 65535, 65535, 3500]
BLUE = 			[43634, 65535, 65535, 3500]
PURPLE = 		[50486, 65535, 65535, 3500]
PINK = 			[58275, 65535, 47142, 3500]
WHITE = 		[58275, 0, 	   65535, 5500]
COLD_WHTE = 	[58275, 0,     65535, 9000]
WARM_WHITE = 	[58275, 0,     65535, 3200]
GOLD = 			[58275, 0,     65535, 2500]

THRESHOLD = 0.8

# SVM Models
MODELS_DIR 									= "MODELS/demo/"
LOW_VS_HIGH_AROUSAL 						= "low_vs_high_arousal"
LOW_AROUSAL__LOW_VALENCE_VS_HIGH_VALENCE 	= "low_arousal__low_valence_vs_high_valence"
HIGH_AROUSAL__LOW_VALENCE_VS_HIGH_VALENCE 	= "high_arousal__low_valence_vs_high_valence"
ANGRY_VS_FEAR 								= "angry_vs_fear"
CALM_VS_ALL									= "calm_vs_all"

# Classes
LOW_AROUSAL 				= "low_arousal"
HIGH_AROUSAL 				= "high_arousal"
LOW_AROUSAL__LOW_VALENCE 	= "low_arousal__low_valence"
LOW_AROUSAL__HIGH_VALENCE 	= "low_arousal__high_valence"
HIGH_AROUSAL__LOW_VALENCE 	= "high_arousal__low_valence"
HIGH_AROUSAL__HIGH_VALENCE 	= "high_arousal__high_valence"
NEUTRAL						= "neutral"
CALM 						= "calm"
HAPPY 						= "happy"
SAD 						= "sad"
ANGRY 						= "angry"
FEAR 						= "fear"
DISGUST 					= "disgust"
BOREDOM 					= "boredom"

# Emotion to Color
emotion_color_map = {
	NEUTRAL : WARM_WHITE,
	CALM 	: PURPLE,
	HAPPY 	: GREEN,
	SAD 	: BLUE,
	ANGRY 	: RED,
	FEAR 	: ORANGE,
	DISGUST : GOLD,
	BOREDOM : PINK
}

# ~~~ FUNC DEFS ~~~~~~~~~

def model_path(model_name):
	return MODELS_DIR + model_name

def set_lightColor(location, color):
# locations are estimote labels which includes like mint, ice, blueberry color 
# stored in hex format, other format data should be converted before making this function call

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
	query = "UPDATE bulbs SET color=\'"+color+"\' WHERE locations=\'"+location+"\'"
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

def classify_file(recording, model_name):
	Result, P, classNames = aT.fileClassification(recording, model_path(model_name), "svm")
	winner_class = classNames[int(Result)]
	winner_prob =P[int(Result)]
	print "Winner class: " + winner_class + " - with prob: " + str(winner_prob)

	return (winner_class, winner_prob)

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
		midTermBuffer = []
		curWindow = []
		elapsedTime = "%08.3f" % (time.time())

		# Main event loop
		while True:
			while len(get_occupants()) == 0:
				logging.debug('Waiting for occupants')
				time.sleep(WAIT_FOR_OCCUPANT_TIME)

			logging.debug("Starting recording")

			#*******************************************************************

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

			#*******************************************************************

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
						
			# Classify the emotion
			class_name, prob = classify_file(recording, LOW_VS_HIGH_AROUSAL)

			if class_name < THRESHOLD:
				lifxlan.set_color_all_lights(emotion_color_map[NEUTRAL], rapid=False)
			elif class_name == LOW_AROUSAL:
				class_name, prob = classify_file(recording, LOW_AROUSAL__LOW_VALENCE_VS_HIGH_VALENCE)
				if prob < THRESHOLD:
					lifxlan.set_color_all_lights(emotion_color_map[NEUTRAL], rapid=False)
				elif class_name == LOW_AROUSAL__LOW_VALENCE:
					lifxlan.set_color_all_lights(emotion_color_map[SAD], rapid=False)
				elif class_name == LOW_AROUSAL__HIGH_VALENCE:
					lifxlan.set_color_all_lights(emotion_color_map[CALM], rapid=False)
			elif class_name == HIGH_AROUSAL:
				class_name, prob = classify_file(recording, HIGH_AROUSAL__LOW_VALENCE_VS_HIGH_VALENCE)
				if prob < THRESHOLD:
					lifxlan.set_color_all_lights(emotion_color_map[NEUTRAL], rapid=False)
				elif class_name == HIGH_AROUSAL__LOW_VALENCE:
					class_name, prob = classify_file(recording, ANGRY_VS_FEAR)
					if prob < THRESHOLD:
						lifxlan.set_color_all_lights(emotion_color_map[NEUTRAL], rapid=False)
					elif class_name == ANGRY:
						lifxlan.set_color_all_lights(emotion_color_map[ANGRY], rapid=False)
					elif class_name == FEAR:
						lifxlan.set_color_all_lights(emotion_color_map[FEAR], rapid=False)
				elif class_name == HIGH_AROUSAL__HIGH_VALENCE:
					lifxlan.set_color_all_lights(emotion_color_map[HAPPY], rapid=False)
		pass
