%% MaxRS

clear;close all;clc
set(0,'DefaultLineLineWidth',2);

mex maximum_targets.cpp

% rng(8);

%%

O = 0;
u = 1000;
v = 1000;

alpha = 100;
beta  = 100;

% Box 1000x1000
XX = [O;u;u;O;O];
YY = [O;O;v;v;O];

N = 50;

x = O + (u-O).*rand(N,1);
y = O + (v-O).*rand(N,1);

data = [x y];

for i = 1:N
    objects(i,1) = Objectt(data(i,1),data(i,2),1); %#ok<*SAGROW>
end

figure(1);hold on;grid on;box on
plot(XX,YY);shg
xlim([O-alpha u+beta]);
ylim([O-alpha v+beta]);

for i = 1:length(objects)
    plot(objects(i,1).x,objects(i,1).y,'*');
end

%% Scheme 01 (MaxRS)
tic;

opt_rect = maximum_targets(data(:,1),data(:,2),[u,v],[alpha,beta]);

x1 = opt_rect(1);
y1 = opt_rect(2);
x2 = opt_rect(3);
y2 = opt_rect(4);

Optimal_Rectangle = Rectangle(x1,y1,x2,y2);

toc;

drawRectangle(Optimal_Rectangle,1);

%% Scheme 02
tic;
xr = min(XX):10:max(XX);
yr = min(YY):10:max(YY);

Max_points = 0;

s = 1;
for j = yr
    for i = xr
        
        boxX = [i;i+alpha;i+alpha;i;i];
        boxY = [j;j;j+beta;j+beta;j];
        
        in = inpolygon(x,y,boxX,boxY);
                  
        max_in = length(find(in));
        
        if(max_in > Max_points)
            Max_points = max_in;
            Max_data   = {boxX boxY x(in) y(in) x(~in) y(~in) Max_points};
        end
        
    end
end
toc;

figure(2);hold on;grid on;
plot(XX,YY);shg
xlim([O-alpha u+beta]);
ylim([O-alpha v+beta]);
plot(Max_data{1},Max_data{2},'k--');
scatter(Max_data{3},Max_data{4},'g*');
scatter(Max_data{5},Max_data{6},'r*');
