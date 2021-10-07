#include <proto/status.pb.h>
#include <proto/statusservice.grpc.pb.h>

#include <grpc/grpc.h>
#include <grpcpp/server_builder.h>

#include <iostream>

#include "spdlog/spdlog.h"
#include "spdlog/fmt/ostr.h"
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/sinks/basic_file_sink.h"

#include <boost/program_options.hpp>

namespace po = boost::program_options;

class StatusService final : public protoboilerplate::StatusService::Service {
private:
    std::shared_ptr<spdlog::logger> _logger;
public:
    StatusService(){
        _logger = spdlog::get("server_logger");
    }
    virtual ::grpc::Status GetStatus(::grpc::ServerContext* context, const ::protoboilerplate::StatusRequest* request, ::protoboilerplate::StatusResponse* response)
    {
        _logger->info("Server: GetStatus for \"{}\".", request->name());
        response->set_name("OK");
        return grpc::Status::OK;
    }
};

void initlogging(){

    try
    {
        auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
        console_sink->set_level(spdlog::level::warn);
        console_sink->set_pattern("[multi_sink_example] [%^%l%$] %v");

        auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>("logs/multisink.txt", true);
        file_sink->set_level(spdlog::level::trace);


        spdlog::sinks_init_list sink_list = { file_sink, console_sink };

        spdlog::logger logger("server_logger", sink_list.begin(), sink_list.end());

        logger.set_level(spdlog::level::debug);
        logger.warn("this should appear in both console and file");
        logger.info("this message should not appear in the console, only in the file");
        logger.flush();  //todo:

        // or you can even set multi_sink logger as default logger
        spdlog::set_default_logger(std::make_shared<spdlog::logger>("server_logger", spdlog::sinks_init_list({console_sink, file_sink})));

    }
    catch (const spdlog::spdlog_ex& ex)
    {
        std::cout << "Log initialization failed: " << ex.what() << std::endl;
    }
}

int main(int argc, char* argv[])
{
    std::string address_port = "0.0.0.0:50051";

    // parse command line and config
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
        address_port = vm["port"].as<std::string>();
    }

    // set up the logger

    initlogging();

    auto logger = spdlog::get("server_logger");

    logger->warn("Server Starting");

    grpc::ServerBuilder builder;
    builder.AddListeningPort(address_port, grpc::InsecureServerCredentials());

    StatusService my_statusservice;
    builder.RegisterService(&my_statusservice);

    logger->warn("Server getting ready to listen on {}!", address_port);
    logger->warn("yikes");
    logger->error("double yikes!");

    std::unique_ptr<grpc::Server> server(builder.BuildAndStart());
    server->Wait();

    return 0;
}
