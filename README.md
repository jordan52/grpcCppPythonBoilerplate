
# grpcCppPythonBoilerplate

## purpose

What is my purpose? You don't want to know, but the purpose of this repo is to illustrate one way of using grpc and protobuf to build a client and server in c++ and also a python client that can hit that server just like the c++ client does. A few weeks ago I was like, "I really need to learn me some modern c++" and when I got started I tried to think of something to build. I couldn't think of anything good so I just started raw dogging some sockets. That got old real quick so I did some crap with asio which was better but not awesome. While digging for answers I kept coming across people praising protobuf and grpc so I figued I should give them a shot.

While doing all this, I found myself fighting a lot with cmake because I really have no idea what it is. In fact, only yesterday I learned that cmake just makes the makefiles and you still have to use make (I was using an IDE which did all the making out on my behalf. (Not going to lie, it is way better doing it yourself.)) The point here is that, hopefully, this project represents one way you can use cmake to generate your protobuf source files (or whatever they're called) and the grpc service and also build some projects that use those. Of course, I learned how to do this yesterday so, you know, it probably ain't right.


## building and getting started

I have no idea if you will have any luck bulding and running this project. I can say that I'm doing this on a clapped out thinkpad running ubuntu with who knows what installed on it. I also know that I had to install a few extra things to get this project off the ground. I also know that over the past few weeks I have installed a ton of crap. So, I'm not 100% sure what you'll need.

This project uses cmake to build the protobuf definitions for c++ and python and also to build the c++ client and server.

**Part of the cmake file in the protobuf directory (At this time) has a hard-coded path to the grpc_python_plugin executable on my machine. You, of course, are going to have to change that to get it to work on your machine. Unless your name is jordan and you installed grpc in ~/.local. If you did... hey twinsie! <vomit>**


## install grpc locally, i have it at ~/.local/

https://grpc.io/docs/languages/cpp/quickstart/

sudo apt install python3-pip
pip3 install --upgrade protobuf
pip3 install grpcio-tools
pip3 install googleapis-common-protos


to make the project
cmake -DCMAKE_FIND_PACKAGE_PREFER_CONFIG=TRUE
make

cd cppserver
./server

new terminal:
cd cppclient
./client

new terminal:
cd pythinclient
python3 main.py


# python client
The python client is a crappy example, I think. I'm not 100% happy about the protobuf import situation. Seems real janky.


# Thanks
Inspired by https://github.com/faaxm/exmpl-cmake-grpc