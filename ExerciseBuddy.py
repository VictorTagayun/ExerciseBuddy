import asyncio
import cozmo
from Common.woc import WOC
from Common.colors import Colors
from os import system
import random
import _thread
import sys
import speech_recognition as sr
from threading import Timer

'''
Exercise Buddy Module
@class ExerciseBuddy
@author - Team Wizards of Coz
'''
class ExerciseBuddy(WOC):
    
    cl = None
    exit_flag = False
    audioThread = None
    liftThread = None
    lookThread = None
    direction = 1
    speed = 1
    tiredDuration = 15
    duration = 1
    cozmoSleeping = False
    startWorkout = False
    isTired = False
    tries = 0
    cubes = None
    
    def __init__(self, *a, **kw):
        
        sys.setrecursionlimit(0x100000)
        
        cozmo.setup_basic_logging()
        cozmo.connect(self.startResponding)
        
        
        
    def startResponding(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self.coz = coz_conn.wait_for_robot()
        
#         self.coz.world.add_event_handler(cozmo.objects.EvtObjectTapped, self.on_object_tapped)

#         self.coz.play_anim('anim_gotosleep_getout_02').wait_for_completed()
        self.coz.set_all_backpack_lights(Colors.GREEN)
        
        try:
            self.cubes = self.coz.world.wait_until_observe_num_objects(1, object_type = cozmo.objects.LightCube,timeout=60)
        except asyncio.TimeoutError:
            print("Didn't find a cube :-(")
            return
        finally:
            self.cubes[0].set_lights(Colors.GREEN);
            print("found!!")
        
        self.audioThread = _thread.start_new_thread(self.startAudioThread, ())
        
        
        while not self.exit_flag:
            asyncio.sleep(0)
        self.coz.abort_all_actions()
    
    
    
    def startAudioThread(self):
        try:
            print("Take input");
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.startListening())
        except Exception as e:
            print(e)
            
            
            
    def on_object_tapped(self, event, *, obj, tap_count, tap_duration, tap_intensity, **kw):
        print(obj == self.cubes[0])
        if(obj == self.cubes[0]):
            self.increaseSpeed()
    
    
    
    async def startListening(self):
        if not self.cozmoSleeping:
            print("Taking input");
            r = sr.Recognizer()
            r.energy_threshold = 5000
            print(r.energy_threshold)
            with sr.Microphone(chunk_size=512) as source:
                audio = r.listen(source)
            try:
                speechOutput = r.recognize_google(audio)
                print(speechOutput)
                self.processSpeech(speechOutput);
                await asyncio.sleep(1);
                await self.startListening()
                self.coz.set_backpack_lights_off();
    
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                self.coz.play_anim("anim_explorer_huh_01_head_angle_40").wait_for_completed()
                speechOutput = 'cosmo'
                self.processSpeech(speechOutput);
                await asyncio.sleep(1);
#                 await asyncio.sleep(0);
                await self.startListening()
    
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    
    
    def processSpeech(self,speechOutput):
        if self.startWorkout is False:
            if 'exercis' in speechOutput or 'excercis' in speechOutput or 'out' in speechOutput or 'work' in speechOutput or 'Out' in speechOutput or 'cozmo' in speechOutput or 'Cozmo' in speechOutput or 'Cosmo' in speechOutput or 'buddy' in speechOutput or 'body' in speechOutput or 'osmo' in speechOutput or 'Kosmos' in speechOutput or 'Kosmo' in speechOutput:
                if self.tries == 0:
                    self.coz.set_backpack_lights_off();
                    self.coz.play_anim("anim_keepaway_losegame_01").wait_for_completed()
                    self.coz.play_anim("anim_driving_upset_start_01").wait_for_completed()
                    self.coz.set_all_backpack_lights(Colors.GREEN)
                elif self.tries == 1:
                    self.coz.set_backpack_lights_off();
                    self.coz.pickup_object(self.cubes[0]).wait_for_completed()
                    self.coz.play_anim("anim_keepaway_pounce_01").wait_for_completed()
                    self.coz.set_all_backpack_lights(Colors.GREEN)
                elif self.tries == 2:
                    self.coz.set_backpack_lights_off();
                    self.coz.play_anim("anim_driving_upset_start_01").wait_for_completed()
                    self.coz.pickup_object(self.cubes[0]).wait_for_completed()
                    self.startWorkout = True
                    self.changeDirection()
                    self.coz.set_all_backpack_lights(Colors.GREEN)
                    self.liftThread = _thread.start_new_thread(self.startLiftThread, ())
                
                self.tries += 1
            else:
                self.coz.play_anim("anim_explorer_huh_01_head_angle_40").wait_for_completed()
        else:
            if 'fast' in speechOutput or 'ter' in speechOutput or 'tor' in speechOutput or 'tard' in speechOutput or 'tar' in speechOutput or 'irst' in speechOutput:
                self.speed += 1
                self.duration -= 0.1
                if self.duration <= 0.2:
                    self.duration = 0.2    
            elif 'slow' in spechOutput or 'lo' in speechOutput or 'fluid' in speechOutput:
                self.speed -= 1
                self.duration += 0.1
            
    
    
    
    def getTiredAndSleep(self):
        self.isTired = True
        self.startWorkout = False
        self.coz.play_anim("anim_workout_lowenergy_getout_01").wait_for_completed()
        self.coz.move_lift(-2)
        self.coz.play_anim("anim_gotosleep_fallasleep_01").wait_for_completed()
        self.coz.play_anim("anim_gotosleep_getout_04").wait_for_completed()
        self.coz.play_anim("anim_reacttoblock_happydetermined_02").wait_for_completed()
        self.resetValues()
    
    
    def resetValues(self):
        self.direction = 1
        self.speed = 2
        self.tiredDuration = 10
        self.duration = 1
        self.cozmoSleeping = False
        self.isTired = False
        self.startWorkout = False
        self.tries = 0
    
    
    def increaseSpeed(self):
        self.speed += 1
        self.duration -= 0.1
        
        if self.duration <= 0.2:
            self.duration = 0.2    
        
    
    def startLiftThread(self):
        print(self.startWorkout)
        if self.startWorkout is True:
            try:
                print("Start Lifting");
                Timer(self.tiredDuration, self.getTiredAndSleep).start()
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.startLifting())
            except Exception as e:
                print(e)       
         
    
    async def startLifting(self):
        if self.isTired == False:  
            self.coz.move_lift(self.speed * self.direction)
            await self.startLifting()
    
    
    def changeDirection(self):
        if self.startWorkout is True:
            self.direction *= -1
            
            Timer(self.duration, self.changeDirection).start()
            


if __name__ == '__main__':
    ExerciseBuddy()