'''
Maximum Rectangle Enclosing Algorithm using Interval Tree
Implementation based on paper: S.C. Nandy and B.B. Bhattacharya. "A Unified Algorithm for Finding Maximum and Minimum Object Enclosing
                                Rectangles and Cuboids."  Computer Math Application. Vol 29. No.8. 1995
Author: Chunxiao Diao + Muhammed Mas-ud Hussain
Last Modified Date: September 21 2015
'''
import sys
import os
import copy
#import matplotlib.pyplot as plt
import pdb
import random


#global variable
#used in incToNode functions to determine whether an interval overlapping/intersecting the left or right of current interval has been found
left_found = False
right_found = False

# 1 is the left one, 2 is the right one
#used to help determine whether to merge two adjacent intervals in decToNode
# left 1 and 2 are the intervals to the left and to the right of the left point of current interval respectively.
#e.g    current interval ->  [2,4] left_intersect1 = [x,2] left_intersect2 = [2,y]    x <2 and 2<y<=4
#same applies to right_intersect
left_intersect1 = None
left_intersect2 = None
right_intersect1 = None
right_intersect2 = None

#the root of interval tree
interval_tree_root = None

class Window():
    def __init__(self,l,r,h,score):
        self.l = l
        self.r = r
        self.h = h
        self.score = score

class IntervalTree():
    def __init__(self,discriminant, father):
        self.discriminant = discriminant
        self.left_child = None
        self.right_child = None
        self.window = None
        self.maxscore = 0
        self.target = None
        self.excess = 0
        self.father = father

class Area():
    def __init__(self,height,width):
        self.height = height
        self.width = width

class Rectangle():
    def __init__(self,x1,y1,x2,y2,weight=1):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.weight = weight

class Object():
    def __init__(self,x,y,weight):
        self.x = x
        self.y = y
        self.weight = weight

# traversal functions used to help with debugging
def preOrderTraverse(root,l):
    if (root == None):
        return
    list = [root.discriminant]
    if (root.window != None):
        list.append([root.window.l,root.window.r,root.window.h,root.window.score])
    l.append(list)
    preOrderTraverse(root.left_child,l)
    preOrderTraverse(root.right_child,l)

def inOrderTraverse(root,l):
    if (root == None):
        return
    inOrderTraverse(root.left_child,l)
    l.append(root.discriminant)
    inOrderTraverse(root.right_child,l)

#build a balanced interval tree
#use the average of two median points as root; attach left nodes(nodes to the left of right medians) as left subtrees and right nodes
# (nodes to the right of left median) as right subtrees
def buildIntervalTree(st,ed,listOfPoints,root):
    if (st == ed):
        leaf_node = IntervalTree(listOfPoints[st],root)
        leaf_node.window = Window(listOfPoints[st],listOfPoints[st],-5,0)
        return leaf_node
    mid = (st + ed) // 2
    new_node = IntervalTree((listOfPoints[mid]+listOfPoints[mid+1])/2,root)
    new_node.left_child  = buildIntervalTree(st,mid,listOfPoints,new_node)
    new_node.right_child = buildIntervalTree(mid+1,ed,listOfPoints,new_node)
    return new_node

#process input
def readInput(area, rectangle):
    #argv[1] is the input filename
    fin = open(sys.argv[1])
    #read area (width height)
    l1 = fin.readline()
    l1=l1.replace('\n','').replace('\t',' ')
    l1=l1.split()
    area.width = float(l1[0])
    area.height = float(l1[1])
    #read rectangle (width height)
    l1 = fin.readline()
    l1=l1.replace('\n','').replace('\t',' ')
    l1=l1.split()
    rectangle.width = float(l1[0])
    rectangle.height = float(l1[1])
    #read points x y weight possibility on each line seperated by a whitespace
    lines = fin.readlines()
    lines = [x.replace('\t',' ').split(' ') for x in lines]
    lines = [[x[0],x[1],x[2],x[3].replace('\n','')] for x in lines]
    objects = [Object(float(x[0]),float(x[1]),float(x[2]),float(x[3])) for x in lines]
    objects.sort(key=lambda m: m.y)
    fin.close()
    return objects

 #draw an object as a red dot
