cmake_minimum_required(VERSION 2.8.9)
project(Localization_Algorithms)

include_directories(include)
 
file(GLOB SOURCES "src/*.cpp")
 
add_executable(Localization_Algorithms ${SOURCES})  
