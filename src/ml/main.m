%
% Main driver for Matlab portion of CS598 project.
%


disp('CS598 final project');

 % add other paths to search for functions/scripts
addpath('template','demo');

% test reading audio file from dropbox directory
templatePath = strcat(get_dropbox_path(),'raw_samples/distinct_sounds/a_16bit_48000.wav');
[templateY,templateFs] = audioread(templatePath);
fprintf('Loaded template a. Length: %d, Sample rate: %d \n',size(templateY,1),templateFs);

