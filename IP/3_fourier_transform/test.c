#include <stdio.h>
#include <complex.h>
#include <math.h>
#define PI 3.141592654
void main()
{
	int negNum = -1;
	double value = -1, result;


	double arg = 360;

   	// Converting to radian
   	arg = (arg * PI) / 180;

	double complex negSqrt = csqrt(negNum);

	double pReal = creal(negSqrt);
	double pImag = cimag(negSqrt);
	double test = cos(arg);

	result = exp(value);

	//printf("Real Part - %f\nImaginary Part - %f\nFor Negative Square Root - %d",pReal, pImag, negNum);
	printf("The Square of 0 is %f\n", test);


}