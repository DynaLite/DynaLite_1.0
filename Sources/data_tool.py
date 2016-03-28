import sys, getopt, random, csv
from prettytable import PrettyTable
from numpy.random import multinomial, shuffle, randint
from numpy import argmax, nonzero
from sklearn import tree

#  Generates data for a room/bulb, for a single day
#
#  Requires: prettytable
#
#  Usage: python data_tool.py [-t <time> || -a] -d <num_days> -o <filename> -u <num_users>
#  -t : time interval mode, where <time> is the time between data collection in minutes
#  -a : action-oriented mode, where data is only collected when there is an action taken
#  -d : number of days to simulate, defaults to 1
#  -u : number of users to simulate, defaults to 1
#  -o : indicates that you would like to print the data to a csv file

class User:
	# #Generates a random User

    # Generates a User based on input file, or a random user if no file is provided
    # present_likelihood + absent_likelihood = 1
    # pos_likelihood + neg_likelihood + neutral_likelihood = 1
	def __init__(self, 
				present_likelihood = None, 
				absent_likelihood = None, 
				pos_likelihood = None, 
				neg_likelihood = None, 
				neutral_likelihood = None, 
				pos_color = None,
				neg_color = None,
				neutral_color = None,
				emo_consistency_score = None,
				history_consistency_score = None):
		if(present_likelihood != None):
			self.present = present_likelihood
		else:
			self.present = random.random()
		self.absent = 1-self.present

		if(pos_likelihood != None):
			self.pos = pos_likelihood
		else:
			self.pos = random.random()
		if(neg_likelihood != None):
			self.neg = neg_likelihood
		else:
			self.neg = random.random()
			while(self.neg + self.pos > 1):
				self.neg = random.random()
		self.neutral = (1.- self.pos) - self.neg

		if(pos_color != None):
			self.pos_color = pos_color
		else:
			self.pos_color = random.uniform(0, 360)
		if(neg_color != None):
			self.neg_color = neg_color
		else:
			self.neg_color = random.uniform(0, 360)
		if(neutral_color != None):
			self.neutral_color = neutral_color
		else:
			self.neutral_color = random.uniform(0, 360)

		if(emo_consistency_score != None):
			self.emocons = emo_consistency_score
		else:
			self.emocons = random.random()

		if(history_consistency_score != None):
			self.histcons = history_consistency_score
		else:
			self.histcons = random.random()
			while(self.histcons + self.emocons > 1):
				self.histcons = random.random()

		self.color = randint(1,3)

	def getPresence(self):
		#self.lastPresence = entnum
		return argmax(multinomial(1, [self.present, self.absent], size=1))
	def getEmotion(self):	
		return argmax(multinomial(1, [self.pos, self.neg, self.neutral], size=1))
	def getColor(self):
		return self.color
		arg = argmax(multinomial(1, [self.histcons, self.emocons], size=1))
		if (arg == 0):
			emo = argmax(multinomial(1, [self.pos, self.neg, self.neutral], size=1))
			if(emo == 0):
				return self.pos_color
			if(emo == 1)
				return self.neg_color
			if(emo == 2):
				return self.neutral_color


			

def generate(timeInterval=None, outputfile = None, days=1, num_users=1):
	# days = int(days)
	# timeInterval = int(timeInterval)
	# users = int
	
	entries = []
	users = []
	for i in range(0, num_users):
		users.append(User())

	#Time interval mode
	if timeInterval:
		for t in range(0, 24*60*days, timeInterval):
			user_presence = []
			user_emotion = []
			for i in range(num_users):
				user_presence.append(users[i].getPresence())
				user_emotion.append(users[i].getEmotion())

			colors = []
			for i in nonzero(user_presence):
				colors.append(users[i].getColor())

			index = random.randint(1,len(colors))
			if not colors:
				color = "Off"
			else:
				color = colors[index]
			intensity = 100
			set_by = index

			entries.append([t, color, intensity, set_by] + user_presence + user_emotion)

	#Action-oriented mode
	else:
		print("action-oriented mode")


	user_pres = []
	user_emo = []
	for i in range(num_users):
		user_pres.append("user-" + str(i) + " present")
		user_emo.append("user-" + str(i) + " emotion")
	

	t = PrettyTable(["timestamp", "color", "intensity", "set-by"] + user_pres + user_emo)
	for i in range(len(entries)):
		t.add_row(entries[i])
	print(t)

	if(outputfile != None):
		with open(outputfile + ".csv", 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(entries)


def main(argv):

	outputfile = None
	days = '1'
	users = '1'
	try:
		opts, args = getopt.getopt(argv,"t:ai:o:d:u:",["time-interval=","ofile=", "days=", "users="])
	except getopt.GetoptError:
		print ('python data_tool.py [-t <time> || -a] -d <num_days> -o <filename>')
		sys.exit(2)
	for opt, arg in opts:
		# if opt == '-h':
		#    print 'test.py -i <inputfile> -o <outputfile>'
		#    sys.exit()
		if opt in ("-t", "--time-interval"):
			timeInterval = arg
			mode = "t"
		elif opt in ("-a"):
			mode = "a"
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-d", "--days"):
			days = arg
		elif opt in ("-u", "--users"):
			users = arg

	if(mode == "a"):
		generate(outputfile, int(days), int(users))
	if(mode == 't'):
		generate(int(timeInterval), outputfile, int(days), int(users))

def createDecisionTree(train, outputs):
	dt = tree.DecisionTreeClassifier()
	dt = clf.fit(train, outputs)
	return dt

def predict(dt, input):
	return dt.predict(input)

if __name__ == "__main__":
	main(sys.argv[1:])
