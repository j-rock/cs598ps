%
% Generate a plot for the results
%

% add other paths to search for functions/scripts
addpath('template','demo','doc');

%%
% Plot the results for the single-class Yes/No classification
%
x=linspace(1,5,5)
y=[0.91 0.875 0.95 0.91 0.91]
n=[0.83 0.95 0.91 0.91 0.875]
yg=[0.67 0.67 0.67 0.70 0.75]
ng=[0.67 0.75 0.75 0.625 0.70]


figure('Name',sprintf('Plot Results'),'Color',[1.0 1.0 1.0]);

hold all;
plot(x,y,x,n)
plot(x,yg,'Color',[1.0 0.0 0.0]);
title('Yes/No Classification');
xlabel('Test Runs')
ylabel('Accuracy')
ylim([0 1])
legend('yes','no','baseline');

%%
% Plot the results for the single-class Vowel classification
%
x=linspace(1,5,5)
a=[0.86 0.90 0.86 0.94 0.82]
e=[0.88 0.90 0.90 0.88 0.90]
i=[0.77 0.75 0.81 0.79 0.79]
o=[0.90 0.86 0.88 0.90 1.0]
u=[0.84 0.86 0.92 0.92 0.90]
bg=[0.72 0.74 0.74 0.76 0.70]


figure('Name',sprintf('Plot Results'),'Color',[1.0 1.0 1.0]);

hold all;
plot(x,a,x,e,x,i,x,o,x,u)
plot(x,bg,'Color',[1.0 0.0 0.0]);
title('Vowel Classification');
xlabel('Test Runs')
ylabel('Accuracy')
ylim([0 1])
legend('a','e','i','o','u','baseline');

%%
% Plot the results for the multi-class yes/no classification
%
x=linspace(1,10,10)
yn=[0.90 0.74 0.77 0.77 0.80 1.0 0.74 0.87 0.90 0.90]
ynbg=[0.51 0.45 0.41 0.54 0.48 0.54 0.51 0.45 0.48 0.51]


figure('Name',sprintf('Plot Results'),'Color',[1.0 1.0 1.0]);

hold all;
plot(x,yn)
plot(x,ynbg,'Color',[1.0 0.0 0.0]);
title('Yes/No Classification');
xlabel('Test Runs')
ylabel('Accuracy')
ylim([0 1])
legend('yes/no','baseline');

%%
% Plot the results for the multi-class yes/no classification
%
x=linspace(1,10,10)
v=[0.62 0.73 0.68 0.71 0.65 0.67 0.69 0.71 0.63 0.61]
vbg=[0.25 0.36 0.37 0.39 0.34 0.37 0.37 0.33 0.38 0.26]
yn=[0.90 0.74 0.77 0.77 0.80 1.0 0.74 0.87 0.90 0.90]
ynbg=[0.51 0.45 0.41 0.54 0.48 0.54 0.51 0.45 0.48 0.51]


figure('Name',sprintf('Plot Results'),'Color',[1.0 1.0 1.0]);

hold all;
plot(x,yn)
plot(x,ynbg,':','Color',[1.0 0.0 0.0]);
plot(x,v)
plot(x,vbg,'--','Color',[1.0 0.0 0.0]);

title('Multi-Class Classification');
xlabel('Test Runs')
ylabel('Accuracy')
ylim([0 1])
legend('yes/no','yes/no baseline','vowels','vowels baseline');