def draw_objects(objects):
    point_xs = [object.x for object in objects]
    point_ys = [object.y for object in objects]
    plt.plot(point_xs,point_ys,'ro')

#draw a rectangle with linewidth = thickness and color = flag
def draw_rectangle(rectangle,thickness,flag='b'):
    line1 = plt.plot([rectangle.x1, rectangle.x1], [rectangle.y1, rectangle.y2])
    line2 = plt.plot([rectangle.x2, rectangle.x2], [rectangle.y1, rectangle.y2])
    line3 = plt.plot([rectangle.x1, rectangle.x2], [rectangle.y1, rectangle.y1])
    line4 = plt.plot([rectangle.x1, rectangle.x2], [rectangle.y2, rectangle.y2])
    plt.setp(line1,color=flag,linewidth=thickness)
    plt.setp(line2,color=flag,linewidth=thickness)
    plt.setp(line3,color=flag,linewidth=thickness)
    plt.setp(line4,color=flag,linewidth=thickness)

#propogate Excess of a father node to its two child nodes. return node V
def findNodeV(root,l,r,h):
    propagateExcess(root,h)
    if (root.discriminant < l):
        return findNodeV(root.right_child,l,r,h)
    elif (root.discriminant > r):
        return findNodeV(root.left_child,l,r,h)
    else:
        return root

#propogate Excess of a father node to its two child nodes. return leaf node l or leaf node r
def findLeafNode(root,v,h):
    propagateExcess(root,h)
    if (root.discriminant == v):
        return root
    if (root.discriminant > v):
        return findLeafNode(root.left_child,v,h)
    if (root.discriminant < v):
        return findLeafNode(root.right_child,v,h)

#propagates Excess of a father node to its two child nodes.
def propagateExcess(root,h):
    if (root.excess != 0):
        if (root.left_child != None):
            root.left_child.excess+=root.excess
            root.left_child.maxscore+=root.excess
            if (root.left_child.window != None):
                root.left_child.window.score+=root.excess
                root.left_child.window.h = h
        if (root.right_child != None):
            root.right_child.excess+=root.excess
            root.right_child.maxscore+=root.excess
            if (root.right_child.window != None):
                root.right_child.window.score+=root.excess
                root.right_child.window.h = h
    root.excess = 0
    
#insert window [a,b] to the first node with discriminant larger than a and smaller than b
def insertWindow(window,root):
    if (window == None):
        return None
    if (root.discriminant <= window.r and root.discriminant >= window.l):
        root.window = window
        return root
    elif root.discriminant < window.l:
        return insertWindow(window,root.right_child)
    else:
        return insertWindow(window,root.left_child)

