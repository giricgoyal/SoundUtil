from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *
import random


class Sound:
	__soundEnv = getSoundEnvironment()	# container for sound environment
	__mm = MenuManager.createAndInitialize()
	__mainMenu = __mm.getMainMenu()
	
	__debugSound = None
	__debugSoundContainer = None

	__moreSoundOptions = None
	__moreSoundOptionsContainer = None

	__menuDebugToggle = None

	__buttonList = dict()
	__soundInstances = dict()

	__font = "/soundUtil/bin/helvetica.ttf"


	__WAND1 = 1
	__WAND2 = 2

	__wandPosition1 = None
	__wandOrientation1 = None
	
	__wandPosition2 = None
	__wandOrientation2 = None

	__totalButtons = 0
	__startButton = 0
	__endButton = 0
	
	@staticmethod
	def initSoundSubMenu():
		#Level1 menu

		Sound.__debugSound = Sound.__mainMenu.addSubMenu("Debug Sound")
		Sound.__debugSoundContainer = Sound.__debugSound.addContainer().getContainer()
		Sound.__debugSoundContainer.setLayout(ContainerLayout.LayoutVertical)
		Sound.__debugSoundContainer.setHorizontalAlign(HAlign.AlignLeft)

		Sound.__moreSoundOptions = Sound.__mainMenu.addSubMenu("Sound Options")
		Sound.__moreSoundOptionsContainer = Sound.__moreSoundOptions.addContainer().getContainer()
		Sound.__moreSoundOptionsContainer.setLayout(ContainerLayout.LayoutVertical)
		Sound.__moreSoundOptionsContainer.setHorizontalAlign(HAlign.AlignLeft)

		Sound.__menuDebugToggle = Button.create(Sound.__moreSoundOptionsContainer)
		Sound.__menuDebugToggle.setText("Debug Mode")
		Sound.__menuDebugToggle.setCheckable(True)
		Sound.__menuDebugToggle.setChecked(True)
		Sound.__menuDebugToggle.setUIEventCommand('buttonCallBack()')
		Sound.addToButt0nList("DebugSoundMode", Sound.__menuDebugToggle)
	
	@staticmethod
	def getDebugS0undVar():
		return Sound.__debugSoundContainer

	@staticmethod
	def getButt0nList():
		return Sound.__buttonList

	@staticmethod
	def addToButt0nList(name, button):
		Sound.__buttonList[name] = button
		Sound.__totalButtons += 1

	@staticmethod
	def updateS0undFromDebugMenu():	
		for sound, button in Sound.getButt0nList().iteritems():
			if (sound != "DebugSoundMode"):
				if button.isChecked() == False:
					Sound.getS0undInstance(sound).setMute(True)
					text = button.getLabel()
					text.setText(text.getText().replace("(Un-Muted) : ", "(Muted) : "))
					button.setFillColor(Color('#FF1111FE'))
				
				else:
					Sound.getS0undInstance(sound).setMute(False)
					text = button.getLabel()
					button.getLabel().setColor(Color('#eeee11ee'))
					text.setText(text.getText().replace("(Muted) : ", "(Un-Muted) : "))
					button.setFillColor(Color('#111111FE'))
			else:
				if (button.isChecked() == False):
					for sound, instance in Sound.getSoundInstances().iteritems():
						instance.setDebug(False)
				else:
					for sound, instance in Sound.getSoundInstances().iteritems():
						instance.setDebug(True)

	@staticmethod
	def updateEvent(event):
		#if (event.getServiceType() == ServiceType.Mocap):
		if (event.getSourceId() == Sound.__WAND1):
			Sound.__wandPosition1 = event.getPosition()
			Sound.__wandOrientation1 = event.getOrientation()
		if (event.getSourceId() == Sound.__WAND2):
			Sound.__wandPosition2 = event.getPosition()
			Sound.__wandOrientation2 = event.getOrientation()


	@staticmethod
	def getSoundInstances():
		return Sound.__soundInstances
			
	@staticmethod
	def getS0undInstance(name):
		return Sound.__soundInstances[name]

	@staticmethod
	def addToS0undInstances(name, sound):
		Sound.__soundInstances[name] = sound

	@staticmethod
	def getS0undEnv():
		return Sound.__soundEnv

	@staticmethod
	def getFont():
		return Sound.__font

	@staticmethod
	def setFont():
		return Sound.__font

	@staticmethod
	def getWand(wandId):
		#return Sound.__wandPosition1, Sound.__wandOrientation1
		if (wandId == Sound.__WAND1):
			return Sound.__wandOrientation1
		if (wandId == Sound.__WAND2):
			return Sound.__wandOrientation2
		return 1

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

	__debugOn = False		# (boolean)	for debugging purposes only, set to False for not debugging messages
	__sphere = None 		# (Shape) for debugging sound position
	__sphere2 = None
	__name = None 			# (text) for debugging sound position
	__posText = None 		# (text) for debugging sound position.
	__line = None 			# (line) for debugging sound position

	__soundInstance = None	# container for the sound instance
	__soundLoad = None		# container for loading sound
	__hostObj = None		# container for host object
	__soundFile = ""		# (string) file name/path

	__loopPlay = False		# (boolean)	play in loop
	__stereo = False			# (boolean)	play in stereo mode
	__isPlaying = False		# (boolean)	check is playing sound
	__isMuted = False 	# (boolean) attach the spheres to cam

	__startTime = 0			# (int)		start time of play	(in seconds)
	__endTime = -1			# (int)		end time of play	(in seconds)

	__programT = ""
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

	__showDebugWindow = False
	
	__options = ['p', 's', 'e', 't', 'f', 'v', 'r', 'o']

	__planeShape = None
	__volText = None
	__programText = None

	__nameText2 = None
	__posX = None
	__posY = None
	__posZ = None

	__startEndText = None

	__planeSceneNode  = None
	__sphereSceneNode = None

	
	__intersected = False
	# ------------------------------------------------------------------------------------
	# private data members



	# (PRIVATE) : constructor 1
	# takes three arguments
	# > hostObj -- the object to which you want to bind the sound to
	# > dir -- directory name in which you want to put the sound to
	# > soundFilePath -- path and name to the sound file.
	# no return value
	def __init__(self, dirc, soundFilePath, hostObj = None):
		# None if no hostObj
		__soundEnv = Sound.getS0undEnv()
		if __soundEnv != None:
			self.__hostObj = hostObj
			self.__soundLoad = __soundEnv.loadSoundFromFile(dirc, soundFilePath)
			self.__soundInstance = SoundInstance(self.__soundLoad)
			self.__soundInstance.setLoop(False)
			self.__soundFile = soundFilePath
			Sound.addToS0undInstances(self.__soundFile, self)
			self.__initDebugWindow()
			self.__addToDebugMenu()
			#self.__soundEnv.showDebugInfo(True)
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
			#if self.__isPlaying == False:
			if 1==1:
				self.__isPlaying = True
				if self.__stereo == True:
					self.__debugMode("Playing " + str(self.__soundFile) + " ; Vol " + str(self.__soundInstance.getVolume()))
					self.__debugMode("Position : " + str(self.__soundInstance.getPosition()))
					self.__debugMode("----");
					self.__soundInstance.playStereo()
				else:
					self.__debugMode("Playing " + str(self.__soundFile) + " ; Vol " + str(self.__soundInstance.getVolume()))
					self.__debugMode("Position : " + str(self.__soundInstance.getPosition()))
					self.__debugMode("----");
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
		if (self.__getDebugMode() == True):
			print "debug> " + str(text)
		# end if
	# end __debugMode


	def __errorMode(self, text):
		print "\n!!!!!!!!!!\n"
		print "------->\n" + text + "\n<-------\n"
		print "Exiting!!!!\n"
		exit(1)
	# end __errorMode()

	# (PRIVATE) : find errors in input string
	# takes one argument
	# > arr -- array of input
	# no return value
	def __reportError(self, arr):
		for i in range(0,len(arr)):
			if arr[i].strip() != "":
				if " " in arr[i].strip():
					if arr[i].strip().split(" ")[0] in self.__options:
						pass
					else:
						self.__errorMode("No such option as \"" + arr[i].strip().split(" ")[0] + "\" in \"" + self.__soundFile + "\".")
					# end if
				else:
					if arr[i].strip() in self.__options:
						self.__errorMode("Option/Value missing for \"" + arr[i].strip() + "\" in \"" + self.__soundFile + "\".")
					else:
						self.__errorMode("No such option as \"" + arr[i].strip() + "\" in \"" + self.__soundFile + "\"")
				# end if
			# end if
		# end for
	# end __reportError()

	def __getDebugMode(self):
		return self.__debugOn

	def __getProgramT(self):
		return self.__programT

	def __setProgramT(self, val):
		self.__programT = val


	# (PRIVATE) : parse the input string for program
	# takes one argument
	# > string -- input string
	# no return value
	def __parseInput(self, input):
		inputArr = input.strip().split("-")
		self.__reportError(inputArr)
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
							self.__setProgramT(value)
						else:
							print ("No Program Found. Using RANDOM_FULL")
							self.__program = RANDOM_FULL
							self.__setProgramT("RANDOM_FULL")
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
						self.__randomSeed = random.random() if ((int(value) < 0) or (int(value) > 100)) else float((float(100 - float(value))/100))
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


	# (PRIVATE) : shows the sound as a visual for debug purposes.
	# takes no argument
	# no return value
	def __showSound(self):
		self.__sphere.setEffect("colored -d #EEEE11EE")
		self.__planeShape.setEffect("colored -d #EEEE11EE")
	# end __showSound

	def __hideSound(self):
		self.__sphere.setEffect("colored -d #EE1111EE")
		self.__planeShape.setEffect("colored -d #EE1111EE")
	# end __hideSound

	def __updateSoundSpherePos(self):
		self.__sphere.setPosition(self.__soundInstance.getPosition())
		self.__name.setPosition(self.__sphere.getPosition() + Vector3(-0.5,0.5,0))
		self.__posText.setPosition(self.__name.getPosition() + Vector3(-0.5, -0.1, 0))
		
		self.__planeSceneNode.setPosition(self.__soundInstance.getPosition() + Vector3(1000, 0, 0))
		
		pos = "(x,y,z): (" + str(self.__soundInstance.getPosition().x) + "," + str(self.__soundInstance.getPosition().y) + "," + str(self.__soundInstance.getPosition().z) + ")"
		self.__posText.setText(str(pos))
		

	def __hideAll(self):
		self.__sphere.setPosition(getDefaultCamera().getPosition() + Vector3(1000, 0, 0))
		self.__posText.setPosition(getDefaultCamera().getPosition() + Vector3(1000, 0, 0))
		self.__name.setPosition(getDefaultCamera().getPosition() + Vector3(1000, 0, 0))
		self.__planeSceneNode.setPosition(getDefaultCamera().getPosition() + Vector3(1000, 0, 0))
	

	def __updatePlanePos(self):
		self.__planeSceneNode.setPosition(self.__soundInstance.getPosition())

		self.__sphere.setPosition(getDefaultCamera().getPosition() + Vector3(1000, 0, 0))
		self.__name.setPosition(self.__soundInstance.getPosition() + Vector3(1000, 0, 0))
		self.__posText.setPosition(self.__soundInstance.getPosition() + Vector3(1000, 0, 0))
		
		
		pos = self.__soundInstance.getPosition()
		self.__posText.setText(str(pos))
		self.__posX.setText("X: " + str(pos.x))
		self.__posY.setText("Y: " + str(pos.y))
		self.__posZ.setText("Z: " + str(pos.z))

		self.__programText.setText("Program: " + str(self.__getProgramT()))
		
		

	# end __updateSoundSpherePos
		

	# (PRIVATE) : adds the sound to debug menu
	# takes no argument
	# no return value
	def __addToDebugMenu(self):
		button = Button.create(Sound.getDebugS0undVar())
		button.setText(self.__soundFile)
		button.setCheckable(True)
		button.setChecked(True)
		button.setUIEventCommand('buttonCallBack()')
		button.setFillEnabled(True)
		button.setFillColor(Color('#111111FE'))
		Sound.addToButt0nList(self.__soundFile, button)

		text = button.getLabel()
		button.getLabel().setColor(Color('#eeee11ee'))
		text.setText(str("(Un-Muted) : ") + str(self.__soundFile))

		self.__debugMode("Added to the Debug Menu")
	# end __addToDebugMenu


	def __initDebugWindow(self):
	
		self.__sphere = SphereShape.create(0.5, 4)
		self.__sphere.getMaterial().setAlpha(0.4)
		self.__sphere.setEffect("colored -d #EEEE11EE")
		self.__sphere.getMaterial().setTransparent(True)

		self.__name = Text3D.create(Sound.getFont(), 1, str(self.__soundFile))
		self.__name.setFontSize(0.03)
		self.__name.setFontResolution(256)
		self.__name.getMaterial().setDoubleFace(1)
		self.__name.setFixedSize(False)
		self.__name.setColor(Color('white'))
		self.__name.setFacingCamera(getDefaultCamera())

		
		pos = "(x,y,z): (" + str(self.__soundInstance.getPosition().x) + "," + str(self.__soundInstance.getPosition().y) + "," + str(self.__soundInstance.getPosition().z) + ")"
		self.__posText = Text3D.create(Sound.getFont(), 1, str(pos))
		self.__posText.setFontSize(0.03)
		self.__posText.setFontResolution(256)
		self.__posText.getMaterial().setDoubleFace(1)
		self.__posText.setFixedSize(False)
		self.__posText.setColor(Color('white'))
		self.__posText.setFacingCamera(getDefaultCamera())


		self.__planeSceneNode = SceneNode.create(self.__soundFile + "PlaneSceneNode")

		self.__planeShape =  PlaneShape.create(1,0.5)
		self.__planeShape.setPosition(0, 0, -0.5)
		self.__planeShape.setEffect("colored -d #EEEE11EE")
		self.__showDebugWindow = False
		self.__planeSceneNode.addChild(self.__planeShape)
		
		self.__nameText2 = Text3D.create(Sound.getFont(), 1, str(self.__soundFile))
		self.__nameText2.setFontSize(0.03)
		self.__nameText2.setPosition(Vector3(-0.4, 0.18, -0.4))
		self.__nameText2.setFontResolution(256)
		self.__nameText2.getMaterial().setDoubleFace(1)
		self.__nameText2.setFixedSize(False)
		self.__nameText2.setColor(Color('white'))
		self.__planeSceneNode.addChild(self.__nameText2)

		self.__posX = Text3D.create(Sound.getFont(), 1, str(pos))
		self.__posX.setFontSize(0.03)
		self.__posX.setPosition(Vector3(-0.4, 0.12, -0.4))
		self.__posX.setFontResolution(256)
		self.__posX.getMaterial().setDoubleFace(1)
		self.__posX.setFixedSize(False)
		self.__posX.setColor(Color('white'))
		self.__planeSceneNode.addChild(self.__posX)

		self.__posY = Text3D.create(Sound.getFont(), 1, str(pos))
		self.__posY.setFontSize(0.03)
		self.__posY.setPosition(Vector3(-0.4, 0.06, -0.4))
		self.__posY.setFontResolution(256)
		self.__posY.getMaterial().setDoubleFace(1)
		self.__posY.setFixedSize(False)
		self.__posY.setColor(Color('white'))
		self.__planeSceneNode.addChild(self.__posY)

		self.__posZ = Text3D.create(Sound.getFont(), 1, str(pos))
		self.__posZ.setFontSize(0.03)
		self.__posZ.setPosition(Vector3(-0.4, 0, -0.4))
		self.__posZ.setFontResolution(256)
		self.__posZ.getMaterial().setDoubleFace(1)
		self.__posZ.setFixedSize(False)
		self.__posZ.setColor(Color('white'))
		self.__planeSceneNode.addChild(self.__posZ)


		self.__volText = Text3D.create(Sound.getFont(), 1, "Volume: " + str(self.__randomVolume))
		self.__volText.setFontSize(0.03)
		self.__volText.setPosition(Vector3(-0.4, -0.06, -0.4))
		self.__volText.setFontResolution(256)
		self.__volText.getMaterial().setDoubleFace(1)
		self.__volText.setFixedSize(False)
		self.__volText.setColor(Color('white'))
		self.__planeSceneNode.addChild(self.__volText)
	
		self.__programText = Text3D.create(Sound.getFont(), 1, "Program: " + str(self.__getProgramT()))
		self.__programText.setFontSize(0.03)
		self.__programText.setPosition(Vector3(-0.4, -0.12, -0.4))
		self.__programText.setFontResolution(256)
		self.__programText.getMaterial().setDoubleFace(1)
		self.__programText.setFixedSize(False)
		self.__programText.setColor(Color('white'))
		self.__planeSceneNode.addChild(self.__programText)
		
		self.__planeSceneNode.setFacingCamera(getDefaultCamera())
		
	
	def __getShowDebug(self):
		return self.__showDebugWindow

	def __setShowDebug(self, val):
		self.__showDebugWindow = val



	# (PRIVATE) : update method for each sound instance
	# takes three arguments
	# > frame
	# > t
	# > dt
	# pass the arguments from the onUpdate method in your main file
	# no return value
	def __updateEach(self, frame, t, dt):
		#self.__debugMode("Updating position at : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))

		# If no hostObj then dont update position.
		if (self.__hostObj != None):
			# Update position
			self.setSoundPosition(self.__hostObj.getPosition())
		# end if

		# use __program to identify how to play the sound
		if (self.__program == SoundCons.RANDOM_FULL) or (self.__program == SoundCons.RANDOM_LOOP) or (self.__program == SoundCons.RANDOM_CONSTANT):
			if ((t - self.__randomDt) > self.__randomTime):
				self.__debugMode("frame, t, dt : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))

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
					self.__debugMode("frame, t, dt : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
					self.__setPlay(True)
				# end if
				if (((int(t) >= self.__startTime) and (self.__endTime == -1)) and (self.__isPlaying == False)):
					# start playing from start till it finishes playing
					self.__debugMode("frame, t, dt : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
					self.__setPlay(True)
				# end if
				if ((int(t) >= self.__endTime) and (self.__endTime != -1) and (self.__isPlaying == True)):
					# stop after t
					self.__debugMode("frame, t, dt : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
					self.__setPlay(False)
				# end if
				if ((int(t) < self.__startTime) and (self.__isPlaying == True)):
					# stop playing otherwise
					self.__debugMode("frame, t, dt : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
					self.__setPlay(False)
				# end if
			elif (((self.__startTime == 0) and (self.__endTime == -1)) and (self.__isPlaying == False)):
				# start playing from 0 till it finishes playing
				self.__debugMode("frame, t, dt : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
				self.__setPlay(True)
			# end if	
		
		elif ((self.__program == SoundCons.FREQUENT_CONSTANT) or (self.__program == SoundCons.FREQUENT_RANDOM)):
			self.__debugMode("frame, t, dt : " + str(frame) + " : " + str(int(t)) + " : " + str(dt))
			if (int(t) >= self.__startTime):
				self.__setPlay(True)
				if (self.__program == SoundCons.FREQUENT_CONSTANT):
					if ((int(t) - self.__randomDt) >= self.__timeGap):
						self.__randomDt = int(t)
						self.__setPlay(True)
						# end if
					# end if
				else:
					if ((int(t) - self.__randomDt) <= self.__timeGap): 
						if (self.__frequencyCounter <= self.__frequency):
							num = random.random()
							if (num <= (self.__timeGap/self.__frequency)):
								self.__frequencyCounter = self.__frequencyCounter + 1

								self.__setPlay(True)	
								# end if
							# end if
					else:
						self.__randomDt = int(t)
						self.__frequencyCounter = 0
					# end if
			# end if
		# end 

		#if self.__soundInstance.isDone() == True:
		#	self.__isPlaying = False
		# end if
		
		if (self.__soundInstance.isPlaying() == True):
			self.__isPlaying = True
			#self.__debugMode("Still playing")
		# end if
		
		if (self.__soundInstance.isPlaying() == False):
			self.__isPlaying = False
			#self.__debugMode("Not Playing")	

		# end if
		
		if (self.__getDebugMode() == True):
			if (self.__getShowDebug() == False):
				self.__updateSoundSpherePos()
			else:
				self.__updatePlanePos()

			if (self.__isMuted == True):
				self.__soundInstance.setVolume(0)
			else:	
				self.__soundInstance.setVolume(self.__randomVolume)
			
		else:
			self.__hideAll()
			
	# end update




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
			self.__setPlay(True)

		elif (self.__program == SoundCons.LOOP):
			self.__soundInstance.setLoop(True)
			self.__setPlay(True)

		elif (self.__program == SoundCons.NONE):
			self.__setPlay(True)

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

	# (PUBLIC) : set Loop play
	# takes one argument
	# > val -- True (play in loop) or False (don't play in loop)
	# no return value
	def setLoop(self, val):
		self.__soundInstance.setLoop(val)
	# end setLoop


	# (PUBLIC) : toggle debug mode on /off
	# takes one argument
	# val -- true/false
	# no return value
	def setDebug(self, val, color = "#DDDD11ee"):
		self.__debugOn = val
			
	# end setDebug


	def setMute(self, val):
		if val == True:
			self.__soundInstance.setVolume(0)
			self.__hideSound()
			self.__isMuted = True
			self.__debugMode("Muted " + str(self.__soundFile) + " ; Vol " + str(self.__soundInstance.getVolume()))
			self.__debugMode("Position : " + str(self.__soundInstance.getPosition()))		
		else:
			self.__soundInstance.setVolume(self.__randomVolume)
			self.__showSound()
			self.__isMuted = False
			self.__debugMode("UnMuted " + str(self.__soundFile) + " ; Vol " + str(self.__soundInstance.getVolume()))
			self.__debugMode("Position : " + str(self.__soundInstance.getPosition()))
			# end if
	# end setMute

	def checkIntersection(self, ray):
		print ray
		hitdata = hitNode(self.__sphere, ray[1], ray[2])
		if (hitdata[0]):
			self.__debugMode("Intersect With : " + str(self.__soundFile))
			return True
		return False

	def isDebugOn(self):
		return self.__debugOn


	@staticmethod
	def update(frame, t, dt):
		for sound, instance in Sound.getSoundInstances().iteritems():
			instance.__updateEach(frame, t, dt)


	@staticmethod
	def updateEvent(event):
		if (event == None):
			return
		else:			
			Sound.updateEvent(event)
			if (event.getServiceType() == ServiceType.Wand):
				if (event.isButtonDown(EventFlags.Button5)):
					print "button pressed"
					
					#wandOrientation = Sound.getWand(event.getSourceID())
					ray = getRayFromEvent(event)
					#ray = Ray3(Point3(getDefaultCamera().getPosition().x, getDefaultCamera().getPosition().y, getDefaultCamera().getPosition().z), (getDefaultCamera().getOrientation() * event.getOrientation()) * Vector3(0,0,-1))
					instances = Sound.getSoundInstances()
					
					for name, sound in instances.iteritems():
						if ((sound.checkIntersection(ray) == True) and (sound.isDebugOn() == True)):
							print "Intersect"
							sound.__setShowDebug(True)
						else:
							sound.__setShowDebug(False)
					
				elif (event.isButtonUp(EventFlags.Button5)):
					print "button released"
					instances = Sound.getSoundInstances()
					for name, sound in instances.iteritems():
						sound.__setShowDebug(False)
# end class SoundUtil


def buttonCallBack():
	Sound.updateS0undFromDebugMenu()


Sound.initSoundSubMenu()



