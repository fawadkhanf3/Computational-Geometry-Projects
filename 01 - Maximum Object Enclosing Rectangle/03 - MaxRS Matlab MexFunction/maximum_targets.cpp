#include "MaxRS.cpp"
#include "mex.h"
#include <conio.h>
#include <math.h>
using namespace std;

// Mex-Function (Gateway to MATLAB)
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
	double *x_coords; // Pointers to Input Array
	double *y_coords; // Pointers to Input Array
	const double *uv, *ab;

	x_coords = mxGetPr(prhs[0]); // Input Array 1
	y_coords = mxGetPr(prhs[1]); // Input Array 2
	uv = mxGetPr(prhs[2]);
	ab = mxGetPr(prhs[3]);

	const double r_w = uv[0];
	const double r_h = uv[1];
	const double a_w = ab[0];
	const double a_h = ab[1];

	int N = (int)mxGetNumberOfElements(prhs[0]);

	Area coverage(a_h, a_w);
	Area area(r_h, r_w);

	d_w = coverage.width / 2.0;
	d_h = coverage.height / 2.0; 

	// perform the initial maxrs
	vector<Object> objects;
	for (int i = 0; i < N; i++) {
		Object temp(x_coords[i], y_coords[i], 1);
		objects.push_back(temp);
	}

	Window *opt_window = process_maxrs(area, coverage, objects);

	/// Find the objects within MaxRS solution
	double x_co = (opt_window->l + opt_window->r) / 2.0, y_co = opt_window->h;
	Rectangle rect(max(0.0, x_co - d_w), max(0.0, y_co - d_h), min(area.width, x_co + d_w), min(area.height, y_co + d_h));

	plhs[0] = mxCreateDoubleMatrix(4, 1, mxREAL);

	double *opt_rectangle;
	opt_rectangle = mxGetPr(plhs[0]);

	opt_rectangle[0] = rect.x1;
	opt_rectangle[1] = rect.y1;
	opt_rectangle[2] = rect.x2;
	opt_rectangle[3] = rect.y2;

}