function x_int = x_intersect(edges,y)
    x0 = 0;
    x1 = 0;
    
    for i = 1:length(edges)
       if ((edges{i}.is_right) && (edges{i}.ymin <= y) && (edges{i}.ymax >= y))
          x0 = ( y + 0.5 - edges{i}.b) / edges{i}.m;
          x1 = ( y - 0.5 - edges{i}.b) / edges{i}.m;
       end
    end
    x_int = floor(min(x0,x1));
end