struct IntervalTree
{
    double discriminant;
    IntervalTree *left_child;
    IntervalTree *right_child;
    Window *window;
    double maxscore; 
    Window *target;
    double excess;
    IntervalTree *father;

    IntervalTree(double discriminant, IntervalTree *father){
        this->discriminant = discriminant;
        this->left_child = NULL;
        this->right_child = NULL;
        this->window = NULL;
        this->maxscore = 0;
        this->target = NULL;
        this->excess = 0;
        this->father = father;
    }

    void display(){
        printf("discriminant: %f\nexcess: %f\nmaxscore: %f\n", discriminant, excess, maxscore);
        if(father != NULL) printf("father (discriminant): %f\n", father->discriminant);
        else puts("father: NULL");

        if(left_child != NULL) printf("left_ch (discriminant): %f\n", left_child->discriminant);
        else puts("left_ch: NULL");

        if(right_child != NULL) printf("right_ch (discriminant): %f\n", right_child->discriminant);
        else puts("right_ch: NULL");

        window->display();
        target->display();
    }
};

