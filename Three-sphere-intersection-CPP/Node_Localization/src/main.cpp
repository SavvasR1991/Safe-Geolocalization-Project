#include <iostream>
#include "FileReaderWriter.h"
#include "CurrentDirectory.h"

using namespace std;
 
int main()
{

    fileReaderWriter(GetCurrentWorkingDirInput().c_str());

	return 0;
}
