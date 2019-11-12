#ifndef TETRAHEDRON_CALCULATOR_ALGORITHM_H 
#define TETRAHEDRON_CALCULATOR_ALGORITHM_H

#include <cmath>        
#include "Coordinates.h"

using namespace std;

double vectorTwoPointLength(Coordinates A,Coordinates B){

	double lengthVectorAB = 0;

	double X_a_b = 0;

	double Y_a_b = 0;

	double Z_a_b = 0;

	X_a_b = abs(A.getXCoordinates() - B.getXCoordinates());

	Y_a_b = abs(A.getYCoordinates() - B.getYCoordinates());

	Z_a_b = abs(A.getZCoordinates() - B.getZCoordinates());

	lengthVectorAB = sqrt(pow(X_a_b,2) + pow(Y_a_b,2) + pow(Z_a_b,2));

	return lengthVectorAB;

}


Coordinates triangularPyramidTopCalculationAlgorithm1(Coordinates threePoints[],Coordinates actualCoordinates){

	Coordinates topPyramid;

    double x1 = threePoints[0].getXCoordinates();
	double x2 = threePoints[1].getXCoordinates();
	double x3 = threePoints[2].getXCoordinates();

	double y1 = threePoints[0].getYCoordinates();
	double y2 = threePoints[1].getYCoordinates();
	double y3 = threePoints[2].getYCoordinates();

	double z1 = threePoints[0].getZCoordinates();
	double z2 = threePoints[1].getZCoordinates();
	double z3 = threePoints[2].getZCoordinates();
	
	double x4 = actualCoordinates.getXCoordinates();
	double y4 = actualCoordinates.getYCoordinates();
	double z4 = actualCoordinates.getZCoordinates();
	
	double r1=vectorTwoPointLength(threePoints[0],actualCoordinates);
	double r2=vectorTwoPointLength(threePoints[1],actualCoordinates);
	double r3=vectorTwoPointLength(threePoints[2],actualCoordinates);
	
	double a1, b1, c1, k1, a3, b3, c3, k3, a31, b31, e, f, g, h, A, B, C, x, y, z, rootD;
	
	double x_,y_,z_;
	
	double epsilon = 0.00001;

    cout<<"------------>Calculating Coordinates for Unknowed Node<------------\n";
    
    cout<<"(a)Point    : A("<<x1<<","<<y1<<","<<z1<<") "<<endl;
    cout<<"(b)Point    : B("<<x2<<","<<y2<<","<<z2<<") "<<endl;
    cout<<"(c)Point    : C("<<x3<<","<<y3<<","<<z3<<") "<<endl;
    cout<<"(d)Point    : D("<<x4<<","<<y4<<","<<z4<<") (Unknown Node)"<<endl;
    cout<<"(e)Distance : |DA|="<<r1<<endl;
    cout<<"(f)Distance : |DB|="<<r2<<endl;
    cout<<"(g)Distance : |DC|="<<r3<<endl;
	
	cout<<"\n********************** Algorithm coordinates calculation *********************"<<endl;
	cout<<"1.Calculating k1"<<endl;
	k1 = r1 * r1 - r2 * r2 - x1 * x1 + x2 * x2 - y1 * y1 + y2 * y2 - z1 * z1 + z2 * z2;
	cout<<"> k1 = r1 * r1 - r2 * r2 - x1 * x1 + x2 * x2 - y1 * y1 + y2 * y2 - z1 * z1 + z2 * z2 = "<<r1<<" * "<<r1<<" - "<<r2<<" * "<<r2<<" - "<<x1<<" * "<<x1<<" + "<<x2<<" * "<<x2<<" - "<<y1<<" * "<<y1<<" + "<<y2<<" * "<<y2<<" - "<<z1<<" * "<<z1<<" + "<<z2<<" * "<<z2<<" = "<<k1<<endl;
	
	cout<<"\n2.Calculating x1,x2 y1,y2 z1,z2 difference"<<endl;
	a1 = 2 * (x2 - x1);
	b1 = 2 * (y2 - y1);	
	c1 = 2 * (z2 - z1);	
	cout<<"> a1 = 2 * (x2 - x1) = 2 * ("<<x2<<" - "<<x1<<") ="<<a1<<endl;
	cout<<"> b1 = 2 * (y2 - y1) = 2 * ("<<y2<<" - "<<y1<<") ="<<b1<<endl;
	cout<<"> c1 = 2 * (z2 - z1) = 2 * ("<<z2<<" - "<<z1<<") ="<<c1<<endl;
	
	cout<<"\n3.Calculating k3"<<endl;
	k3 = r3 * r3 - r2 * r2 - x3 * x3 + x2 * x2 - y3 * y3 + y2 * y2 - z3 * z3 + z2 * z2;
	cout<<"> k3 = r3 * r3 - r2 * r2 - x3 * x3 + x2 * x2 - y3 * y3 + y2 * y2 - z3 * z3 + z2 * z2 = "<<r3<<" * "<<r3<<" - "<<r2<<" * "<<r2<<" - "<<x3<<" * "<<x3<<" + "<<x2<<" * "<<x2<<" - "<<y3<<" * "<<y3<<" + "<<y2<<" * "<<y2<<" - "<<z3<<" * "<<z3<<" + "<<z2<<" * "<<z2<<" = "<<k3<<endl;
	
	cout<<"\n4.Calculating x2,x3 y2,y3 z2,z3 difference"<<endl;
	a3 = 2 * (x2 - x3);
	b3 = 2 * (y2 - y3);
	c3 = 2 * (z2 - z3);
	cout<<"> a3 = 2 * (x2 - x3) = 2 * ("<<x2<<" - "<<x3<<") ="<<a3<<endl;
	cout<<"> b3 = 2 * (y2 - y3) = 2 * ("<<y2<<" - "<<y3<<") ="<<b3<<endl;
	cout<<"> c3 = 2 * (z2 - z3) = 2 * ("<<z2<<" - "<<z3<<") ="<<c3<<endl;
	
    cout<<"\n5.Check a1,a3 values if are zero"<<endl;
	if (a1 == 0) {
	    cout<<"> 5a. a1 = zero"<<endl;
		e = -c1 / b1;
		f = k1 / b1;
		cout<<">> Calculating e = -c1 / b1 = "<<-c1<<"/"<<b1<<" = "<<e<<endl;
		cout<<">> Calculating f = k1 / b1 ="<<k1<<"/"<<b1<<" = "<<f<<endl;	
	} else if (a3 == 0) {
		cout<<"> 5b. a3 = zero"<<endl;
		e = -c3 / b3;
		f = k3 / b3;
		cout<<">> Calculating e = -c3 / b3 = "<<-c3<<"/"<<b3<<" = "<<e<<endl;
		cout<<">> Calculating f = k3 / b3 ="<<k3<<"/"<<b3<<" = "<<f<<endl;		
	} else {
		cout<<"> 5c. a1,a3 = not zero"<<endl;
		a31 = a3 / a1;
		e = - ((a31 * c1 - c3) / (a31 * b1 - b3));
		f = (a31 * k1 - k3) / (a31 * b1 - b3);
		cout<<">> Calculating a31 = a3 / a1 = "<<a3<<"/"<<a1<<" = "<<a31<<endl;
		cout<<">> Calculating e = - ((a31 * c1 - c3) / (a31 * b1 - b3)) ="<<k3<<"/"<<b3<<" = "<<e<<endl;	
	    cout<<">> Calculating f = (a31 * k1 - k3) / (a31 * b1 - b3) ="<<k3<<"/"<<b3<<" = "<<f<<endl;	
	}
	
    cout<<"\n6.Check b1,b3 values if are zero"<<endl;
	if (b1 == 0) {
		g = -c1 / a1;
		h = k1 / a1;
		cout<<"> 6a. b1 = zero"<<endl;
		cout<<">> Calculating g = -c1 / a1 = "<<-c1<<"/"<<a1<<" = "<<g<<endl;
		cout<<">> Calculating h = k1 / a1 ="<<k1<<"/"<<a1<<" = "<<h<<endl;
	} else if (b3 == 0) {
		g = -c3 / a3;
		h = k3 / a3;
	    cout<<"> 6b. b3 = zero"<<endl;
		cout<<">> Calculating g = -c3 / a3 = "<<-c3<<"/"<<a3<<" = "<<g<<endl;
		cout<<">> Calculating h = k3 / a3 = "<<k3<<"/"<<a3<<" = "<<h<<endl;	
	} else {
		b31 = b3 / b1;
		g = - ((b31 * c1 - c3) / (b31 * a1 - a3));
		h = (b31 * k1 - k3) / (b31 * a1 - a3);
	    cout<<"> 6c. b1,b3 = not zero"<<endl;
		cout<<">> Calculating b31 = b3 / b1 = "<<b3<<"/"<<b1<<" = "<<b31<<endl;
		cout<<">> Calculating g = - ((b31 * c1 - c3) / (b31 * a1 - a3)) ="<<g<<endl;	
	    cout<<">> Calculating h = (b31 * k1 - k3) / (b31 * a1 - a3) ="<<k3<<"/"<<b3<<" = "<<h<<endl;
	}
	
    cout<<"\n7.Calculate A B C"<<endl;
	A = g * g + e * e + 1;
	B = -x1 * g - y1 * e - 2 * z1 - x1 * g - y1 * e + 2 * g * h + 2 * e * f;
	C = x1 * x1 + y1 * y1 + z1 * z1 - 2 * x1 * h - 2 * y1 * f + h * h + f * f - r1 * r1;
	cout<<"> A = g * g + e * e + 1 = "<<A<<endl;
	cout<<"> B = -x1 * g - y1 * e - 2 * z1 - x1 * g - y1 * e + 2 * g * h + 2 * e * f = "<<B<<endl;
	cout<<"> C = x1 * x1 + y1 * y1 + z1 * z1 - 2 * x1 * h - 2 * y1 * f + h * h + f * f - r1 * r1 = "<<C<<endl;
	
	cout<<"\n8.Calculate rootD"<<endl;
	rootD = sqrt(B * B - 4 * A * C);
	cout<<"> rootD = sqrt(B * B - 4 * A * C) = sqrt("<<B<<" * "<<B<<" - "<<4<<" * "<<A<<" * "<<C<<") = "<<rootD<<endl;
	
    cout<<"\n9.Calculate x,y,z of unknown node"<<endl;
	z = (-B + rootD) / (2 * A);
	x = g * z + h;
	y = e * z + f;
	cout<<"> z = (-B + rootD) / (2 * A) = ("<<-B<<" + "<<rootD<<" ) / ("<<2<<" *" <<A<<") = "<<z<<endl;
	cout<<"> x = g * z + h = "<<g<<" * "<<z<<" + "<<h<<" = "<<x<<endl;
	cout<<"> y = e * z + f = "<<e<<" * "<<z<<" + "<<f<<" = "<<y<<endl;
	topPyramid.setCoordinates(x,y,z);
	
	x_ = abs(x4-x);
	y_ = abs(y4-y);
	z_ = abs(z4-z);
	
	if(x_<epsilon){
	    x_ =0;
	}
	if(y_<epsilon){
	    y_ =0;
	}
	if(z_<epsilon){
	    z_ =0;
	}
	cout<<"\n**************************Algorithm Finshed***********************************"<<endl;
	
	if(x!= x || y!=y || z!=z ){
		cout<<"Cannot create a triangular pyramid.Implausible values.";
	}
	else{
	    cout<<"\n(h)Expected Value x = "<<x4<<" y = "<<y4<<" z = "<<z4<<endl;
		cout<<"(i)Actual Value   x = "<<x<<" y = "<<y<<" z = "<<z<<endl;
		cout<<"(j)Epsilon e      e = "<<epsilon<<endl;
		cout<<"(k)Error          x = "<<x_<<" y = "<<y_<<" z = "<<z_<<endl;
	}
	
	if(x_==0 && y_==0 && z_==0){
	    cout<<"-------------------------->Test PASSES !!!!!!<---------------------"<<endl;
	}
	else{
		cout<<"--------------------------->Test FAILS<---------------------------- "<<endl;
	}
    cout<<"\n";
   	return topPyramid;
}

#endif 
