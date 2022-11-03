function MaxRect = compute_largest_rectangle(convex_hull)

changed = false;
fixed = false;
fixedX = 1;
fixedY = 1;

edges = compute_edges(convex_hull);

conv_hull_xmin = min(convex_hull(:,1),[],1);
[~,ind] = max(convex_hull,[],1);
conv_hull_xmax_yxmax = convex_hull(ind(1),:);
conv_hull_xmax = conv_hull_xmax_yxmax(1);
yxmax          = conv_hull_xmax_yxmax(2);
conv_hull_ymax = max(convex_hull(:,2),[],1);

int_x = zeros(conv_hull_ymax,1);
for y = 1:conv_hull_ymax
    int_x(y) = x_intersect(edges,y);
end

top    = find_edge(edges,true,conv_hull_xmin);
bottom = find_edge(edges,false,conv_hull_xmin);

aAC  = 0;
aBD  = 0;
aABC = 0;
aABD = 0;
aACD = 0;
aBCD = 0;
max_area = 0;

hAC = 0;
wAC = 0;
hBD = 0;
wBD = 0;
hABC = 0;
wABC = 0;
hABD = 0;
wABD = 0;
hACD = 0;
wACD = 0;
hBCD = 0;
wBCD = 0;
maxw = 0;
maxh = 0;

maxp = [0,0];
pAC  = [0,0];
pBD  = [0,0];
pABC = [0,0];
pABD = [0,0];
pACD = [0,0];
pBCD = [0,0];


for x = conv_hull_xmin:conv_hull_xmax-1
    
    ymin = y_intersect(top,x);
    ymax = y_intersect(bottom,x);
    
    for ylo = ymax:-1:ymin
        for yhi = ymin:ymax
            
            if yhi > ylo
                
                onA = (yhi == ymax && ~bottom.is_right);
                onD = (ylo == ymin && ~top.is_right);
                
                xlo = int_x(ylo);
                xhi = int_x(yhi);
                
                xright = min(xlo(1),xhi(1));
                
                onC = (xright == xlo && yxmax >= ylo);
                onB = (xright == xhi && yxmax <= yhi);
                
                height = yhi - ylo;
                width = xright - x;
                
                if (~fixed)
                    
                else
                    
                    fixedWidth = ceil((height*fixedX)/fixedY);
                    
                    if (fixedWidth <= width)
                        width = fixedWidth;
                    else
                        width = 0;
                    end
                end
                
                area = width*height;
                
                if (onA && onC && ~onB && ~onD)
                    if area > aAC
                        aAC = area;
                        pAC = [x,ylo];
                        hAC = height;
                        wAC = width;
                    end
                end
                
                if (onB && onD && ~onA && ~onC)
                    if area > aBD
                        aBD = area;
                        pBD = [x,ylo];
                        hBD = height;
                        wBD = width;
                    end
                end
                
                if (onA && onB && onC)
                    if area > aABC
                        aABC = area;
                        pABC = [x,ylo];
                        hABC = height;
                        wABC = width;
                    end
                end
                
                if (onA && onB && onD)
                    if area > aABD
                        aABD = area;
                        pABD = [x,ylo];
                        hABD = height;
                        wABD = width;
                    end
                end
                
                if (onA && onC && onD)
                    if area > aACD
                        aACD = area;
                        pACD = [x,ylo];
                        hACD = height;
                        wACD = width;
                    end
                end
                
                if (onB && onC && onD)
                    if area > aBCD
                        aBCD = area;
                        pBCD = [x,ylo];
                        hBCD = height;
                        wBCD = width;
                    end
                end
                
                if area > max_area
                    max_area = area;
                    maxp = [x,ylo];
                    maxw = width;
                    maxh = height;
                    
                end
                
            end
        end
    end
    
    if x == top.xmax
        top = find_edge(edges,true,x);
    end
    if x == bottom.xmax
        bottom = find_edge(edges,false,x);
    end
    
end

MaxRect = [pAC(1), pAC(2), wAC, hAC;
    pBD(1), pBD(2), wBD, hBD;
    pABC(1), pABC(2), wABC, hABC;
    pABD(1), pABD(2), wABD, hABD;
    pACD(1), pACD(2), wACD, hACD;
    pBCD(1), pBCD(2), wBCD, hBCD;
    maxp(1), maxp(2), maxw, maxh];

end