#include <proto/status.pb.h>
#include <proto/statusservice.grpc.pb.h>

#include <grpc/grpc.h>
#include <grpcpp/create_channel.h>

#include <iostream>


int main(int argc, char* argv[]) {


    protoboilerplate::StatusRequest statusRequest;
    protoboilerplate::StatusResponse statusResponse;

    statusRequest.set_node_name("cppclient");

    auto channel = grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials());
    std::unique_ptr<protoboilerplate::StatusService::Stub> stub = protoboilerplate::StatusService::NewStub(channel);
    grpc::ClientContext context;  // need a new context per call... sort of.
    grpc::Status status = stub->GetStatus(&context, statusRequest, &statusResponse);

    std::cout << "GRCP Status Service Show Me What You Got:" << std::endl;
    std::cout << "Name: " << statusResponse.name() << std::endl;


}