#include <proto/status.pb.h>
#include <proto/statusservice.grpc.pb.h>

#include <grpc/grpc.h>
#include <grpcpp/server_builder.h>

#include <iostream>

class StatusService final : public protoboilerplate::StatusService::Service {
public:
    virtual ::grpc::Status GetStatus(::grpc::ServerContext* context, const ::protoboilerplate::StatusRequest* request, ::protoboilerplate::StatusResponse* response)
    {
        std::cout << "Server: GetStatus for \"" << request->name() << "\"." << std::endl;
        response->set_name("OK");
        return grpc::Status::OK;
    }
};

int main(int argc, char* argv[])
{
    grpc::ServerBuilder builder;
    builder.AddListeningPort("0.0.0.0:50051", grpc::InsecureServerCredentials());

    StatusService my_statusservice;
    builder.RegisterService(&my_statusservice);

    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    server->Wait();

    return 0;
}
