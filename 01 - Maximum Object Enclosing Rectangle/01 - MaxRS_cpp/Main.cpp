#include <iostream>
#include <conio.h>
#include <cstring>
#include <cstddef>

#include <stdlib.h>
#include <stdio.h>

#include "Area.h"
#include "Object.h"
#include "Window.h"
#include "Rectangle.h"
#include "IntervalTree.h"

#include <algorithm>
#include <vector>
#include <set>

using namespace std;

double d_w, d_h; 
bool left_found = false;
bool right_found = false;

IntervalTree *left_intersect1 = NULL;
IntervalTree *left_intersect2 = NULL;
IntervalTree *right_intersect1 = NULL;
IntervalTree *right_intersect2 = NULL;

IntervalTree *interval_tree_root = NULL;

void restrict_precision(double &val)
{
	val = roundf(val * 1000000000) / 1000000000;
}

void restrict_precision(vector<Object> &objects)
{
	for (int i = 0; i<objects.size(); i++) {
		restrict_precision(objects[i].x);
		restrict_precision(objects[i].y);
	}
}

IntervalTree* buildIntervalTree(int st, int ed, vector<double> listOfPoints, IntervalTree *root)
{
	if (st == ed) {
		IntervalTree *leaf_node = new IntervalTree(listOfPoints[st], root);
		leaf_node->window = new Window(listOfPoints[st], // l
			listOfPoints[st], // r
			(double)(-5), // h
			(double)(0)); // score
		return leaf_node;
	}

	int mid = (st + ed) / 2;

	IntervalTree *new_node = new IntervalTree((listOfPoints[mid] + listOfPoints[mid + 1]) / 2, root);

	new_node->left_child = buildIntervalTree(st, mid, listOfPoints, new_node);
	new_node->right_child = buildIntervalTree(mid + 1, ed, listOfPoints, new_node);
	return new_node;
}

void preOrderTraverse(IntervalTree *root)
{
	if (root == NULL) return;

	root->display();
	preOrderTraverse(root->left_child);
	preOrderTraverse(root->right_child);
}

// propagate Excess of a father node to its two child nodes.
void propagateExcess(IntervalTree *root, double h)
{
	if (root->excess != 0)
	{
		if (root->left_child != NULL)
		{
			root->left_child->excess += root->excess;
			root->left_child->maxscore += root->excess;
			if (root->left_child->window != NULL)
			{
				root->left_child->window->score += root->excess;
				root->left_child->window->h = h;
			}
		}
		if (root->right_child != NULL)
		{
			root->right_child->excess += root->excess;
			root->right_child->maxscore += root->excess;
			if (root->right_child->window != NULL)
			{
				root->right_child->window->score += root->excess;
				root->right_child->window->h = h;
			}
		}
	}
	root->excess = 0;
}


IntervalTree* findNodeV(IntervalTree *root, double l, double r, double h)
{
	propagateExcess(root, h);

	if (root->discriminant < l) return findNodeV(root->right_child, l, r, h);
	else if (root->discriminant > r) return findNodeV(root->left_child, l, r, h);
	return root;
}

IntervalTree* findLeafNode(IntervalTree *root, double v, double h)
{
	propagateExcess(root, h);
	if (root->discriminant == v) return root;
	if (root->discriminant > v) return findLeafNode(root->left_child, v, h);
	if (root->discriminant < v) return findLeafNode(root->right_child, v, h);
	return NULL; // suppress warning
}

// insert window [a,b] to the first node with discriminant larger than a
// and smaller than b
IntervalTree* insertWindow(Window *window, IntervalTree *root)
{
	if (window == NULL) return NULL;
	if (root->discriminant <= window->r && root->discriminant >= window->l)
	{
		root->window = window;
		return root;
	}
	else if (root->discriminant < window->l) return insertWindow(window, root->right_child);
	return insertWindow(window, root->left_child);
}

