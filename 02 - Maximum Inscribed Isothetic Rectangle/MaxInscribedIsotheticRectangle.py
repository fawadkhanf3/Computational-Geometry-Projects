from __future__ import division

import numpy as np


class Edge(object):
    def __init__(self,p,q):
        self.xmin = np.min((p[0],q[0]))
        self.xmax = np.max((p[0],q[0]))
        self.ymin = np.min((p[1],q[1]))
        self.ymax = np.max((p[1],q[1]))
        self.m = float(q[1]-p[1])/float(q[0]-p[0])
        self.b = p[1]-self.m*p[0]
        self.is_top = p[0]>q[0]
        self.is_right = p[1]>q[1]


def compute_edges(convex_hull):
    num_points = len(convex_hull)
    return [Edge(convex_hull[i-1],convex_hull[i]) for i in range(num_points)]

def x_intersect(edges,y):
    x0,x1 = 0,0

    for edge in edges:
        if edge.is_right and edge.ymin <= y <= edge.ymax:
            x0 = (y + 0.5 - edge.b)/edge.m
            x1 = (y - 0.5 - edge.b)/edge.m

    return int(np.floor(np.min((x0,x1))))

def y_intersect(edge,x):
    y_first = edge.m * (x-0.5) + edge.b
    y_last  = edge.m * (x+0.5) + edge.b

    if edge.is_top:
        return int(np.ceil(np.max((y_first,y_last))))

    return int(np.floor(np.min((y_first,y_last))))

def find_edge(edges,is_top,x):
    max_edge = edges[0]
    for edge in edges:
        if edge.xmin != x:
            continue
        if edge.xmin == edge.xmax:
            continue
        if edge.is_top == is_top:
            max_edge = edge
    return max_edge

def compute_largest_rectangle(convex_hull):
    conv_hull_xmin, _ = np.min(convex_hull, axis = 0)
    ind = np.argmax(convex_hull, axis=0)
    conv_hull_xmax, yxmax = convex_hull[ind[0]]
    conv_hull_ymax = convex_hull[ind[1]][1]

    edges = compute_edges(convex_hull)
    int_x = [x_intersect(edges,y) for y in range(conv_hull_ymax)]

    top = find_edge(edges,True,conv_hull_xmin)
    bottom = find_edge(edges,False,conv_hull_xmin)

    aBD = aABC = aABD = aACD = aBCD = max_area = 0
    hAC = wAC = hBD = wBD = hABC = wABC = hABD = wABD = hACD = wACD = hBCD = wBCD = 0

    maxp = np.asarray([0,0])
    pAC = np.asarray([0,0])
    pBD = np.asarray([0,0])
    pABC = np.asarray([0,0])
    pABD = np.asarray([0,0])
    pACD = np.asarray([0,0])
    pBCD = np.asarray([0,0])

    for x in range(conv_hull_xmin,conv_hull_xmax):
        ymin = y_intersect(top,x)
        ymax = y_intersect(bottom,x)

        for ylo in reversed(range(ymin,ymax+1)):
            for yhi in range(ymin,ymax+1):
                if yhi <= ylo:
                    continue

                onA = yhi == ymax and not bottom.is_right
                onD = ylo == ymin and not top.is_right

                xlo = int_x[ylo]
                xhi = int_x[yhi]

                xright = int(np.min((xlo,xhi)))

                onC = xright == xlo and yxmax >= ylo
                onB = xright == xhi and yxmax <= yhi

                height = yhi - ylo
                width = xright - x

                area = width*height

                if onA and onC and not onB and not onD:
                    if area > aAC:
                        aAC = area
                        pAC = np.nsarray([x,ylo])
                        hAC = height
                        wAC = width

                if onB and onD and not onA and not onC:
                    if area > aBD:
                        aBD = area
                        pBD = np.nsarray([x,ylo])
                        hBD = height
                        wBD = width

                if onA and onB and onC:
                    if area > aABC:
                        aABC = area
                        pABC = np.nsarray([x,ylo])
                        hABC = height
                        wABC = width

                if onA and onB and onD:
                    if area > aABD:
                        aABD = area
                        pABD = np.nsarray([x,ylo])
                        hABD = height
                        wABD = width

                if onA and onC and onD:
                    if area > aACD:
                        aACD = area
                        pACD = np.nsarray([x,ylo])
                        hACD = height
                        wACD = width

                if onB and onC and onD:
                    if area > aBCD:
                        aBCD = area
                        pBCD = np.nsarray([x,ylo])
                        hBCD = height
                        wBCD = width

                if area > max_area:
                    max_area = area
                    maxp = np.nsarray([x,ylo])
                    maxw = width
                    maxh = height

        if x == top.xmax:
          top = find_edge(edges,True,x)
        if x == bottom.xmax:
               bottom = find_edge(edges,False,x)

    return np.asarray([[pAC[0], pAC[1], wAC, hAC],
                           [pBD[0], pBD[1], wBD, hBD],
                           [pABC[0], pABC[1], wABC, hABC],
                           [pABD[0], pABD[1], wABD, hABD],
                           [pACD[0], pACD[1], wACD, hACD],
                           [pBCD[0], pBCD[1], wBCD, hBCD],
                           [maxp[0], maxp[1], maxw, maxh]])

polygon = np.nsarray([344,80],
                     [160,82],
                     [163,197],
                     [328,279])

rectanges = compute_largest_rectangle(polygon)


