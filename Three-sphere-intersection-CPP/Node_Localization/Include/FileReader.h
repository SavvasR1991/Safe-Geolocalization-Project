#ifndef FILEREADER_H 
#define FILEREADER_H

#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string>
#include "Tetrahedron_Calculator.h"
#include "CurrentDirectory.h"

using namespace std;


bool contains_number(const string &c)
{
    return (c.find_first_of("0123456789") != string::npos);
} 

void split(const string &txt, char ch,double *tempCoordinates)
{
    size_t pos = txt.find( ch );
    size_t initialPos = 0;
    int counter = 0;
    double i_dec = 0;
    
    while( pos != std::string::npos ) {
        tempCoordinates[counter] = atof(txt.substr( initialPos, pos - initialPos ).c_str());
        counter++;
        if(counter >2)
            break;
        initialPos = pos + 1;

        pos = txt.find( ch, initialPos );
    }
}

void fileReaderWriter(const char* input){

    ifstream file(input);
    ofstream myfile;
    myfile.open (GetCurrentWorkingDirOutput().c_str());
    
    double *tempCoordinates = new double[3];
    double l1,l2,l3;
    
    int counter = 0;
    int triangularCounter = 1;

    Coordinates XtopPyramid;
    Coordinates actualCoordinates;
	Coordinates pyramidBase[3];
	
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
           if(contains_number(line)){
               split((line).append(" "),' ',tempCoordinates);
               switch (counter){
                    case 0:
                        pyramidBase[0].setCoordinates(tempCoordinates[0], tempCoordinates[1],tempCoordinates[2]);
                        break;
                    case 1:
                        pyramidBase[1].setCoordinates(tempCoordinates[0], tempCoordinates[1],tempCoordinates[2]);
                        break;
                    case 2:
                        pyramidBase[2].setCoordinates(tempCoordinates[0], tempCoordinates[1],tempCoordinates[2]);
                        break;
                    case 3:
                        actualCoordinates.setCoordinates(tempCoordinates[0], tempCoordinates[1],tempCoordinates[2]);
                        XtopPyramid = triangularPyramidTopCalculation(pyramidBase,actualCoordinates);
                        
                        myfile << "The Base of the Triangular Pyramid of Shape "<<triangularCounter<<" is :\n";
                        myfile<< "A = [ "<<pyramidBase[0].getXCoordinates()<<" , "<<pyramidBase[0].getYCoordinates()<<" , "<<pyramidBase[0].getZCoordinates()<<"]\n";
                        myfile<< "B = [ "<<pyramidBase[1].getXCoordinates()<<" , "<<pyramidBase[1].getYCoordinates()<<" , "<<pyramidBase[1].getZCoordinates()<<"]\n";
                        myfile<< "C = [ "<<pyramidBase[2].getXCoordinates()<<" , "<<pyramidBase[2].getYCoordinates()<<" , "<<pyramidBase[2].getZCoordinates()<<"]\n";
                        myfile<< "The unknown Node has    D  = [ "<<actualCoordinates.getXCoordinates()<<" , "<<actualCoordinates.getYCoordinates()<<" , "<<actualCoordinates.getZCoordinates()<<"]\n";
                        myfile<< "The length of A,D is  |AD| = [ "<<vectorTwoPointLength(actualCoordinates,pyramidBase[0])<<"]\n";
                        myfile<< "The length of B,D is  |BD| = [ "<<vectorTwoPointLength(actualCoordinates,pyramidBase[1])<<"]\n";
                        myfile<< "The length of C,D is  |CD| = [ "<<vectorTwoPointLength(actualCoordinates,pyramidBase[2])<<"]\n";
                        myfile<<"The algorithm calcuted: D' = [ "<<XtopPyramid.getXCoordinates()<<" , "<<XtopPyramid.getYCoordinates()<<" , "<<XtopPyramid.getZCoordinates()<<"]\n";
                        myfile<<"\n\n";
                        triangularCounter++;
                        break;
                    default:
                        break;
               }
               counter++;
               if(counter==4){
                    counter=0;
               }
            }
        }
        file.close();
        myfile.close();
    }
    delete []tempCoordinates;
}

#endif 