// when the bottom of a rectangle is processed, we add ([l,r]) it
// into the interval tree
IntervalTree* incToNodeV(double l, double r, double h, double weight, IntervalTree *root)
{
	if (root->window != NULL)
	{
		// a window [a,b] in the tree contains interval [l,r]
		// in this case , we break it into three new windows [a,l] [l,r] and [r,b]
		if ((!left_found) && (!right_found) && (root->window->l <= l) && (root->window->r >= r))
		{
			Window *left_window = NULL;
			Window *right_window = NULL;
			// [l, r] -> [root.window.l, l] [l,r] [r, root.window.r]
			if (root->window->l < l) left_window = new Window(root->window->l, l, h, root->window->score);
			if (root->window->r > r) right_window = new Window(r, root->window->r, h, root->window->score);
			Window *mid_window = new Window(l, r, h, root->window->score + weight);

			insertWindow(left_window, root);
			insertWindow(right_window, root);
			insertWindow(mid_window, root);
			left_found = true;
			right_found = true;
		}
		else if ((root->window->l < l) && (root->window->r > l) && (!left_found))
		{
			// a window [a,b] overlap with the left part of interval
			// breaks the window into two windows [a,l] [l,b]
			// or [root.window.l, l] [l, root.window.r]
			Window *mid_window = new Window(l, root->window->r, h, root->window->score + weight);
			Window *left_window = new Window(root->window->l, l, h, root->window->score);
			insertWindow(left_window, root);
			insertWindow(mid_window, root);
			left_found = true;
		}
		else if ((root->window->l < r) && (root->window->r > r) && (!right_found))
		{
			// a window [a,b] overlap with the right part of interval
			// breaks the window into two windows [a,r] [r,b]
			// [root.window.l, r] [r, root.window. r]
			Window *right_window = new Window(r, root->window->r, h, root->window->score);
			Window *mid_window = new Window(root->window->l, r, h, root->window->score + weight);
			insertWindow(right_window, root);
			insertWindow(mid_window, root);
			right_found = true;
		}
		else if ((root->window->l >= l) && (root->window->r <= r) &&
			(!((left_found && (root->window->l == l)) ||
				(right_found && (root->window->r == r)))))
		{
			root->window->score += weight;
			root->window->h = h;
		}

		if (root->discriminant > r) return incToNodeV(l, r, h, weight, root->left_child);
		else if (root->discriminant < l) return incToNodeV(l, r, h, weight, root->right_child);
		return root;
	}
	return NULL; // suppress warnings
}

IntervalTree* incToNodeL(double l, double r, double h, double weight, IntervalTree *root)
{
	if (root->window != NULL) {
		// left overlapping
		// a window [a,b] overlap with the left part of interval
		// breaks the window into two windows [a,l] [l,b]
		if ((root->window->l < l) && (root->window->r > l) &&
			(!left_found))
		{
			Window *mid_window = new Window(l, root->window->r, h, root->window->score + weight);
			Window *left_window = new Window(root->window->l, l, h, root->window->score);
			insertWindow(left_window, root);
			insertWindow(mid_window, root);
			left_found = true;
		}
		else if ((root->window->l >= l) && (root->window->r <= r) &&
			((!((left_found && (root->window->l == l)) ||
				(right_found && root->window->r == r))) ||
				(root->window->r == root->window->l)))
		{
			// interval contains window
			root->window->score += weight;
			root->window->h = h;
		}
	}

	if (root->discriminant == l) return root;
	else if (root->discriminant < l) return incToNodeL(l, r, h, weight, root->right_child);
	else if (root->discriminant > l)
	{
		// right subtree must be contained in the interval
		// change the root's excess
		root->right_child->excess += weight;
		root->right_child->maxscore += weight;
		if (root->right_child->window != NULL)
		{
			root->right_child->window->score += weight;
			root->right_child->window->h = h;
		}
		return incToNodeL(l, r, h, weight, root->left_child);
	}
	return NULL;
}

IntervalTree* incToNodeR(double l, double r, double h, double weight, IntervalTree *root)
{
	if (root->window != NULL)
	{
		if ((root->window->r > r) && (root->window->l < r) && (!right_found))
		{
			// a window [a,b] overlap with the right part of interval
			// breaks the window into two windows [a,r] [r,b]
			Window *right_window = new Window(r, root->window->r, h, root->window->score);
			Window *mid_window = new Window(root->window->l, r, h, root->window->score + weight);
			insertWindow(right_window, root);
			insertWindow(mid_window, root);
			right_found = true;
		}
		else if ((root->window->l >= l) && (root->window->r <= r) &&
			((!((left_found && (root->window->l == l)) ||
				(right_found && (root->window->r == r)))) ||
				(root->window->r == root->window->l)))
		{
			root->window->score += weight;
			root->window->h = h;
		}
	}

	if (root->discriminant == r) return root;
	else if (root->discriminant > r) return incToNodeR(l, r, h, weight, root->left_child);
	else if (root->discriminant < r)
	{
		// left subtree must be contained in the interval
		// change the root's excess
		root->left_child->excess += weight;
		root->left_child->maxscore += weight;
		if (root->left_child->window != NULL)
		{
			root->left_child->window->score += weight;
			root->left_child->window->h = h;
		}
		return incToNodeR(l, r, h, weight, root->right_child);
	}
	return NULL; // suppress warnings
}

