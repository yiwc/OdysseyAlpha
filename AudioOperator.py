#!/usr/bin/sudo python

import speech_recognition as sr
import os
import random
import threading
import time
#Microphone audio recognition

class Audio_Operator():
    def __init__(self,db=None):
        self.r = sr.Recognizer()
        # self.mic = sr.Microphone(device_index=self.get_default_device_index())
        self.mic = sr.Microphone()
        print(sr.Microphone.list_microphone_names())
        with self.mic as source:
            print("waiting for init Mic")
            self.r.adjust_for_ambient_noise(source)
        self.res=""
        self.res_target = ""
        self.res_target_cube=["box","cube","Box","fox"]
        self.res_target_bottle=["water","Water","bottle","bottom","but","what"]

        self.ListenMode=0 #1,from file.#0,from mic

        self.run_main_able=0 #1,run;2, stop running(actually running, yet doing nothing)
        self.isListening=0 #is listen blocking
        self.isRecognizing=0 #is analysing blocking


    def SetRuningAble(self,able):
        self.run_main_able=able

    def start_run_main_thread(self):
        AudioThread = threading.Thread(target=self.run_main)
        AudioThread.start()

    def run_main(self,mode=1):#mode=1,soundfile ; mode=0,microphone.
        loop=0
        while(1):
            if(self.run_main_able):
                loop+=1
                print("\n\nRec Loop:",loop)
                mode=self.ListenMode
                if(mode==1):#use file sound
                    file=self.get_random_sound_file()
                    with file as source:
                        audio = self.r.record(source)
                elif(mode==0):# use microphone
                    print("speak to the mic")
                    try:
                        self.isListening=1
                        with self.mic as source:
                            audio = self.r.listen(source, phrase_time_limit=3)
                        self.isListening=0
                    except:
                        print("Listen Error: Speak Nothing")
                try:
                    self.isRecognizing=1
                    res=self.r.recognize_google(audio)
                    self.isRecognizing=0
                except:
                    self.isRecognizing = 0
                    res="None"
                self.res=res
                print("Recognition Res:", res)

                for word in self.res_target_bottle:
                    if(word) in self.res:
                        self.res_target="bottle"
                for word in self.res_target_cube:
                    if(word) in self.res:
                        self.res_target="cube"
            else:
                self.res=''
                time.sleep(1)
    def run_with_a_soundfile(self): #simpler version of run_with_soundfile
        hello=self.get_test_sound_file()
        with hello as source:
            audio=self.r.record(source)
            res=self.r.recognize_google(audio)
            print(res)
    def run_with_mic_simple(self):
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
            print(1)
            # audio = self.r.listen(source)
            audio = self.r.listen(source,timeout=1)
            # self.r.listen()
            print(2)
            res=self.r.recognize_google(audio)
            print(3,"res:",res)
            return res

    #functional
    def get_test_sound_file(self):
        return sr.AudioFile('hello.wav')
    def get_default_device_index(self):
        devices_list=sr.Microphone.list_microphone_names()
        print("device list",devices_list)
        index=0
        for i in range(len(devices_list)):
            index=i
            if(devices_list[index]=="default"):
                break
        print("index",index)
        return index
    def get_random_sound_file(self):
        files=os.listdir()
        audios=[]
        for file in files:
            if(".wav" in file):
                audios.append(file)
        # print(audios)
        filename=random.choice(audios)
        print("File Selected:",filename)
        return sr.AudioFile(filename)

if __name__=="__main__":
    AudioOP=Audio_Operator()
    # AudioOP.run(g)
    # print(AudioOP.get_random_sound_file())
    # AudioOP.run_with_mic()
    # AudioOP.run_main(mode=0)
    AudioOP.start_run_main_thread()