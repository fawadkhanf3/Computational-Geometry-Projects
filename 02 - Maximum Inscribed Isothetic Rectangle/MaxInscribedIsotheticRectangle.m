%% Maximum Inscribed Isothetic Rectangle

clear;close all;clc
format short g
set(0,'DefaultLineLineWidth',2);
addpath(genpath(pwd));

poly = [344, 80;
        160, 82;
        163, 197;
        328, 279]; 
    
poly = [369   438;
        314   519;
        385   582;
        440   501]; 

poly = [2354        2794
        2003        3309
        2457        3708
        2809        3193];  
       
poly = [4,0;
        1,1;
        2,4;
        3,6;
        5,3];    
          
tic;       
rectangles = compute_largest_rectangle(poly.*100);
toc;

maxRect = [rectangles(end,1),rectangles(end,2);
           rectangles(end,1)+rectangles(end,3),rectangles(end,2);
           rectangles(end,1)+rectangles(end,3),rectangles(end,2)+rectangles(end,4);
           rectangles(end,1),rectangles(end,2)+rectangles(end,4)]./100;

figure(1);hold on;grid on;box on;
ps1 = polyshape(poly);
ps2 = polyshape(maxRect);

plot(ps1);
plot(ps2);

rmpath(genpath(pwd));