function y_int = y_intersect(edge,x)

y_first = edge.m * (x - 0.5) + edge.b;
y_last  = edge.m * (x + 0.5) + edge.b;

if edge.is_top
    y_int = ceil(max(y_first,y_last));
else
    y_int = floor(min(y_first,y_last));
end

end