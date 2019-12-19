#!/usr/bin/sudo python

import speech_recognition as sr
import os
import random
#Microphone audio recognition

class Audio_Operator():
    def __init__(self):
        self.r = sr.Recognizer()
        # self.mic = sr.Microphone(device_index=self.get_default_device_index())
        self.mic = sr.Microphone()
        print(sr.Microphone.list_microphone_names())
        with self.mic as source:
            print("waiting for init Mic")
            self.r.adjust_for_ambient_noise(source)


    def run_main(self,mode=1):#mode=1,soundfile ; mode=0,microphone.
        loop=0
        while(1):
            loop+=1
            print("\n\nRec Loop:",loop)

            if(mode==1):#use file sound
                file=self.get_random_sound_file()
                with file as source:
                    audio = self.r.record(source)
            elif(mode==0):# use microphone
                print("speak to the mic")
                with self.mic as source:
                    audio = self.r.listen(source, timeout=1)
            try:
                res=self.r.recognize_google(audio)
            except:
                res="None"
            print("Recognition Res:", res)
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
    AudioOP.run_main(mode=1)