#when the bottom of a rectangle is processed, we add ([l,r]) it into the interval tree
def incToNodeV(l,r,h,weight,root):
    global left_found
    global right_found
    if root==None:
        return
    if (root.window != None):
        # a window [a,b] in the tree contains interval [l,r]
        # in this case , we break it into three new windows [a,l] [l,r] and [r,b]
        if ((not left_found) and (not right_found) and root.window.l <= l and root.window.r >=r):   ###Case-3
            left_window = None
            right_window = None
            if root.window.l < l:
                left_window = Window(root.window.l,l,h,root.window.score)
            if root.window.r > r:
                right_window = Window(r,root.window.r,h,root.window.score)
            mid_window = Window(l,r,h,root.window.score+weight)
            insertWindow(left_window,root)
            insertWindow(right_window,root)
            insertWindow(mid_window,root)
            left_found = True
            right_found = True
        # a window [a,b] overlap with the left part of interval
        #breaks the window into two windows [a,l] [l,b]
        elif root.window.l < l and root.window.r > l and (not left_found):   ###Case-1L
            mid_window = Window(l,root.window.r,h,root.window.score+weight)
            left_window = Window(root.window.l,l,h,root.window.score)
            insertWindow(left_window,root)
            insertWindow(mid_window,root)
            left_found = True
        # a window [a,b] overlap with the right part of interval
        #breaks the window into two windows [a,r] [r,b]
        elif root.window.l < r and root.window.r > r and (not right_found):    ###Case 1-R
            right_window = Window(r,root.window.r,h,root.window.score)
            mid_window = Window(root.window.l,r,h,root.window.score+weight)
            insertWindow(right_window,root)
            insertWindow(mid_window,root)
            right_found = True
        # interval contains window (only possible on node_v)
        elif root.window.l>=l and root.window.r <= r and (not ((left_found and root.window.l == l) or (right_found and root.window.r == r))):  ####Case-2
            root.window.score+=weight
            root.window.h = h
    if root.discriminant > r:
        return incToNodeV(l,r,h,weight,root.left_child)
    elif root.discriminant < l:
        return incToNodeV(l,r,h,weight,root.right_child)
    else:
        return root

def incToNodeL(l,r,h,weight,root):
    global left_found
    global right_found
    if root==None:
        return
    if (root.window != None):
        #left overlapping
        # a window [a,b] overlap with the left part of interval
        #breaks the window into two windows [a,l] [l,b]
        if root.window.l < l and root.window.r > l and (not left_found):
            mid_window = Window(l,root.window.r,h,root.window.score+weight)
            left_window = Window(root.window.l,l,h,root.window.score)
            insertWindow(left_window,root)
            insertWindow(mid_window,root)
            left_found = True
        # interval contains window
        elif root.window.l>=l and root.window.r <= r and ((not ((left_found and root.window.l == l) or (right_found and root.window.r == r)))
                                                            or root.window.r == root.window.l):
            root.window.score+=weight
            root.window.h = h
    if (root.discriminant == l):
        return root
    elif (root.discriminant < l):
        return incToNodeL(l,r,h,weight,root.right_child)
    elif (root.discriminant > l):
        #right subtree must be contained in the interval
        #change the root's excess
        root.right_child.excess+=weight
        root.right_child.maxscore+=weight
        if (root.right_child.window != None):
            root.right_child.window.score +=weight
            root.right_child.window.h = h
        return incToNodeL(l,r,h,weight,root.left_child)

def incToNodeR(l,r,h,weight,root):
    global left_found
    global right_found
    if root==None:
        return
    if (root.window != None):
        # a window [a,b] overlap with the right part of interval
        #breaks the window into two windows [a,r] [r,b]
        if root.window.r > r  and root.window.l < r and (not right_found):
            right_window = Window(r,root.window.r,h,root.window.score)
            mid_window = Window(root.window.l,r,h,root.window.score+weight)
            insertWindow(right_window,root)
            insertWindow(mid_window,root)
            right_found = True
        # interval contains window
        elif root.window.l>=l and root.window.r <= r and ((not ((left_found and root.window.l == l) or (right_found and root.window.r == r)))
                                                            or root.window.r == root.window.l):
            root.window.score+=weight
            root.window.h = h
    if (root.discriminant == r):
        return root
    elif (root.discriminant > r):
        return incToNodeR(l,r,h,weight,root.left_child)
    elif (root.discriminant < r):
        #left subtree must be contained in the interval
        #change the root's excess
        root.left_child.excess+=weight
        root.left_child.maxscore+=weight
        if root.left_child.window != None:
            root.left_child.window.score+=weight
            root.left_child.window.h = h
        return incToNodeR(l,r,h,weight,root.right_child)

