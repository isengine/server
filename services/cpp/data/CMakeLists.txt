cmake_minimum_required(VERSION 3.5)
project(App)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")

add_executable(app main.cpp)
