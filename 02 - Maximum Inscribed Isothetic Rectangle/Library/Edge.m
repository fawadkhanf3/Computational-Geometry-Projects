classdef Edge
   
    properties
       xmin;
       xmax;
       ymin;
       ymax;
       m;
       b;
       is_top;
       is_right;
    end
    
    methods
        function obj = Edge(p,q)
           obj.xmin = min(p(1),q(1));
           obj.xmax = max(p(1),q(1));
           obj.ymin = min(p(2),q(2));
           obj.ymax = max(p(2),q(2));
           obj.m    = (q(2)-p(2))/(q(1)-p(1));
           obj.b    = p(2)-obj.m*p(1);
           
           obj.is_top   = p(1)>q(1);
           obj.is_right = p(2)>q(2);
        end
    end
    
end