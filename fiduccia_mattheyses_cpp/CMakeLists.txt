cmake_minimum_required(VERSION 3.24)
project(FM)

set(CMAKE_CXX_STANDARD 17)

add_executable(FM main.cpp DataStructures.cpp DataStructures.h Vertex.cpp Vertex.h Graph.cpp Graph.h)
