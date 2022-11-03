struct Window
{
    double l, r, h, score;

    Window(double l, double r, double h, double score){
        this->l = l;
        this->r = r;
        this->h = h;
        this->score = score;
    }

    Window* clone(){
        Window *clone = new Window(l, r, h, score);
        return clone;
    }

    void display(){
        printf("l: %f\nr: %f\nh: %f\nscore: %f\n", l, r, h, score);
    }
};

