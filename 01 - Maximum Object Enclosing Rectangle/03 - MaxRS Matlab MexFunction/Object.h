struct Object
{
    double x,y,weight;
    Object(double x, double y, double weight){
        this->x = x;
        this->y = y;
        this->weight = weight;
    }
    bool operator<(const Object &p)const{
        return y<p.y;
    }
};
