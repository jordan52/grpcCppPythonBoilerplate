import grpc
import sys
import os
import time
import secrets


nodeNames = ['battery', 'correct', 'horse', 'staple', "cheeseballs"]

# I don't like this, but it is the simplest way to grab the proto files.
#sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'protobuf'))
from os.path import dirname, abspath
sys.path.append(os.path.join(dirname(dirname(abspath(__file__))),'protobuf'))
from proto import status_pb2
from proto import statusservice_pb2_grpc


def getstatus(stub):
    try:
        statreq = status_pb2.StatusRequest(node_name = secrets.choice(nodeNames))
        statres = stub.GetStatus(statreq)
        print(statres)
        print(f"manual member get for name is {statres.node_name}")
    except grpc.RpcError as e:
        print(e.code())
    else:
        print(grpc.StatusCode.OK)
    

def run():
    with grpc.insecure_channel('localhost:50051') as channel:

        stub = statusservice_pb2_grpc.StatusServiceStub(channel)
        print("running")
        while True:
            time.sleep(0.01)
            getstatus(stub)

if __name__ == '__main__':
    run()