#backward pass. compare the maximum of a node's two children and the score of the window on current node
# chose the largest one as the local maximum
# Changes needed for all-maxrs
def updateToNode(cur, end_node):
    if (cur.window != None and (cur.left_child == None or cur.window.score > cur.left_child.maxscore)
            and (cur.right_child == None or cur.window.score > cur.right_child.maxscore)):
        cur.maxscore = cur.window.score
        cur.target = cur.window
    elif (cur.left_child!= None and (cur.right_child == None or cur.left_child.maxscore > cur.right_child.maxscore)):
        cur.maxscore = cur.left_child.maxscore
        cur.target = cur.left_child.target
    elif cur.right_child != None:
        cur.maxscore = cur.right_child.maxscore
        cur.target = cur.right_child.target
    if cur == end_node:
        return cur.target
    else:
        return updateToNode(cur.father,end_node)

#processing the bottom of a rectangle
#propogate excess first
#then go through the tree to find overlapping or containing windows
# the bottom of the rectangle is namecoded as "the interval"
# the intervals or windows in the interval tree are namecoded "window"
def incIntervalTree(h,l,r,weight,root):
    #pdb.set_trace()
    #window containing interval
    global left_found
    global right_found
    left_found = False
    right_found = False
    #propogate excess
    node_v = findNodeV(root,l,r,h)
    node_l = findLeafNode(root,l,h)
    node_r = findLeafNode(root,r,h)
    #find corresponding overlapping or containing windows and break them into new windows if necessary
    incToNodeV(l,r,h,weight,root)
    incToNodeL(l,r,h,weight,node_v.left_child)
    incToNodeR(l,r,h,weight,node_v.right_child)
    #backward path; update local maximum
    updateToNode(node_l,node_v)
    updateToNode(node_r,node_v)
    updateToNode(node_v,root)



#processing the top of a rectangle case by case
#leaf nodes represent a point and have windows [a,a]
def decToNode(l,r,h,weight,root,flag):
 # global variable definitions included at the beginning of the file for
    global left_intersect1
    global left_intersect2
    global right_intersect1
    global right_intersect2
    if root==None:
        return
    if (root.window != None):
        if root.window.l < root.window.r:
        # since we do not break windows on leaf nodes, we need to check whether the current node is a leaf node first
        #try to find the adjacent pairs that intersect on l and r
            if root.window.l == l:
                left_intersect2 = root
            if root.window.r == l:
                left_intersect1 = root
            if root.window.l == r:
                right_intersect2 = root
            if root.window.r == r:
                right_intersect1 = root
        #if the interval contains the window, change the score of the window
        if root.window.l >= l and root.window.r <= r:
            root.window.score -=weight
            root.window.h = h
        if (left_intersect1 != None and left_intersect2 != None):
            #two adjacent windows that intersect on l are found
            #delete the current window(if the weight difference is equal to the current weight of the interval)
            # merge two windows into the one that is closer to the root
            if left_intersect1.window.score  == left_intersect2.window.score:
                new_window = Window(left_intersect1.window.l,left_intersect2.window.r,left_intersect2.window.h,left_intersect2.window.score)
                left_intersect1.window = None
                left_intersect2.window = None
                #if the right window happens to intersect with point r, the new merged window needs to be marked
                if new_window.r == r:
                    right_intersect1 = insertWindow(new_window,interval_tree_root)
            left_intersect1 = None
            left_intersect2 = None
        if (right_intersect1 != None and right_intersect2 != None):
            #two adjacent windows that intersect on r are found
            #delete the current window, merge both windows into the adjacent one which is closer to the root
            if right_intersect1.window.score  == right_intersect2.window.score:
                new_window = Window(right_intersect1.window.l,right_intersect2.window.r,right_intersect1.window.h,right_intersect1.window.score)
                right_intersect1.window = None
                right_intersect2.window = None
                #if the left window happens to intersect with point r, the new merged window needs to be marked
                if new_window.l == l:
                    left_intersect2 = insertWindow(new_window,interval_tree_root)
                root.window = None
            right_intersect1 = None
            right_intersect2 = None
    if flag == 'v':
        if (root.discriminant > l and root.discriminant < r):
            return
        elif (r < root.discriminant):
            decToNode(l,r,h,weight,root.left_child,flag)
        elif (l > root.discriminant):
            decToNode(l,r,h,weight,root.right_child,flag)
    elif flag == 'l':
        if (root.discriminant == l):
            return
        elif (l < root.discriminant):
            #when traversing nodes on path to l, the right subtrees are all contained in the interval
            root.right_child.excess-=weight
            root.right_child.maxscore-=weight
            if (root.right_child.window != None):
                root.right_child.window.score-=weight
                root.right_child.window.h = h
            decToNode(l,r,h,weight,root.left_child,flag)
        elif (l > root.discriminant):
            decToNode(l,r,h,weight,root.right_child,flag)
    elif flag == 'r':
        if (root.discriminant == r):
            return
        elif (r < root.discriminant):
            decToNode(l,r,h,weight,root.left_child,flag)
        elif (r > root.discriminant):
        #when traversing nodes on path to r, the left subtrees are all contained in the interval
            root.left_child.excess-=weight
            root.left_child.maxscore-=weight
            if root.left_child.window != None:
                root.left_child.window.score-=weight
                root.left_child.window.h = h
            decToNode(l,r,h,weight,root.right_child,flag)

