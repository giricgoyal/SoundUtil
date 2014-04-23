from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *
from soundUtil import *


scene = getSceneManager()
cam = getDefaultCamera()

m = MenuManager.createAndInitialize()
mainMen = m.getMainMenu()

scene.setBackgroundColor(Color(0, 0, 0, 1))

light = Light.create()
light.setLightType(LightType.Point)


sphere = SphereShape.create(0.1,4)
sphere.getMaterial().setAlpha(0.5)
sphere.setPosition(Vector3(0,0,-1))
sphere.getMaterial().setProgram("colored")
sphere.setEffect('colored -e #88000099')

box = BoxShape.create(1,3,1)
box.getMaterial().setAlpha(0.5)
box.setPosition(Vector3(0,1,-5))
box.getMaterial().setProgram("colored")
box.setEffect('colored -e #00008899')

se = getSoundEnvironment()

obj1 = SoundUtil("test", "codeblueMONO.wav", sphere)
#obj1.setLoop(True)
obj1.setProgram("-p RANDOM_CONSTANT -t 10 -f 95 -v "+str(2*1.0))
obj1.setDebug(True)

#sound1 = se.loadSoundFromFile("test", "hospitalbackgroundMONO.wav")

theta = 0
r1 = 100
r2 = 50

count = 0

def onUpdate(frame, t, dt):
	global count
	global theta, r

	count = count + 1
	if count % 60*30 == 0:
		if theta > 360:
			theta = 0
		else:
			pass
		x = r1 * cos(theta)
		z = r2 * sin(theta)
		theta = theta + t/2
		#sphere.setPosition(Vector3(1+count/60, 0, 0))
		#obj1.update(frame, t, dt)
		SoundUtil.update(frame, t, dt)

def onEvent():
	e = getEvent()
	SoundUtil.updateEvent(e)

'''
def onDraw(displaySize, tileSize, camera, painter):
	SoundUtil.updateDraw(displaySize, tileSize, camera, painter)
'''

setUpdateFunction(onUpdate)
setEventFunction(onEvent)
#setDrawFunction(onDraw)

