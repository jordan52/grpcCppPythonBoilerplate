import grpc
import sys
import os

# I don't like this, but it is the simplest way to grab the proto files.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'protobuf'))

from proto import status_pb2
from proto import statusservice_pb2_grpc


def getstatus(stub):
    statreq = status_pb2.StatusRequest(name = "python client")
    statres = stub.GetStatus(statreq)
    print(statres)
    print(f"manual member get for name is {statres.name}")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:

        stub = statusservice_pb2_grpc.StatusServiceStub(channel)
        print("running")
        getstatus(stub)

if __name__ == '__main__':
    run()