// backward path. compare the maximum of a node's two children and the
// score of the window on current node
// chose the largest one as the local maximum
Window* updateToNode(IntervalTree *cur, IntervalTree *end_node)
{
	if ((cur->window != NULL) &&
		((cur->left_child == NULL) || (cur->window->score > cur->left_child->maxscore)) &&
		((cur->right_child == NULL) || (cur->window->score > cur->right_child->maxscore)))
	{
		cur->maxscore = cur->window->score;
		cur->target = cur->window;
	}
	else if ((cur->left_child != NULL) &&
		((cur->right_child == NULL) ||
			cur->left_child->maxscore > cur->right_child->maxscore))
	{
		cur->maxscore = cur->left_child->maxscore;
		cur->target = cur->left_child->target;
	}
	else if (cur->right_child != NULL)
	{
		cur->maxscore = cur->right_child->maxscore;
		cur->target = cur->right_child->target;
	}

	if (cur == end_node) return cur->target;
	return updateToNode(cur->father, end_node);
}

// processing the bottom of a rectangle
// propogate excess first
// then go through the tree to find overlapping or containing windows
// the bottom of the rectangle is namecoded as "the interval"
// the intervals or windows in the interval tree are namecoded "window"
void incIntervalTree(double h, double l, double r, double weight, IntervalTree *root)
{
	left_found = false;
	right_found = false;

	IntervalTree *node_v = findNodeV(root, l, r, h);
	IntervalTree *node_l = findLeafNode(root, l, h);
	IntervalTree *node_r = findLeafNode(root, r, h);

	incToNodeV(l, r, h, weight, root);

	incToNodeL(l, r, h, weight, node_v->left_child);

	incToNodeR(l, r, h, weight, node_v->right_child);

	updateToNode(node_l, node_v);
	updateToNode(node_r, node_v);
	updateToNode(node_v, root);
}

