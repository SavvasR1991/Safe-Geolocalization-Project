cmake_minimum_required(VERSION 2.8.9)
project(Node_Localization)

include_directories(Include)
 
file(GLOB SOURCES "src/*.cpp")
 
add_executable(Node_Localization ${SOURCES})  
