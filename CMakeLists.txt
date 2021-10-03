cmake_minimum_required(VERSION 3.16)
project(grpcCppPythonBoilerplate)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
set(CMAKE_CXX_STANDARD 14)

add_subdirectory(protobuf)
add_subdirectory(cppserver)
add_subdirectory(cppclient)

#add_executable(grpcCppPythonBoilerplate main.cpp)


# To run this you will run
# cmake -DCMAKE_FIND_PACKAGE_PREFER_CONFIG=TRUE
# make