// processing the top of a rectangle case by case
// leaf nodes represent a point and have windows [a,a]
void decToNode(double l, double r, double h, double weight, IntervalTree *root, char flag)
{
	if (root->window != NULL)
	{
		if (root->window->l < root->window->r)
		{
			// since we do not break windows on leaf nodes, we need to
			// check whether the current node is a leaf node first
			// try to find the adjacent pairs that intersect on l and r
			if (root->window->l == l) left_intersect2 = root;
			if (root->window->r == l) left_intersect1 = root;
			if (root->window->l == r) right_intersect2 = root;
			if (root->window->r == r) right_intersect1 = root;
		}
		// if the interval contains the window, change the score of the window
		if ((root->window->l >= l) && (root->window->r <= r))
		{
			root->window->score -= weight;
			root->window->h = h;
		}

		if ((left_intersect1 != NULL) && (left_intersect2 != NULL))
		{
			// two adjacent windows that intersect on l are found
			// delete the current window(if the weight difference is
			// equal to the current weight of the interval)
			// merge two windows into the one that is closer to the root
			if ((left_intersect1->window->score == left_intersect2->window->score))
			{
				Window *new_window = new Window(left_intersect1->window->l,
					left_intersect2->window->r,
					left_intersect2->window->h,
					left_intersect2->window->score);
				left_intersect1->window = NULL;
				left_intersect2->window = NULL;
				if (new_window->r == r) right_intersect1 = insertWindow(new_window, interval_tree_root);
			}
			left_intersect1 = NULL;
			left_intersect2 = NULL;
		}

		if ((right_intersect1 != NULL) && (right_intersect2 != NULL))
		{
			// two adjacent windows that intersect on r are found
			// delete the current window, merge both windows into the
			// adjacent one which is closer to the root
			if (right_intersect1->window->score == right_intersect2->window->score)
			{
				Window *new_window = new Window(right_intersect1->window->l,
					right_intersect2->window->r,
					right_intersect1->window->h,
					right_intersect1->window->score);
				right_intersect1->window = NULL;
				right_intersect2->window = NULL;
				// if the left window happens to intersect with point
				// r, the new merged window needs to be marked
				if (new_window->l == l) left_intersect2 = insertWindow(new_window, interval_tree_root);
				root->window = NULL;
			}
			right_intersect1 = NULL;
			right_intersect2 = NULL;
		}
	}

	if (flag == 'v')
	{
		if ((root->discriminant > l) && (root->discriminant < r)) return;
		else if (r < root->discriminant) decToNode(l, r, h, weight, root->left_child, flag);
		else if (l > root->discriminant) decToNode(l, r, h, weight, root->right_child, flag);
	}
	else if (flag == 'l')
	{
		if (root->discriminant == l) return;
		else if (l < root->discriminant)
		{
			root->right_child->excess -= weight;
			root->right_child->maxscore -= weight;
			if (root->right_child->window != NULL)
			{
				root->right_child->window->score -= weight;
				root->right_child->window->h = h;
			}
			decToNode(l, r, h, weight, root->left_child, flag);
		}
		else if (l > root->discriminant) decToNode(l, r, h, weight, root->right_child, flag);
	}
	else if (flag == 'r')
	{
		if (root->discriminant == r) return;
		else if (r < root->discriminant) decToNode(l, r, h, weight, root->left_child, flag);
		else if (r > root->discriminant)
		{
			root->left_child->excess -= weight;
			root->left_child->maxscore -= weight;
			if (root->left_child->window != NULL)
			{
				root->left_child->window->score -= weight;
				root->left_child->window->h = h;
			}
			decToNode(l, r, h, weight, root->right_child, flag);
		}
	}
}

// processing the top of a rectangle
// propogate excess first
// then traverse the interval tree to merge or change affected windows
void decIntervalTree(double h, double l, double r, double weight, IntervalTree *root)
{

	left_intersect1 = NULL;
	left_intersect2 = NULL;
	right_intersect1 = NULL;
	right_intersect2 = NULL;

	IntervalTree *node_v = findNodeV(root, l, r, h);

	IntervalTree *node_l = findLeafNode(root, l, h);
	IntervalTree *node_r = findLeafNode(root, r, h);

	decToNode(l, r, h, weight, root, 'v');
	decToNode(l, r, h, weight, node_v->left_child, 'l');
	decToNode(l, r, h, weight, node_v->right_child, 'r');

	updateToNode(node_l, node_v);
	updateToNode(node_r, node_v);
	updateToNode(node_v, root);

}

Window* maxEnclosing(vector<Rectangle> &aListOfRectangles, Area coverage, IntervalTree *root)
{
	// optimal answer
	Window *optimalWindow = new Window(0, 0, 0, 0);
	// top index is the index of the next rectangle whose bottom should
	// be added into interval tree (Note: top index is for bottom edge
	// of a rectangle) it can be interpreted as the top lane of a sweep
	// lane algorithm. the active rectangles are between top index and
	// bot index
	int topIndex = 0;
	// bot index is the index of the next rectangle whose top should be
	// removed from interval tree (Note: bot index is for top edge of a
	// rectangle.)
	int botIndex = 0;
	while (topIndex < aListOfRectangles.size())
	{
		// bottom index is always smaller than top index because we
		// process the bottom of a rectangle before we process the top
		// of a rectangle
		if (aListOfRectangles[topIndex].y1 <= aListOfRectangles[botIndex].y2)
		{

			incIntervalTree(aListOfRectangles[topIndex].y1,
				aListOfRectangles[topIndex].x1,
				aListOfRectangles[topIndex].x2,
				aListOfRectangles[topIndex].weight,
				root);

			if (root->maxscore > optimalWindow->score)
			{
				optimalWindow = (Window*)root->target->clone();
				optimalWindow->score = root->maxscore;
				optimalWindow->h = aListOfRectangles[topIndex].y1;
			}
			topIndex++;

			if (root != NULL);

		}
		else
		{

			decIntervalTree(aListOfRectangles[botIndex].y2,
				aListOfRectangles[botIndex].x1,
				aListOfRectangles[botIndex].x2,
				aListOfRectangles[botIndex].weight,
				root);

			botIndex++;
			if (root != NULL);

		} // end else
	} // end while
	return optimalWindow;
}