#processing the top of a rectangle
#propogate excess first
#then traverse the interval tree to merge or change affected windows
def decIntervalTree(h,l,r,weight,root):
    if root==None:
        return
    #pdb.set_trace()
    #definitions of global variables are at the beginning of the file
    global left_intersect1
    global left_intersect2
    global right_intersect1
    global right_intersect2
    left_intersect1 = None
    left_intersect2 = None
    right_intersect1 = None
    right_intersect2 = None
    #propage excess
    node_v = findNodeV(root,l,r,h)
    node_l = findLeafNode(root,l,h)
    node_r = findLeafNode(root,r,h)
    #traverse the interval tree to merge or change affected windows
    decToNode(l,r,h,weight,root,'v')
    decToNode(l,r,h,weight,node_v.left_child,'l')
    decToNode(l,r,h,weight,node_v.right_child,'r')
    #update nodes to get best answer
    updateToNode(node_l,node_v)
    updateToNode(node_r,node_v)
    updateToNode(node_v,root)

#sweep lane algorithm from bottom to the top
def max_enclosing(rectangles, coverage, root):
    #optimal answer
    optimal_window = Window(0,0,0,0)
    #top index is the index of the next rectangle whose bottom should be added into interval tree (Note: top index is for bottom edge of a rectangle)
    #it can be interpreted as the top lane of a sweep lane algorithm. the active rectangles are between top index and bot index
    top_index = 0
    #bot index is the index of the next rectangle whose top should be removed from interval tree (Note: bot index is for top edge of a rectangle.)
    bot_index = 0
    while (top_index < len(rectangles)):
        #pdb.set_trace()
        #bottom index is always smaller than top index because we process the bottom of a rectangle before we process the top of a rectangle
        if (rectangles[top_index].y1 <= rectangles[bot_index].y2):
            #print "bot line:",rectangles[top_index].y1,rectangles[top_index].x1,rectangles[top_index].x2
            incIntervalTree(rectangles[top_index].y1,rectangles[top_index].x1,
                                         rectangles[top_index].x2,rectangles[top_index].weight,root)
            ### Mas-ud Modified!!!
            if (root.maxscore > optimal_window.score and root.target!=None):
                optimal_window = copy.deepcopy(root.target)
                optimal_window.score = root.maxscore
                optimal_window.h = rectangles[top_index].y1
            top_index+=1
            #print "local_best",optimal_window.l,optimal_window.r,optimal_window.h, optimal_window.score
        else:
            #print "top line:",rectangles[bot_index].y2,rectangles[bot_index].x1,rectangles[bot_index].x2
            decIntervalTree(rectangles[bot_index].y2,rectangles[bot_index].x1,
                                         rectangles[bot_index].x2,rectangles[bot_index].weight,root)
            bot_index+=1
        '''
        temp_l = []
        preOrderTraverse(root,temp_l)
        print temp_l
        '''
    return optimal_window

