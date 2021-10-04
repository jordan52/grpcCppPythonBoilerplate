
# grpcCppPythonBoilerplate

## purpose

What is my purpose? You don't want to know, but the purpose of this repo is to illustrate one way of using gRPC and protobuf to build a client and server in c++. It also has a python client that can hit that server just like the c++ client does. A few weeks ago I was like, "I really need to learn me some modern c++" and when I got started I tried to think of something to build. I couldn't think of anything good so I just started raw dogging some sockets. That got old real quick so I did some crap with [asio](https://think-async.com/Asio/) which was better but not awesome. While digging for answers I kept coming across people praising [protobuf](https://developers.google.com/protocol-buffers) and [gRPC]((https://grpc.io/) so I figued I should give them a shot.

While doing all this, I found myself fighting a lot with [cmake](https://cmake.org/) because I really have no idea what it is. In fact, only yesterday I learned that cmake just makes the makefiles and you still have to use make (I was using an IDE which did all the making out on my behalf. (Not going to lie, it is way better doing it manually yourself. Give it a shot, you can thank me later.)) The point here is that, hopefully, this project represents one way you can use cmake to generate your protobuf source files (or whatever they're called) and the gRPC service and also build some projects that use those. Of course, I learned how to do this yesterday so, you know, it probably ain't right.

To wrap this mess up, I think this is a decent boilerplate project that you could copy, add your own probobuf and gRPC specs, use them in a client/server demo, and build without too much trouble. Hopefully I will think of something useful to build using this and, you know, build it with some of that post modern c++ style.

## building and getting started

I have no idea if you will have any luck bulding and running this project. I can say that I'm doing this on a clapped out thinkpad running ubuntu with who knows what installed on it. I also know that I had to install a few extra things to get this project off the ground. I also know that over the past few weeks I have installed a ton of crap. So, I'm not 100% sure what you'll need.

> **if I am missing something, please update this readme and do a PR. someone somewhere would really appreciate it.**

This project uses cmake to build the protobuf definitions for c++ and python and also to build the c++ client and server. I think I got that working by doing the things here (https://cmake.org/install/)

Oh, and hey, listen:

> **Part of the cmake file in the protobuf directory (At this time) has a hard-coded path to the grpc_python_plugin executable on my machine. You, of course, are going to have to change that to get it to work on your machine. Unless your name is jordan and you installed grpc in ~/.local. If you did... sup twinsie!??!**


install gRPC locally, i have it at ~/.local/ because I followed these instructions exactly (https://grpc.io/docs/languages/cpp/quickstart/)

I already had python3 on my machine so I did this

`pip3 install --upgrade protobuf`

`pip3 install grpcio-tools`

`pip3 install googleapis-common-protos`


Hopefully you can just make the project by doing this:

to make the project
`cmake -DCMAKE_FIND_PACKAGE_PREFER_CONFIG=TRUE`

`make`

Did it build? Of course! let's run these things. You'll need a few terminals. Not to humblebrag, but I use a few tmux panes.

`cd cppserver`

`./server`

new terminal:
`cd cppclient`

`./client`

new terminal:
`cd pythonclient`

`python3 main.py`

The output for those programs is nothing exciting, but it is proof that you can get processes to talk to each other by sending protobuf message to each other via gRCP. yay.

# notes about the python client
The python client is a crappy example, I think. I'm not 100% happy about the protobuf import situation. Seems real janky.


# Thanks
Inspired by https://github.com/faaxm/exmpl-cmake-grpc