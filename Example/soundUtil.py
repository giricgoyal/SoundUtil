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
	
	ONCE = 2
	NONE = 3
	LOOP = 7

	FREQUENT_CONSTANT = 8
	FREQUENT_RANDOM = 9

	RANDOM_FULL = 4
	RANDOM_CONSTANT = 5
	RANDOM_LOOP = 6

	def getOption(self, val):
		if val == "ONCE":
			return self.ONCE
		elif val == "NONE":
			return self.NONE
		elif val == "LOOP":
			return self.LOOP
		elif val == "FREQUENT_RANDOM":
			return self.FREQUENT_RANDOM
		elif val == "FREQUENT_CONSTANT":
			return self.FREQUENT_CONSTANT
		elif val == "RANDOM_FULL":
			return self.RANDOM_FULL
		elif val == "RANDOM_CONSTANT":
			return self.RANDOM_CONSTANT
		elif val == "RANDOM_LOOP":
			return self.RANDOM_LOOP
		# end if
		return -1

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
	__endTime = -1			# (int)		end time of play	(in seconds)

	__program = SoundCons.ONCE			# (int)		set the program of the sound.
							# possible values:
							# RANDOM, CUSTOM

	__randomTime = -1		# (int)		time variable for random function
	__randomDt = -1			# (int)		delta time for random function
	__randomSeed = -1		# (int)		seed variable for random function
	__randomLevel = SoundCons.RANDOM_FULL		# (int)		level of randomness
	__randomVolume = 1.0 	# (float)	volume level

	__frequency = 1 		# (int)		frequency per minute. Default is 1
	__timeStamp = 'm'		# c, m , h 	second, minute or hour. Default is m
	__timeGap = 0			# time gap (int)
	__frequencyCounter = 0	# counter for frequency (int) use when program is FREQUENT_RANDOM


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


	# (PRIVATE) : parse the input string for program
	# takes one argument
	# > string -- input string
	# no return value
	def __parseInput(self, input):
		inputArr = input.strip().split("-")
		for eachInput in inputArr:
			if (eachInput.strip() != ""):
				tempArr = eachInput.strip().split(" ")
				if len(tempArr) == 1:
					flag = tempArr[0].strip()
					value = None
				else:
					flag = tempArr[0].strip()
					value = tempArr[1].strip()
				# end if

				# Flags:
				#
				# -p : set Program
				# -s : set start time
				# -e : set end time
				# -t : random time index (int)
				# -f : radnom seed index (float)
				# -v : set volume
				# -r : frequency
				# -o : time Stamp. Prequency per time stamp, hr, min or sec

				if (flag == 'p'):
					if value == None:
						self.__program = SoundCons.RANDOM_FULL
					else:
						if (SoundCons.getOption(SoundCons(), value) != -1):
							self.__program = SoundCons.getOption(SoundCons(), value)
						else:
							print ("No Program Found. Using RANDOM_FULL")
							self.__program = RANDOM_FULL
						# end if
					# end if
				elif (flag == 's'):
					if value == None:
						self.__startTime = 0
					else:
						self.__startTime = 0 if (int(value) < 0) else int(value)
					# end if
				elif (flag == 'e'):
					if value == None:
						self.__endTime = -1
					else:
						self.__endTime = -1 if (int(value) <= 0) else int(value)
					# end if
				elif (flag == 't'):
					if value == None:
						self.__randomTime = random.randrange(9, 101, 5)
					else:
						self.__randomTime = random.randrange(9, 101, 5) if (int(value) < 0) else int(value)
					# end if
				elif (flag == 'f'):
					if value == None:
						self.__randomSeed = random.random()
					else:
						self.__randomSeed = random.random() if (float(value) < 0) else float(value)
					# end if
				elif (flag == 'v'):
					if value == None:
						self.__randomVolume = 1.0
					else:
						self.__randomVolume = 1.0 if (float(value) < 0) else float(value)
					# end if
				elif (flag == 'r'):
					if value == None:
						self.__frequency = 1
					else:
						self.__frequency = 1 if (int(value) < 0) else int(value)
					# end if
				elif (flag == 'o'):
					self.__randomDt = 0
					if value == None:
						self.__timeStamp = 'min'
						self.__timeGap = 60/self.__frequency if (self.__program == SoundCons.FREQUENT_CONSTANT) else 60
					elif (value == "hr"):
						self.__timeStamp = 'hr'
						self.__timeGap = 3600/self.__frequency if (self.__program == SoundCons.FREQUENT_CONSTANT) else 3600
					elif (value == "min"):
						self.__timeStamp = 'min'
						self.__timeGap = 60/self.__frequency if (self.__program == SoundCons.FREQUENT_CONSTANT) else 60
					elif (value == 'sec'):
						self.__timeStamp = 'sec'
						self.__timeGap = 0
					# end if
				# end if
				self.__debugMode(str(flag) + " : " + str(value))
		
			# end if
		# end for 
	# end __parseInput

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

	# Flags:
	#
	# -p : set Program
	# -s : set start time
	# -e : set end time
	# -l : random program level/type
	# -t : random time index (int)
	# -f : radnom seed index (float)
	# -v : set volume

	# pass one argument to set only the start time
	# no return value
	def setProgram(self, input):
		self.__parseInput(input)

		if (self.__program == SoundCons.ONCE):
			if (self.__startTime > self.__endTime) and (self.__startTime != 0):
				self.__endTime = -1
			# end if

		elif (self.__program == SoundCons.RANDOM_LOOP):
			self.__soundInstance.setLoop(True)
			self.__soundInstance.play()

		elif (self.__program == SoundCons.LOOP):
			self.__soundInstance.setLoop(True)
			self.__soundInstance.__setPlay(True)

		elif (self.__program == NONE):
			self.__soundInstance.__setPlay(True)

		elif (self.__program == SoundCons.FREQUENT_CONSTANT) or (self.__program == SoundCons.FREQUENT_RANDOM):
			if (self.__startTime == 0):
				random.seed()
				if (self.__timeStamp == "hr"):
					self.__startTime = random.randrange(0,3601)
				elif (self.__timeStamp == "min"):
					self.__startTime = random.randrange(0,61)
				elif (self.__timeStamp == "sec"):
					self.__startTime = random.randrange(0,1)
			# end if
		# end if
	# end setProgram

	'''
	def setProg(self, program, list = None):
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
	'''


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
		#self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))

		# If no hostObj then dont update position.
		if (self.__hostObj != None):
			# Update position
			self.setSoundPosition(self.__hostObj.getPosition())
		# end if

		# use __program to identify how to play the sound
		if (self.__program == SoundCons.RANDOM_FULL) or (self.__program == SoundCons.RANDOM_LOOP) or (self.__program == SoundCons.RANDOM_CONSTANT):
			self.__debugMode(str(self.__randomTime))
			if ((t - self.__randomDt) > self.__randomTime):
				self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))

				self.__randomDt = t
				random.seed()
				if (self.__program == SoundCons.RANDOM_FULL):
					self.__randomTime = random.randrange(9, 101, 5)
					self.__randomSeed = random.random()
				# end if
				num = random.random()
				if (self.__program == SoundCons.RANDOM_LOOP):
					if num > self.__randomSeed:
						self.__soundInstance.setVolume(self.__randomVolume)
					else:
						self.__soundInstance.setVolume(0.0)
					# end if
				else:
					if num > self.__randomSeed:
						if (self.__isPlaying == False):
							self.__setPlay(True)
						# end if
					# end if
				# end if
			# end if

		elif self.__program == SoundCons.ONCE:
			# Play within time interval
			if (self.__startTime != 0) and (self.__endTime != 0):
				if (((int(t) >= self.__startTime) and (int(t) <= self.__endTime)) and (self.__isPlaying == False)):
					# start playing from start till end
					self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
					self.__setPlay(True)
				# end if
				if (((int(t) >= self.__startTime) and (self.__endTime == -1)) and (self.__isPlaying == False)):
					# start playing from start till it finishes playing
					self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
					self.__setPlay(True)
				# end if
				if ((int(t) >= self.__endTime) and (self.__endTime != -1) and (self.__isPlaying == True)):
					# stop after t
					self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
					self.__setPlay(False)
				# end if
				if ((int(t) < self.__startTime) and (self.__isPlaying == True)):
					# stop playing otherwise
					self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
					self.__setPlay(False)
				# end if
			elif (((self.__startTime == 0) and (self.__endTime == -1)) and (self.__isPlaying == False)):
				# start playing from 0 till it finishes playing
				self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
				self.__setPlay(True)
			# end if

		elif self.__program == SoundCons.LOOP:
			if (self.__isPlaying == False):
				self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
				self.__soundInstance.__setPlay(True)
			#self.__debugMode("Playing : LOOP")

		elif (self.__program == SoundCons.FREQUENT_CONSTANT) or (self.__program == SoundCons.FREQUENT_RANDOM):
			self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
			if (int(t) >= self.__startTime):
				self.__soundInstance.__setPlay(True)
				if (self.__program == SoundCons.FREQUENT_CONSTANT):
					if (int(t) - self.__randomDt >= self.__timeGap)
						self.__randomDt = int(t)
						if self.__isPlaying == False:
							self.__soundInstance.__setPlay(True)
						# end if
					# end if
				else:
					if (int(t) - self.__randomDt <= self.__timeGap): 
						if (self.__frequencyCounter <= self.__frequency):
							num = random.random()
							if (num <= self.__timeGap/self.__frequency):
								self.__frequencyCounter = self.__frequencyCounter + 1

								if self.__isPlaying == False:
									self.__soundInstance.__setPlay(True)	
								# end if
							# end if
					else:
						self.__randomDt = int(t)
						self.__frequencyCounter = 0
					# end if
			# end if
		# end 


		
		if self.__soundInstance.isPlaying() == True:
			self.__isPlaying = True
			#self.__debugMode("Still playing")
		# end if
		
		if (self.__soundInstance.isPlaying() == False):
			self.__isPlaying = False
			#self.__debugMode("Not Playing")	
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


