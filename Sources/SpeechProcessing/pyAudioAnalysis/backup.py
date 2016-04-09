# Below is old code I wanted to keep for reference
		'''
		while 1:
				l,data = inp.read()
				if l:
					for i in range(len(data)/2):
						curWindow.append(audioop.getsample(data, 2, i))

					if (len(curWindow)+len(midTermBuffer)>midTermBufferSize):
						samplesToCopyToMidBuffer = midTermBufferSize - len(midTermBuffer)
					else:
						samplesToCopyToMidBuffer = len(curWindow)

					midTermBuffer = midTermBuffer + curWindow[0:samplesToCopyToMidBuffer];
					del(curWindow[0:samplesToCopyToMidBuffer])
				

				# If RECORDING_LEN num of seconds have ellapsed
				if len(midTermBuffer) == midTermBufferSize:
					end_datetime = datetime.datetime.now()
					# allData = allData + midTermBuffer             
					curWavFileName = RecordPath + os.sep + str(elapsedTime) + ".wav"                
					midTermBufferArray = numpy.int16(midTermBuffer)
					wavfile.write(curWavFileName, Fs, midTermBufferArray)
					# print "AUDIO  OUTPUT: Saved " + curWavFileName
					midTermBuffer = []
		'''
					# elapsedTime = "%08.3f" % (time.time())  
		'''
					# Enqueue the file to be processed
					unprocessed_files.put(curWavFileName)

					logging.debug('Putting ' + str(curWavFileName) + ' : ' 
								  + str(unprocessed_files.qsize()) + ' items in queue')
		return
		'''