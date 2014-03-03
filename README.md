SoundUtil
=========


Sound Module to help better manage the sound for CAVE2 omegalib applications.

The module is written in python.
-----------------------------------------------------------------------------

Features: 


1. Attach sounds to scene nodes. This updated the sound position when the scene nodes update.
2. Set programs for the sounds like, play them randomly, play them at a constant interval, play sounds once after an interval. (All the current programs are listed under.)


How to use:

1.  Create an Object of SoundUtil.
      soundObject = SoundUtil(String directory, String path_to_soundfile, Object_to_attach_sound_to)

2.  Handle sound program and options. (More information on programs and available options below).

3.  Use SoundUtil's update method to update the sound with the object. Call the sound Util's Update method in your update method.
    
    def update (frame, t, dt):   
            soundObject.update(frame, t, dt)


You can read about the method directory at the wiki page.
<https://github.com/giricgoyal/SoundUtil/wiki>





  