Window* process_maxrs(Area area, Area coverage, vector<Object> &objects)
{
	restrict_precision(objects);

	/*
	cout << "computing maxrs with " << objects.size() << " objects.\n";
	for(int i=0; i<objects.size(); i++){
	cout << objects[i].x << ' ' << objects[i].y << ' ' << objects[i].weight << endl;
	}
	*/

	sort(objects.begin(), objects.end());
	///cout << "sorted\n";
	///print to see the objects

	cout << "computing maxrs with " << objects.size() << " objects.\n";
	cout << "[x   y] " << endl;
	for(int i=0; i<objects.size(); i++){
		cout << objects[i].x << ' ' << objects[i].y << endl;// << ' ' << objects[i].weight << endl;
	}

	vector<Rectangle> rectangles; ///contains all the rectangles
	for (int i = 0; i<objects.size(); i++)
	{
		Rectangle temp(max(0.0, objects[i].x - coverage.width / 2), max(0.0, objects[i].y - coverage.height / 2),
			min(area.width, objects[i].x + coverage.width / 2), min(area.height, objects[i].y + coverage.height / 2),
			objects[i].weight);
		rectangles.push_back(temp);
	}

	///print to see the rectangles
	///cout << "rectangles created\n";

	vector<double> x1s, xs; ///x1s contains all the x coords, xs contains unique x coords sorted
	for (int i = 0; i<rectangles.size(); i++)
	{
		x1s.push_back(rectangles[i].x1);
		x1s.push_back(rectangles[i].x2);
	}

	sort(x1s.begin(), x1s.end());

	//cout.precision(20);

	xs.push_back(x1s[0]);
	double last = x1s[0];
	for (int i = 1; i<x1s.size(); i++)
	{
		//cout << "cur: " << x1s[i] << " last: " << last << endl;
		if (fabs(x1s[i] - last) == 0) continue;
		xs.push_back(x1s[i]);
		//cout << x1s[i] << " pushed\n";
		last = x1s[i];
	}

	/*
	///print to see xs
	printf("xs created, size = %d\n", (int)xs.size());
	for(int i=0; i<xs.size(); i++) cout << xs[i] << ' ';
	cout << "\n\n";
	*/

	IntervalTree *root = buildIntervalTree(0, xs.size() - 1, xs, NULL);

	///puts("tree built");
	//puts("$$$$$$$$$$$$$$$$$$$$$$$$$$");
	//preOrderTraverse(root);
	//puts("$$$$$$$$$$$$$$$$$$$$$$$$$$");

	interval_tree_root = root;
	root->window = new Window(xs[0], xs[xs.size() - 1], (double)(-5), (double)(0));

	///puts("root window created.");

	Window *optimal_window = maxEnclosing(rectangles, coverage, root);
	///GETTING SEGMENTATION FAULT HERE

	return optimal_window;
}


void main()
{
	srand(8);
	const double r_w = 1000;
	const double r_h = 1000;
	const double a_w = 100;
	const double a_h = 100;

	Area coverage(a_h, a_w);
	Area area(r_h, r_w);

	d_w = coverage.width / 2.0; /// r_w/2
	d_h = coverage.height / 2.0; /// r_h/2

	// perform the initial maxrs
	vector<Object> objects;
	for (int i = 0; i < 50; i++) {
		Object temp(200+(1000-200)*rand()/RAND_MAX, 200 + (1000 - 200)*rand()/RAND_MAX,1);
		objects.push_back(temp);
	}

	Window *opt_window = process_maxrs(area, coverage, objects);

	/// Find the objects within MaxRS solution
	double x_co = (opt_window->l + opt_window->r) / 2.0, y_co = opt_window->h;
	Rectangle rect(max(0.0, x_co - d_w), max(0.0, y_co - d_h), min(area.width, x_co + d_w), min(area.height, y_co + d_h));

	cout << "\n Optimal Rectangle Coordinates: " << endl;
	cout << " x1 = " << rect.x1 << endl;
	cout << " x2 = " << rect.x2 << endl;
	cout << " y1 = " << rect.y1 << endl;
	cout << " y2 = " << rect.y2 << endl;

	_getch();
}
