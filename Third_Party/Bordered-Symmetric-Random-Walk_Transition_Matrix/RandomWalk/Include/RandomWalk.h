#include "List.h"
#include "List2.h"

int helperInt = 0;

int nodeTransformation(int x, int y, int z, int w, int d) {
	return(x + w * (y - 1) + w * d * (z - 1));
}

struct ArrayAndSize {
	int** array;
	int size;
};

ArrayAndSize* calculateNeighbourNodes(int x, int y, int z, int w, int d, int h) {
	int i, arraySize;
	ArrayAndSize* neighbourNodes = new ArrayAndSize;
	List listA;
	if (x > 1) listA.insert(x - 1, y, z);
	if (x < w) listA.insert(x + 1, y, z);
	if (y > 1) listA.insert(x, y - 1, z);
	if (y < d) listA.insert(x, y + 1, z);
	if (z > 1) listA.insert(x, y, z - 1);
	if (z < h) listA.insert(x, y, z + 1);

	arraySize = listA.totalNodes;
	helperInt = arraySize;
	neighbourNodes->array = new int* [arraySize];
	neighbourNodes->size = arraySize;
	for (i = 0; i < arraySize; ++i) {
		neighbourNodes->array[i] = new int[3];
	}

	listA.convertListToArray(neighbourNodes->array);
	listA.deleteList();


	return neighbourNodes;
}


void randomWalk(int width, int depth, int height) {

	int w, d, h, numberOfStates, i, j, x, y, z;
	int** P, ** nodePoints;
	int* nodeDegrees;
	int nodeNumber = 0;

	ArrayAndSize* tempPointer;
	List2* neighbourNodes,* tempNeighbourNodes;
	List* transformedNeighbourNodes;

	w = width;
	d = depth;
	h = height;
	numberOfStates = w * d * h;

	P = new int* [numberOfStates];
	for (i = 0; i < numberOfStates; ++i) {
		P[i] = new int[numberOfStates];
		for (j = 0; j < numberOfStates; j++) {
			P[i][j] = 0;
		}
	}

	nodePoints = new int* [numberOfStates];
	for (i = 0; i < numberOfStates; ++i) {
		nodePoints[i] = new int[3];
		for (j = 0; j < 3; j++) {
			nodePoints[i][j] = 0;
		}
	}

	nodeDegrees = new int[numberOfStates];




	for (z = 1; z <= h; ++z) {
		for (y = 1; y <= d; ++y) {
			for (x = 1; x <= w; ++x) {
				nodePoints[nodeNumber][0] = x;
				nodePoints[nodeNumber][1] = y;
				nodePoints[nodeNumber][2] = z;
				nodeNumber++;
			}
		}
	}
	neighbourNodes = new List2();
	int rows;

	nodeNumber = 0;
	i = 0;
	for (z = 1; z <= h; ++z) {
		for (y = 1; y <= d; ++y) {
			for (x = 1; x <= w; ++x) {
				nodeNumber++;
				tempPointer = calculateNeighbourNodes(x, y, z, w, d, h);
				neighbourNodes->insert(tempPointer->array, tempPointer->size);
				nodeDegrees[i] = tempPointer->size;
				i++;
			}
		}
	}

	transformedNeighbourNodes = new List();
	nodeNumber = 0;

	for (z = 1; z <= h; ++z) {
		for (y = 1; y <= d; ++y) {
			for (x = 1; x <= w; ++x) {
				nodeNumber++;
				
				//TO DO

			}
		}
	}






	for (i = 0; i < numberOfStates; ++i) {
		delete[] P[i];
	}
	delete[] P;

	for (i = 0; i < numberOfStates; ++i) {
		delete[] nodePoints[i];
	}
	delete[] nodePoints;
	delete[] nodeDegrees;
	delete neighbourNodes;


	//neighbourNodes->deleteList();
	transformedNeighbourNodes->deleteList();

}