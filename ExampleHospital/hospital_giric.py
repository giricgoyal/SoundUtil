# simple environment to test sounds for the HANDS nursing study
# copyright 2013 evl

# current issues
# need to turn off head tracking
# need to add a copy machine sound
# move sounds to their own subfolder

from math import *
from euclid import *
from omega import *
from cyclops import *
from omegaToolkit import *
import time
import random
from soundUtil import *

scene = getSceneManager()
cam = getDefaultCamera()

scene.setBackgroundColor(Color(0, 0, 0, 1))

# this doesnt seem to do anything
#ss = ShadowSettings()
#ss.shadowsEnabled = True
#scene.resetShadowSettings(ss)


setNearFarZ(0.1, 200) #1000

everything = SceneNode.create('everything')

# Load hospital model
torusModel = ModelInfo()
torusModel.name = "torus"
torusModel.path = "hospital_all_modified-notable-newtexs-bin.fbx"
#torusModel.path = "hospitalTempFBX.fbx"
#torusModel.path = "hospital_all_modified-notable.fbx"
scene.loadModel(torusModel)
torusModel.generateNormals = True
torusModel.optimize = True

# Create a scene object using the loaded model
torus = StaticObject.create("torus")
#torus.setEffect("textured")
torus.getMaterial().setDoubleFace(1)
torus.getMaterial().setProgram("textured")
torus.getMaterial().setGloss(0)
torus.getMaterial().setShininess(0)
torus.setScale(Vector3(0.3048, 0.3048, 0.3048))
torus.yaw(radians(180.0))

everything.addChild(torus)

# this puts floor of scene above floor of cave, but it looks better
everything.setPosition(Vector3(0, 0.4, 0))

# test for adding in the people as separate objects
# going from sketchup -> fbx had flickering issues with Tommy
# hadn't tried moving Tommy in before - could also try to group him

def addPerson (modelName, modelPath, px, py, pz, rot, sx, sy, sz):
	tModel = ModelInfo()
	tModel.name = modelName
	tModel.path = modelPath
	scene.loadModel(tModel)
	tModel.generateNormals = True
	tModel.optimize = True

	t = StaticObject.create(modelName)
	t.setPosition(Vector3(px, py, pz))
	t.setEffect("textured")
	t.getMaterial().setDoubleFace(1)
	t.setScale(Vector3(0.011*sx, 0.011*sy, 0.011*sz))
	t.yaw(radians(rot))

	everything.addChild(t)

# coordinate system from the user's point of view at the work tablen
# +X to the right
# +Y up
# +Z behind me

addPerson("womanSitting", "Woman-sitting-scrubs.fbx",        -2.4, 0.05, -1.32,  90, 0.7, 0.7, 0.7);
addPerson("ManSitting", "2D_Man_Sitting2-scrubs.fbx",         6.4, 0.324, -1.31, 90, 0.7, 0.7, 0.7);

addPerson("ManWithWatch", "Tommy-scrubs.fbx",                        2, 0, -2.5, 0, 1, 1, 1);
addPerson("TwoBusinessMen", "2D_Group_BusinessMen-scrubs.fbx",      -7, 0, -6,   0, 1, 1, 1);
addPerson("BusinessMan", "2D_Man_Business-scrubs.fbx",            -3.5, 0, -3.5, 0, 1, 1, 1);

addPerson("WhiteCoat", "2D_Man_Casual-scrubs.fbx",                   9, 0, 1,   90, 1, 1, 1);
addPerson("ManWithCoffee", "2D_Man_Standing_John-scrubs.fbx",       10, 0, 0.5, 90, 1, 1, 1);
addPerson("ManWithPhone", "2D_Man_Walking_Side-scrubs.fbx",         -7, 0, -1, -90, 1, 1, 1);
addPerson("WomanCoffee", "2D_Woman_CoffeeCup-scrubs.fbx",           -6, 0, 0,  -90, 1, 1, 1);

addPerson("WomanJacket", "2D_Woman_Front-scrubs.fbx",                4, 0, -0.6, 90, 1, 1, 1);
addPerson("WomanBook", "2D_Woman_Standing_Book-scrubs.fbx",          9, 0, -2, 90, 1, 1, 1);
addPerson("WomanArmsAtSides", "2D_Woman_Standing_Denise-scrubs.fbx", 8, 0, 0,  90, 1, 1, 1);
addPerson("WomanArmsCrossed", "2D_Woman_Standing_Front-scrubs.fbx", -5, 0, -2, 90, 1, 1, 1);
addPerson("WomanBox", "2D_Woman_Standing_Sandra-scrubs.fbx",        -6, 0, 1,  90, 1, 1, 1);

