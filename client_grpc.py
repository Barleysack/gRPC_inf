from typing import SupportsRound
import grpc
import comm07_pb2
import comm07_pb2_grpc
from pydub import AudioSegment
import asyncio
import pyaudio
from pydub.utils import db_to_float
from time import time
import numpy as np

S_ADDRESS = '118.67.135.206:6013'
RATE = 16000
S_THRESHOLD = db_to_float(-35)
MIN_SILENCE = 6
endure = 0
frames = None
ticker = False

def client_loop(S_ADDRESS):
    global frames
    global ticker
    global endure
    
    audio_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,channels=1, #audio stream on
                                          rate=16000,input=True,frames_per_buffer=2048)
    diagnosis = []
    
    with grpc.insecure_channel(S_ADDRESS) as channel:                  #Define channel
        stub = comm07_pb2_grpc.Comm07Stub(channel)                     #Instantiate stub
        while True:
            
            while True:
                
                audio = audio_stream.read(512,exception_on_overflow=False)
                
                audio_checker = AudioSegment(audio,sample_width=2, frame_rate=16000, channels=1)
                
                try : 
                    frames += audio
                except : 
                    frames = audio
                    
                if audio_checker.rms<S_THRESHOLD*audio_checker.max_possible_amplitude:
                    
                    if not ticker:
                        frames=frames[-64:]
                        endure=0
                    elif endure<MIN_SILENCE:
                        endure+=1
                    elif len(frames)<=300:
                        pass
                    else:
                        
                        break
                else:
                    endure=0
                    ticker=True
                    
            ticker = False
            endure = 0
            start= time()
            response = stub.Talker(comm07_pb2.InfRequest(audio=frames)) #Get response
            end=time() 
            diagnosis.append((end-start))
            frames = frames[-64:]
            print(response.answer)
            if response.answer == '안녕':
                break
            
    print(round(np.average(diagnosis),3))
            
    
    

    



    
if __name__=='__main__':
    client_loop(S_ADDRESS)