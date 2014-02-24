from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *
import random

class SoundCons:

	# ------------------------------------------------------------------------------------
	# public data members

	# options for __program
	RANDOM = 1
	ONCE = 2
	NONE = 3
	RANDOM_FULL = 4
	RANDOM_CONSTANT = 5
	RANDOM_LOOP = 6

# end class SoundCons


class SoundUtil:


	# ------------------------------------------------------------------------------------
	# private data members

	__debugOn = True		# (boolean)	for debugging purposes only, set to False for not debugging messages

	__soundInstance = None	# container for the sound instance
	__soundLoad = None		# container for loading sound
	__hostObj = None		# container for host object

	__loopPlay = False		# (boolean)	play in loop
	__stereo = True			# (boolean)	play in stereo mode
	__isPlaying = False		# (boolean)	check is playing sound

	__startTime = 0			# (int)		start time of play	(in seconds)
	__endTime = 0			# (int)		end time of play	(in seconds)

	__program = 0			# (int)		set the program of the sound.
							# possible values:
							# RANDOM, CUSTOM

	__randomTime = 0		# (int)		time variable for random function
	__randomDt = 0			# (int)		delta time for random function
	__randomSeed = 0		# (int)		seed variable for random function
	__randomLevel = 1		# (int)		level of randomness
	__randomVolume = 1.0	# (float)	volume level


	__soundEnv = getSoundEnvironment()	# container for sound environment



	# ------------------------------------------------------------------------------------
	# private data members



	# (PRIVATE) : constructor 1
	# takes three arguments
	# > hostObj -- the object to which you want to bind the sound to
	# > dir -- directory name in which you want to put the sound to
	# > soundFilePath -- path and name to the sound file.
	# no return value
	def __init__(self, dir, soundFilePath, hostObj = None):
		# None if no hostObj
		if self.__soundEnv != None:
			self.__hostObj = hostObj
			self.__soundLoad = self.__soundEnv.loadSoundFromFile(dir, soundFilePath)
			self.__soundInstance = SoundInstance(self.__soundLoad)
			self.__soundInstance.setLoop(False)
		# end if
	# end __init__


	# (PRIVATE) : set the play mode
	# takes one argument
	# > val -- True (Play the sound) or False (Stop the sound)
	# if val is True, then checks if self.__stereo is True
	# if True, Then plays in stereo mode else plays in normal mode
	# no return value
	def __setPlay(self, val):
		if val == True:
			self.__debugMode("Play")
			if self.__isPlaying == False:
				self.__isPlaying = True
				if self.__stereo == True:
					self.__soundInstance.playStereo()
				else:
					self.__soundInstance.play()
				# end if
			# end if
		# end if
		if val == False:
			self.__isPlaying = False
			self.__debugMode("Stop")
			self.__soundInstance.stop()
		# end if
	# end __setPlay


	# (PRIVATE) : set the play stereo mode
	# takes one argument
	# > val -- True (stereo mode) or False (normal mode)
	# no return value
	def __playStereo(self, val):
		self.__stereo = val
	# end __playStereo





	# (PRIVATE) : debug Mode
	# takes one argument
	# > text -- displays the text
	# no return value
	def __debugMode(self, text):
		if (self.__debugOn == True):
			print "debug> " + str(text)
		# end if
	# end __debugMode


	# ------------------------------------------------------------------------------------
	# public members

	# (PUBLIC) : set the position of the sound Instance
	# takes one argument
	# > pos -- position in Vector3 format (Vector3(x,y,z))
	# no return value
	def setSoundPosition(self, pos):
		self.__soundInstance.setPosition(pos)
		self.__debugMode("Setting Position")
	# end __setSoundPosition


	# (PUBLIC) : set the volume of the sound Instance.
	# takes one argument
	# > val -- sound volume (integer or floating point)
	# no return value
	def setVolume(self, val):
		self.__randomVolume = val
		self.__soundInstance.setVolume(val)
	# end __setVolume

	# (PUBLIC) : set the program
	# takes one/two arguments
	# > program -- sets the program of the sound. Eg. Random/custom
	# > list -- list type holds other options

	# setProgram(<program-type>, [parameters])
	# setProgram(SoundCons.ONCE, [startTime(int), endTime(int)])
	# setProgram(SoundCons.RANDOM, [random-level, randomTime(integer), randomSeed(float 0 to 1), randomVolume])

	# setProgram(SoundCons.ONCE, [2, 10])
	# setProgram(SoundCons.ONCE, [2])
	# setProgram(SoundCons.RANDOM)				-- default randomLevel = SoundCons.RANDOM_FULL
	# setProgram(SoundCons.RANDOM, [SoundCons.RANDOM_FULL])
	# setProgram(SoundCons.RANDOM, [SoundCons.RANDOM_CONSTANT])
	# setProgram(SoundCons.RANDOM, [SoundCons.RANDOM_CONSTANT, 25])
	# setProgram(SoundCons.RANDOM, [SoundCons.RANDOM_CONSTANT, 25, 0.80])
	# setProgram(SoundCons.RANDOM, [SoundCons.RANDOM_LOOP, 25, 0.80, 0.5])
	# pass one argument to set only the start time
	# no return value
	def setProgram(self, program, list = None):
		self.__program = program
		if (program == SoundCons.ONCE):
			if (len(list) < 1):
				print "---"
				print "Need one or two elements in the list."
				print "Exiting"
				print "---"
				exit(0)
			elif (len(list) == 1):
				self.__startTime = list[0]
				self.__endTime = -1
			elif (len(list) == 2):
				self.__startTime = list[0]
				self.__endTime = list[1]
			# end if
		# end if

		if (program == SoundCons.RANDOM):
			if (len(list) == 0):
				self.__randomLevel = SoundCons.RANDOM_FULL
			elif (len(list) >= 1):
				self.__randomLevel = list[0]
			# end if
			random.seed()
			self.__randomTime = random.randrange(9, 101, 5)
			self.__randomSeed = random.random()


			if (self.__randomLevel == SoundCons.RANDOM_CONSTANT):
				if (len(list) >= 2):
					self.__randomTime = list[1]
				# end if
				if (len(list) >= 3):
					self.__randomSeed = list[2]
				# end if
			elif (self.__randomLevel == SoundCons.RANDOM_LOOP):
				self.__soundInstance.setLoop(True)
				self.__soundInstance.setVolume(0.0)
				if (len(list) >= 2):
					self.__randomTime = list[1]
				# end if
				if (len(list) >= 3):
					self.__randomSeed = list[2]
				# end if
				if (len(list) >= 4):
					self.__randomVolume = list[3]
				# end if
				self.__soundInstance.play()
			# end if
		# end if
	# end setProgram


	# (PUBLIC) : set Loop play
	# takes one argument
	# > val -- True (play in loop) or False (don't play in loop)
	# no return value
	def setLoop(self, val):
		self.__soundInstance.setLoop(val)
	# end setLoop


	# (PUBLIC) : update method for each sound instance
	# takes three arguments
	# > frame
	# > t
	# > dt
	# pass the arguments from the onUpdate method in your main file
	# no return value
	def update(self, frame, t, dt):
		self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))

		# If no hostObj then dont update position.
		if (self.__hostObj != None):
			# Update position
			self.setSoundPosition(self.__hostObj.getPosition())
		# end if

		# use __program to identify how to play the sound
		if self.__program == SoundCons.RANDOM:
			self.__debugMode(str(self.__randomTime))
			if ((t - self.__randomDt) > self.__randomTime) :
				self.__randomDt = t
				random.seed()
				if (self.__randomLevel == SoundCons.RANDOM_FULL):
					self.__randomTime = random.randrange(9, 101, 5)
					self.__randomSeed = random.random()
				# end if
				num = random.random()
				if (self.__randomLevel == SoundCons.RANDOM_LOOP):
					if num > self.__randomSeed:
						self.__soundInstance.setVolume(self.__randomVolume)
					else:
						self.__soundInstance.setVolume(0.0)
					# end if
				else:
					if num > self.__randomSeed:
						self.__setPlay(True)
					# end if
				# end if
			# end if

		elif self.__program == SoundCons.ONCE:
			# Play within time interval
			if (self.__startTime != 0) and (self.__endTime != 0):
				if (((int(t) >= self.__startTime) and (int(t) <= self.__endTime)) and (self.__isPlaying == False)):
					self.__setPlay(True)
				# end if
				if (((int(t) >= self.__startTime) and (self.__endTime == -1)) and (self.__isPlaying == False)):
					self.__setPlay(True)
				# end if
				if ((int(t) >= self.__endTime) and (self.__endTime != -1) and (self.__isPlaying == True)):
					self.__setPlay(False)
				# end if
				if ((int(t) < self.__startTime) and (self.__isPlaying == True)):
					self.__setPlay(False)
				# end if
			elif (((self.__startTime == 0) and (self.__endTime == 0)) and (self.__isPlaying == False)):
				self.__setPlay(True)
			# end if

		elif self.__program == SoundCons.NONE:
			self.__setPlay(True)
		# end if
		
		if self.__soundInstance.isPlaying() == True:
			self.__isPlaying = True
			self.__debugMode("Still playing")
		# end if
		
		if (self.__soundInstance.isPlaying() == False):
			self.__isPlaying = False
			self.__debugMode("Not Playing")	
		# end if

	# end update


	# (PUBLIC) : toggle debug mode on /off
	# takes one argument
	# val -- true/false
	# no return value
	def setDebug(val):
		self.__debugOn = val
	# end setDebug

# end class SoundUtil