###Function that processes MaxRS
def process_maxrs(area, coverage, objects):
    global interval_tree_root
    objects.sort(key=lambda m: m.y)
    #generate rectangles from objects
    rectangles = [Rectangle(max(0,object.x-coverage.width/2),max(0,object.y - coverage.height/2),
                            min(area.width,object.x+coverage.width/2),min(area.height,object.y + coverage.height/2),object.weight) \
                  for object in objects]
    #for rectangle in rectangles:
    #    #print rectangle.x1,rectangle.y1,rectangle.x2,rectangle.y2
    #    draw_rectangle(rectangle,0.2)
    #draw_objects(objects)
    #generate x indices for interval tree
    x1s = [rectangle.x1 for rectangle in rectangles]
    x2s = [rectangle.x2 for rectangle in rectangles]
    x1s.extend(x2s)
    x1s.sort()
    xs=[x1s[0]]
    #delete duplicates indices
    for x in x1s:
        if (x != xs[-1]):
            xs.append(x)
    #build interval tree
    root = buildIntervalTree(0,len(xs)-1,xs,None)
    interval_tree_root = root
    root.window = Window(xs[0],xs[-1],-5,0)
    #window(l, r, h, score)
    '''
    print xs
    preOrder = []
    preOrderTraverse(root,preOrder)
    print preOrder
    inOrder = []
    inOrderTraverse(root,inOrder)
    print inOrder
    '''
    #find the optimal answer
    optimal_window = max_enclosing(rectangles,coverage,root)
    #print optimal_window.l, optimal_window.r, optimal_window.h, optimal_window.score

    #Draw Rectangles and lines
    #ans_line = plt.plot([optimal_window.l, optimal_window.r], [optimal_window.h, optimal_window.h])
    ##use the mid point as center to draw a rectangle
    #ans_rect = Rectangle(optimal_window.l-coverage.width/2, optimal_window.h-coverage.height/2,
    #                        optimal_window.l+coverage.width/2, optimal_window.h+coverage.height/2, optimal_window.score)
    #draw_rectangle(ans_rect,1.0,'y')
    #plt.setp(ans_line,color='y',linewidth=2.0)
    #plt.axis([-5,area.width + 5,-5,area.height + 5])
    #plt.show()
    #plt.clf()
    ### return the answer
    return optimal_window


r_w = 100
r_h = 100
a_w = 1000
a_h = 1000
coverage = Area(r_h, r_w)
area = Area(a_h, a_w)

d_w = coverage.width / 2.0; 
d_h = coverage.height / 2.0;

objects = []
for i in range(20):
    obj = Object(random.randint(0,1000),random.randint(0,1000),1)
    objects.append(obj)

objects.sort(key=lambda m: m.y)
    #generate rectangles from objects
rectangles = [Rectangle(max(0,object.x-coverage.width/2),max(0,object.y - coverage.height/2),
                        min(area.width,object.x+coverage.width/2),min(area.height,object.y + coverage.height/2),object.weight) \
              for object in objects]
x1s = [rectangle.x1 for rectangle in rectangles]
x2s = [rectangle.x2 for rectangle in rectangles]
x1s.extend(x2s)
x1s.sort()
xs=[x1s[0]]
#delete duplicates indices
for x in x1s:
    if (x != xs[-1]):
        xs.append(x)
        
root = buildIntervalTree(0,len(xs)-1,xs,None)

opt_window = process_maxrs(area, coverage, objects)
x_co = (opt_window.l + opt_window.r) / 2.0
y_co = opt_window.h
rect = Rectangle(max(0, x_co - d_w), max(0, y_co - d_h),
                 min(area.width, x_co + d_w), min(area.height, y_co + d_h))