# lights

light1 = Light.create()
#smap1 = ShadowMap()                                                                   
#light1.setShadow(smap1)                                                               
light1.setColor(Color(0.3, 0.3, 0.3, 1))
light1.setLightType(LightType.Directional)
light1.setLightDirection(Vector3(0.4, 0.2, 0.2))
light1.setEnabled(True)

light2 = Light.create()
#smap2 = ShadowMap()                                                                   
#light2.setShadow(smap2)                                                               
light2.setColor(Color(0.19, 0.19, 0.18, 1))
light2.setLightType(LightType.Directional)
light2.setLightDirection(Vector3(-1.5, -0.5, -1))
light2.setEnabled(True)

light3 = Light.create()
#smap3 = ShadowMap()                                                                   
#light3.setShadow(smap3)                                                               
light3.setColor(Color(0.2, 0.2, 0.2, 1))
light3.setPosition(Vector3(0, 10, 0))
light3.setEnabled(True)


# Setup sound environment
                 

soundUpdateList = []                 
soundFactor = 0.2

'''
def addSound (instance, sx, sy, sz, vol):
        time.sleep(1)
        simusic = SoundInstance(instance)
        simusic.setPosition(Vector3(sx, sy, sz))
        simusic.setLoop(True)
        simusic.setVolume(vol * soundFactor)
        simusic.play()

se = getSoundEnvironment()
if (se != None):
'''


station1 = SoundUtil("nurses", "SOUNDS/nursesstationMONO.wav")
station1.setSoundPosition(Vector3(-3, 1, 1))
station1.setProgram("-p LOOP -v "+str(0.3 * soundFactor))
station1.setDebug(True)
soundUpdateList.append(station1)

station2 = SoundUtil("visiting", "SOUNDS/visitinghoursMONO.wav")
station2.setSoundPosition(Vector3(3, 1, 1))
station2.setProgram("-p LOOP -v "+str(0.3 * soundFactor))
station2.setDebug(True)
soundUpdateList.append(station2)

station3 = SoundUtil("interior", "SOUNDS/hospitalinteriorMONO.wav")
station3.setSoundPosition(Vector3(1, 1, -3))
station3.setProgram("-p LOOP -v "+str(1.5 * soundFactor))
station3.setDebug(True)
soundUpdateList.append(station3)

station5 = SoundUtil("hallway", "SOUNDS/hospitalhallwayMONO.wav")
station5.setSoundPosition(Vector3(1, 1, 3))
station5.setProgram("-p LOOP -v "+str(0.3 * soundFactor))
station5.setDebug(True)
soundUpdateList.append(station5)


'''
        station1 = se.loadSoundFromFile('nurses', 'SOUNDS/nursesstationMONO.wav')
    addSound(station1, -3, 1, 1, 0.3)

        station2 = se.loadSoundFromFile('visiting', 'SOUNDS/visitinghoursMONO.wav')
    addSound(station2, 3, 1, 1, 0.3)

        station3 = se.loadSoundFromFile('interior', 'SOUNDS/hospitalinteriorMONO.wav')
    addSound(station3, 1, 1, -3, 1.5)

        station5 = se.loadSoundFromFile('hallway', 'SOUNDS/hospitalhallwayMONO.wav')
    addSound(station2, 1, 1, 3, 0.3)
    

# incidental sounds that should randomly start/stop
# can leave them looping and just turn the volume up/down
    
    global timusic, pimusic, dimusic, eimusic, cimusic

        
        device1 = se.loadSoundFromFile('typing', 'SOUNDS/typingMONO.wav')
        time.sleep(1)
        timusic = SoundInstance(device1)
        timusic.setPosition(Vector3(0, 1, -3))
        timusic.setLoop(True)
        timusic.setVolume(0.0 * soundFactor)
        timusic.play()

        device2 = se.loadSoundFromFile('phone', 'SOUNDS/phoneringingMONO.wav')
        time.sleep(1)
        pimusic = SoundInstance(device2)
        pimusic.setPosition(Vector3(-3, 1, 0))
        pimusic.setLoop(True)
        pimusic.setVolume(0.0 * soundFactor)
        pimusic.play()

        
        device3 = se.loadSoundFromFile('printing', 'SOUNDS/dotmatrixprinterMONO.wav')
        time.sleep(1)
        dimusic = SoundInstance(device3)
        dimusic.setPosition(Vector3(3, 1, 0))
        dimusic.setLoop(True)
        dimusic.setVolume(0.0 * soundFactor)
        dimusic.play()

        device4 = se.loadSoundFromFile('elevator', 'SOUNDS/elevatordoorMONO.wav')
        time.sleep(1)
        eimusic = SoundInstance(device4)
        eimusic.setPosition(Vector3(2, 1, 3))
        eimusic.setLoop(False)
        eimusic.setVolume(0.7 * soundFactor)
        

        device5 = se.loadSoundFromFile('codeblue', 'SOUNDS/codeblueMONO.wav')
        time.sleep(1)
        cimusic = SoundInstance(device5)
        cimusic.setPosition(Vector3(-2, 1, -3))
        cimusic.setLoop(False)
        cimusic.setVolume(0.7 * soundFactor)
        '''

