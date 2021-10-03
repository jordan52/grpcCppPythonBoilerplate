find_package(protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)
find_package(Threads)

set(PROTO_FILES
    proto/status.proto
    proto/statusservice.proto
    )

add_library(proto ${PROTO_FILES})
target_link_libraries(proto
    PUBLIC
    protobuf::libprotobuf
    gRPC::grpc
    gRPC::grpc++
    )
target_include_directories(proto PUBLIC ${CMAKE_CURRENT_BINARY_DIR})

get_target_property(grpc_cpp_plugin_location gRPC::grpc_cpp_plugin LOCATION)
protobuf_generate(TARGET proto LANGUAGE cpp)
protobuf_generate(TARGET proto LANGUAGE grpc GENERATE_EXTENSIONS .grpc.pb.h .grpc.pb.cc PLUGIN "protoc-gen-grpc=${grpc_cpp_plugin_location}")
protobuf_generate(TARGET proto LANGUAGE python)
# if you have errors here, look at https://stackoverflow.com/questions/34713861/python-grpc-protobuf-stubs-generation-issue-grpc-out-protoc-gen-grpc-plugin
# obviously, you're going to have to change the following line to get this to work on your system
protobuf_generate(TARGET proto LANGUAGE grpc GENERATE_EXTENSIONS .py PLUGIN "protoc-gen-grpc=/home/jordan/.local/bin/grpc_python_plugin")

# I can't figure out how to use protobuf_generate for grpc python files

# For that python command, i think you can reidrect the python files somehwere else using something like this example but I'm not sure I want to
# set(PROTO_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/definitions)
#set(PROTOC_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR})
#
#protobuf_generate(LANGUAGE python
#    PROTOS ${PROTO_SOURCE_DIR}/TemperatureTagGroup.proto
#       ${THINGAPI_INCLUDE_DIR}/adlinktech/datariver/descriptor.proto
#    OUT_VAR PB_FILES
#    PROTOC_OUT_DIR ${PROTOC_OUTPUT_DIR}
#)


# if that above doesn't generate the python you may have to
# sudo apt install python3-pip
# pip3 install --upgrade protobuf
# pip3 install grpcio-tools
# python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/statusservice.proto
