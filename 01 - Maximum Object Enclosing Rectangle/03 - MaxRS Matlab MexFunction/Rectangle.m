classdef Rectangle
    
    properties
        x1;
        x2;
        y1;
        y2;
        weight;
    end
    
    methods 
        function r = Rectangle(x1,y1,x2,y2)
            r.x1 = x1;
            r.y1 = y1;
            r.x2 = x2;
            r.y2 = y2;
            r.weight = 1;
        end
    end
    
end
        
        