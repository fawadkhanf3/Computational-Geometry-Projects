/*
 * Rectangle.h
 *
 * Created by: Ashik <ashik@KAI10>
 * Created on: 2016-10-09
 */
struct Rectangle
{
    double x1, y1, x2, y2, weight;
    Rectangle(double x1, double y1, double x2, double y2, double weight=1.0){
        this->x1 = x1;
        this->x2 = x2;
        this->y1 = y1;
        this->y2 = y2;
        this->weight = weight;
    }
};
