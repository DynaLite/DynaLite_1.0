import os, glob, ntpath, shutil
import scipy.io.wavfile as wavfile

def convertDirMP3ToWav(dirName, Fs, nC, useMp3TagsAsName = False):
	'''
	This function converts the MP3 files stored in a folder to WAV. If required, the output names of the WAV files are based on MP3 tags, otherwise the same names are used.
	ARGUMENTS:
	 - dirName:		the path of the folder where the MP3s are stored
	 - Fs:			the sampling rate of the generated WAV files
	 - nC:			the number of channesl of the generated WAV files
	 - useMp3TagsAsName: 	True if the WAV filename is generated on MP3 tags
	'''
	# For Dynalite, needed to remove this as it uncluded the eyed3 package, which
	# for some reason breaks logging???

def convertFsDirWavToWav(dirName, Fs, nC):
	'''
	This function converts the WAV files stored in a folder to WAV using a different sampling freq and number of channels.
	ARGUMENTS:
	 - dirName:		the path of the folder where the WAVs are stored
	 - Fs:			the sampling rate of the generated WAV files
	 - nC:			the number of channesl of the generated WAV files
	'''

	types = (dirName+os.sep+'*.wav',) # the tuple of file types
	filesToProcess = []

	for files in types:
		filesToProcess.extend(glob.glob(files))		

	newDir = dirName + os.sep + "Fs" + str(Fs) + "_" + "NC"+str(nC)
	if os.path.exists(newDir) and newDir!=".":
		shutil.rmtree(newDir)	
	os.makedirs(newDir)	

	for f in filesToProcess:	
		_, wavFileName = ntpath.split(f)	
		command = "avconv -i \"" + f + "\" -ar " +str(Fs) + " -ac " + str(nC) + " \"" + newDir + os.sep + wavFileName + "\"";
		print command
		os.system(command)

def readAudioFile(path):
	'''
	This function returns a numpy array that stores the audio samples of a specified WAV of AIFF file
	'''
	extension = os.path.splitext(path)[1]

	try:
		if extension.lower() == '.wav':
			[Fs, x] = wavfile.read(path)
		elif extension.lower() == '.aif' or extension.lower() == '.aiff':
			s = aifc.open(path, 'r')
			nframes = s.getnframes()
			strsig = s.readframes(nframes)
			x = numpy.fromstring(strsig, numpy.short).byteswap()
			Fs = s.getframerate()
		else:
			print "Error in readAudioFile(): Unknown file type!"
			return (-1,-1)
	except IOError:	
		print "Error: file not found or other I/O error."
		return (-1,-1)
	return (Fs, x)

def stereo2mono(x):
	'''
	This function converts the input signal (stored in a numpy array) to MONO (if it is STEREO)
	'''
	if x.ndim==1:
		return x
	else:
		if x.ndim==2:
			return ( (x[:,1] / 2) + (x[:,0] / 2) )
		else:
			return -1

