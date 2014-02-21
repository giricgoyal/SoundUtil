from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *
from soundUtil import *


scene = getSceneManager()
cam = getDefaultCamera()

scene.setBackgroundColor(Color(0, 0, 0, 1))

sphere = SphereShape.create(1,4)
sphere.getMaterial().setAlpha(0.5)
sphere.setPosition(Vector3(10,1,0))

box = BoxShape.create(1,3,1)
box.getMaterial().setAlpha(0.5)
box.setPosition(Vector3(0,1,-5))

se = getSoundEnvironment()

obj1 = SoundUtil("test", "hospitalbackgroundMONO.wav", sphere)
obj1.setLoop(True)
obj1.setProgram(SoundCons.RANDOM, [SoundCons.RANDOM_CONSTANT, 5, 0.80])
#obj1.setProgram(SoundCons.ONCE, [2, 5])


#sound1 = se.loadSoundFromFile("test", "hospitalbackgroundMONO.wav")

theta = 0
r1 = 100
r2 = 50

count = 0

def onUpdate(frame, t, dt):
	global count
	global theta, r

	count = count + 1
	if count % 60*5 == 0:
		if theta > 360:
			theta = 0
		else:
			pass
		x = r1 * cos(theta)
		z = r2 * sin(theta)
		theta = theta + t/2
		sphere.setPosition(Vector3(10+count/60, 0))
		obj1.update(frame, t, dt)


setUpdateFunction(onUpdate)
