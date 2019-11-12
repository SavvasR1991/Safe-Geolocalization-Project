#ifndef CURRENTDIRECTORY_H 
#define CURRENTDIRECTORY_H

using namespace std;

#include <stdio.h>  /* defines FILENAME_MAX */
// #define WINDOWS  /* uncomment this line to use it for windows.*/ 
#ifdef WINDOWS
#include <direct.h>
#define GetCurrentDir _getcwd
#else
#include <unistd.h>
#define GetCurrentDir getcwd
#endif
#include<iostream>
#include<string>
 
string GetCurrentWorkingDirInput( void ) {
  char buff[FILENAME_MAX];
  GetCurrentDir( buff, FILENAME_MAX );
  string current_working_dir(buff);
  size_t index = 0;
  while (true) {
     index = current_working_dir.find("build", index);
     if (index == std::string::npos) break;

     current_working_dir.replace(index, 15, "Tests/test1.txt");

     index += 15;
  }
  return current_working_dir;
}

string GetCurrentWorkingDirOutput( void ) {
  char buff[FILENAME_MAX];
  GetCurrentDir( buff, FILENAME_MAX );
  string current_working_dir(buff);
  size_t index = 0;
  while (true) {
     index = current_working_dir.find("build", index);
     if (index == std::string::npos) break;

     current_working_dir.replace(index, 19, "Results/results.txt");

     index += 19;
  }
  return current_working_dir;
}

#endif 
