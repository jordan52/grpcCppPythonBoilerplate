#include <proto/status.pb.h>
#include <proto/statusservice.grpc.pb.h>

#include <grpc/grpc.h>
#include <grpcpp/server_builder.h>

#include <iostream>

#include "spdlog/spdlog.h"
#include <boost/program_options.hpp>

namespace po = boost::program_options;

using namespace std;
class StatusService final : public protoboilerplate::StatusService::Service {
public:
    virtual ::grpc::Status GetStatus(::grpc::ServerContext* context, const ::protoboilerplate::StatusRequest* request, ::protoboilerplate::StatusResponse* response)
    {
        spdlog::info("Server: GetStatus for \"{}\".", request->name());
        response->set_name("OK");
        return grpc::Status::OK;
    }
};

int main(int argc, char* argv[])
{

    string address_port = "0.0.0.0:50051";

    spdlog::info("Server Starting");

    po::options_description desc("Allowed options");
    desc.add_options()
            ("help", "produce help message")
            ("port", po::value(&address_port), "set listening address:port")
            ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);
    if (vm.count("help")) {
        std::cout << desc << "\n";
        return 0;
    }
    if (vm.count("port")) {
        address_port = vm["port"].as<string>();
    }

    grpc::ServerBuilder builder;
    builder.AddListeningPort(address_port, grpc::InsecureServerCredentials());

    StatusService my_statusservice;
    builder.RegisterService(&my_statusservice);

    spdlog::info("Server getting ready to listen on {}!", address_port);

    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    server->Wait();

    return 0;
}
