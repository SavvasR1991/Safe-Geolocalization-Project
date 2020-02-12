#ifndef TETRAHEDRON_CALCULATOR_H 
#define TETRAHEDRON_CALCULATOR_H

#include <cmath>        
#include "Coordinates.h"
#include "Tetrahedron_Calculator_Algorithm.h"

using namespace std;


Coordinates triangularPyramidTopCalculation(Coordinates threePoints[],Coordinates actualCoordinates){

	Coordinates topPyramid;

	topPyramid = triangularPyramidTopCalculationAlgorithm1(threePoints,actualCoordinates);
	
	return topPyramid;

};


#endif 
