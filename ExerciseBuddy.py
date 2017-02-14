import asyncio
import cozmo
from Common.woc import WOC
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
    tiredDuration = 11
    duration = 1
    cozmoSleeping = False
    startWorkout = False
    tries = 0
    
    
    def __init__(self, *a, **kw):
        
        sys.setrecursionlimit(0x100000)
        
        cozmo.setup_basic_logging()
        cozmo.connect(self.startResponding)
        
        
        
    def startResponding(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self.coz = coz_conn.wait_for_robot()
        
        self.coz.play_anim('anim_gotosleep_getout_02').wait_for_completed()
        
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
    
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                await asyncio.sleep(0);
                await self.startListening()
    
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    
    
    def processSpeech(self,speechOutput):
        if self.startWorkout is False:
            if 'exercis' in speechOutput or 'excercis' in speechOutput or 'out' in speechOutput or 'work' in speechOutput or 'Out' in speechOutput or 'cozmo' in speechOutput or 'Cozmo' in speechOutput or 'Cosmo' in speechOutput or 'buddy' in speechOutput or 'body' in speechOutput or 'osmo' in speechOutput or 'Kosmos' in speechOutput or 'Kosmo' in speechOutput:
                if self.tries == 0:
                    self.coz.play_anim("anim_keepaway_losegame_01").wait_for_completed()
                    self.coz.play_anim("anim_driving_upset_start_01").wait_for_completed()
                elif self.tries == 1:
                    self.coz.play_anim("anim_keepaway_pounce_01").wait_for_completed()
                elif self.tries == 2:
                    self.coz.play_anim("anim_driving_upset_start_01").wait_for_completed()
                    self.startWorkout = True
                    self.changeDirection()
                    self.liftThread = _thread.start_new_thread(self.startLiftThread, ())
                
                self.tries += 1
        else:
            if 'fast' in speechOutput or 'ter' in speechOutput or 'tor' in speechOutput or 'tard' in speechOutput or 'tar' in speechOutput or 'irst' in speechOutput:
                Timer(self.tiredDuration, self.getTiredAndSleep).start()
                self.speed += 1
                self.duration -= 0.1
                if self.duration <= 0.2:
                    self.duration = 0.2    
            elif 'slow' in spechOutput or 'lo' in speechOutput or 'fluid' in speechOutput:
                self.speed -= 1
                self.duration += 0.1
            
    
    
    
    def getTiredAndSleep(self):
        self.startWorkout = False
        self.coz.play_anim("anim_workout_lowenergy_getout_01").wait_for_completed()
        self.coz.move_lift(5)
        self.coz.play_anim("anim_gotosleep_fallasleep_01").wait_for_completed()
        self.coz.play_anim("anim_gotosleep_getout_04").wait_for_completed()
        self.resetValues()
    
    
    def resetValues(self):
        self.direction = 1
        self.speed = 2
        self.tiredDuration = 10
        self.duration = 1
        self.cozmoSleeping = False
        self.startWorkout = False
        self.tries = 0
    
    
    
    def startLiftThread(self):
        print(self.startWorkout)
        if self.startWorkout is True:
            try:
                print("Start Lifting");
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.startLifting())
            except Exception as e:
                print(e)       
         
    
    async def startLifting(self):
        self.coz.move_lift(self.speed * self.direction)
        await self.startLifting()
    
    
    def changeDirection(self):
        if self.startWorkout is True:
            self.direction *= -1
            
            Timer(self.duration, self.changeDirection).start()
            


if __name__ == '__main__':
    ExerciseBuddy()