function edges = compute_edges(convex_hull)

num_points = length(convex_hull);

edges = cell(num_points,1);
edges{1} = Edge(convex_hull(end,:),convex_hull(1,:));
for i = 2:num_points
   edges{i} = Edge(convex_hull(i-1,:),convex_hull(i,:));
end

end