device1_New = SoundUtil("typing", "SOUNDS/typingMONO.wav")
time.sleep(1)
device1_New.setProgram("-p RANDOM_LOOP -t 60 -f 30 -v "+str(0.5*soundFactor))
device1_New.setSoundPosition(Vector3(0, 1, -3))
device1_New.setDebug(True)
soundUpdateList.append(device1_New)


device2_New = SoundUtil("phone", "SOUNDS/phoneringingMONO.wav")
time.sleep(1)
device2_New.setProgram("-p RANDOM_LOOP -t 15 -f 30 -v "+str(0.6*soundFactor))
device2_New.setSoundPosition(Vector3(3, 1, 0))
device2_New.setDebug(True)
soundUpdateList.append(device2_New)

device3_New = SoundUtil("printing", "SOUNDS/dotmatrixprinterMONO.wav")
time.sleep(1)
device3_New.setProgram("-p RANDOM_LOOP -t 60 -f 50 -v "+str(1.0*soundFactor))
device3_New.setSoundPosition(Vector3(-3, 1, 0))
device3_New.setDebug(True)
soundUpdateList.append(device3_New)

device4_New = SoundUtil("elevator", "SOUNDS/elevatordoorMONO.wav")
time.sleep(1)
device4_New.setProgram("-p RANDOM_CONSTANT -t 60 -f 20 -v "+str(0.7*soundFactor))
device4_New.setSoundPosition(Vector3(2, 1, 3))
device4_New.setDebug(True)
soundUpdateList.append(device4_New)

device5_New = SoundUtil("codeblue", "SOUNDS/codeblueMONO.wav")
time.sleep(1)
device5_New.setProgram("-p RANDOM_CONSTANT -t 120 -f 5 -v "+str(0.7*soundFactor))
device5_New.setSoundPosition(Vector3(-2, 1, -3))
device5_New.setDebug(True)
soundUpdateList.append(device5_New)
        



oldD = 0
oldP = 0
oldT = 0
oldE = 0
oldC = 0
random.seed()
'''
def updateDotMatrix():
    global soundFactor
    num = random.random()
    if (num > 0.7):
        dimusic.setVolume(0.5 * soundFactor)
    else:
        dimusic.setVolume(0.0 * soundFactor)

def updatePhone():
    global soundFactor
    num = random.random()
    if (num > 0.7):
        pimusic.setVolume(0.6 * soundFactor)
    else:
        pimusic.setVolume(0.0 * soundFactor)

def updateTyping():
    global soundFactor
    num = random.random()
    if (num > 0.5):
        timusic.setVolume(1.0 * soundFactor)
    else:
        timusic.setVolume(0.0 * soundFactor)

def updateElevator():
    global soundFactor
    num = random.random()
    if (num > 0.8):
        eimusic.play()

def updateCodeblue():
    global soundFactor
    num = random.random()
    if (num > 0.95):
        cimusic.play() 
'''


def onUpdate(frame, t, dt):

    '''
    global oldT, oldP, oldD, oldC, oldE

    if (t - oldD) > 60:
            oldD = t
        updateDotMatrix()

    if (t - oldP) > 15:
            oldP = t
            updatePhone()
    
    if (t - oldT) > 60:
            oldT = t
            updateTyping()
    
    if (t - oldE) > 60:
            oldE = t
            updateElevator()

    if (t - oldC) > 120:
            oldC = t
            updateCodeblue()
    '''

    for soundObj in soundUpdateList:
        soundObj.update(frame, t, dt)

setUpdateFunction(onUpdate)

# set the scene to be monoscopic
getDisplayConfig().stereoMode = StereoMode.Mono

# camera position manually determined with tracking turned on                     
getDefaultCamera().setPosition(Vector3(-0.75, 0, 0))

# camera position is where you feet are, offset is where your head is   
# which should be like 1.2m
getDefaultCamera().setHeadOffset(Vector3(0, 1.2, 0))


#lock down the camera location (kind of works)
getDefaultCamera().setTrackingEnabled(False)

#turn off camera navigation
getDefaultCamera().setControllerEnabled(True)

#getDefaultCamera().addChild(everything)
