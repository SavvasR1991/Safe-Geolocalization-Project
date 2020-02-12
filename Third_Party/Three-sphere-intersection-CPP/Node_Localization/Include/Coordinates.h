#ifndef COORDINATES_H 
#define COORDINATES_H

using namespace std;

class Coordinates{

	private:
		double x;
		double y;
		double z;
		double *CoordinatesArray;

	public:
		Coordinates(){
			CoordinatesArray = new double[3];
			x = 0;
			y = 0;
			z = 0;
		};

		Coordinates(double a,double b,double c){
			CoordinatesArray = new double[3];
			x = a;
			y = b;
			z = c;	
		};
		
		~Coordinates(){
			//delete[] CoordinatesArray;
		};

		void setCoordinates(double a,double b,double c){
			x = a;
			y = b;
			z = c;	
		};

		double* getCoordinates(){

			CoordinatesArray[0] = x;
			CoordinatesArray[1] = y;
			CoordinatesArray[2] = z;

			return CoordinatesArray;
		};

		double getXCoordinates(){
			return x;
		};

		double getYCoordinates(){
			return y;
		};

		double getZCoordinates(){
			return z;
		};

		void printCoordinates(){
			cout<<" x = "<<x<<endl;
			cout<<" y = "<<y<<endl;
			cout<<" z = "<<z<<endl;
		};
};

#endif 
