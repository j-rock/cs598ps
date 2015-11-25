%
% Generate a group spectrogram for multiple audio templates.
% Each template is the same length to make it easier to group
% together.
%

disp('Generate spectrogram for multiple templates');

% add other paths to search for functions/scripts
addpath('template','demo','doc');

% read audio template files from dropbox directory
aTemplatesPath = strcat(get_dropbox_path(),'new_templates/templates_acombined.wav');
eTemplatesPath = strcat(get_dropbox_path(),'new_templates/templates_ecombined.wav');
[aTemplateY,aTemplateFs] = audioread(aTemplatesPath);
[eTemplateY,eTemplateFs] = audioread(eTemplatesPath);
y = aTemplateY(:,1); % extract the first channel
Fs = aTemplateFs;
y2 = eTemplateY(:,1); % extract the first channel
Fs2 = eTemplateFs;

% generate spectrogram data for each audio file
[spec,fMax,tMax] = make_spectrogram(y,64,Fs);
[spec2,fMax,tMax] = make_spectrogram(y2,64,Fs2);

%--------------------------------------
% Create Separate Template Spectrograms
%--------------------------------------
% Run the section above first
%%
figure('Name',sprintf('Separate Template Spectrograms'));

subplot(2,1,1);
imagesc([0 tMax],[0 fMax],spec);
colorbar;
title('Spectrogram for a template with Window N=64');
xlabel('Time (sec)');
ylabel('Frequency');
set(gca,'YDir','normal');

subplot(2,1,2);
imagesc([0 tMax],[0 fMax],spec2);
colorbar;
title('Spectrogram for e template with Window N=64');
xlabel('Time (sec)');
ylabel('Frequency');
set(gca,'YDir','normal');

%--------------------------------------
% Create Combined Template Spectrogram
%--------------------------------------
%%
figure('Name',sprintf('Combined Template Spectrogram'));

subplot(1,1,1);
imagesc([0 5],[1 2],[spec2;spec]);
colorbar;
title('Spectrogram for a template with Window N=64');
xlabel('Time (sec)');
ylabel('Frequency');
set(gca,'YDir','normal'); % 'YDir','reverse'  OR 'YDir','normal'

%--------------------------------------
% Alternative Combined Template Spectrogram
%--------------------------------------
%%

img = mat2gray([spec;spec2]);
imshow(img)