import grpc
import sys
import os
from concurrent import futures
# I don't like this, but it is the simplest way to grab the proto files.
#sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'protobuf'))
from os.path import dirname, abspath
sys.path.append(os.path.join(dirname(dirname(abspath(__file__))),'protobuf'))
from proto import status_pb2
from proto import statusservice_pb2_grpc




class StatusSerivceServicer(statusservice_pb2_grpc.StatusServiceServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        print("initializing status service")

    def GetStatus(self, request, context):
        print("Got a status!")

def run():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    statusservice_pb2_grpc.add_StatusServiceServicer_to_server(
        StatusSerivceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run()