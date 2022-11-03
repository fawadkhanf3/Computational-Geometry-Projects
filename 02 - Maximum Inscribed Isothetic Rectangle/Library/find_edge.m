function max_edge = find_edge(edges,is_top,x)

max_edge = edges{1};

for i = 1:length(edges)
    e = edges{i};
    
    if (e.xmin == x)
        if (e.xmax ~= e.xmin)
            if ((e.is_top && is_top) || (~e.is_top && ~is_top))
                max_edge = e;
            end
        end
    end
end

end