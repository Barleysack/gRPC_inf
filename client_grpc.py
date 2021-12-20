import grpc
import comm07_pb2
import comm07_pb2_grpc
from pydub import AudioSegment

with open("./yes_6.wav",'rb') as fd:
    audio = fd.read()
def run(audio):
    
    with grpc.insecure_channel('118.67.135.206:6013') as channel:
        stub = comm07_pb2_grpc.Comm07Stub(channel)
        response=stub.Talker(comm07_pb2.InfRequest(audio))
    print(response)
    print("fine!")
    
if __name__=='__main__':
    run(audio)