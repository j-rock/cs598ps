%
% Generate a group spectrogram for multiple audio templates.
% Each template is the same length to make it easier to group
% together.
%

disp('Generate spectrogram for multiple templates');

% add other paths to search for functions/scripts
addpath('template','demo','doc');

% read audio template files from dropbox directory
%aTemplatesPath = strcat(get_dropbox_path(),'vowels-test/samples/sample_Q1_0002_1_A1.wav');
%eTemplatesPath = strcat(get_dropbox_path(),'vowels-test/samples/sample_Q1_0005_1_E1.wav');
aTemplatesPath = strcat(get_dropbox_path(),'vowels-test/samples/sample_Q1_0008_1_I1.wav');
%eTemplatesPath = strcat(get_dropbox_path(),'vowels-test/samples/sample_Q1_0011_1_O1.wav');
eTemplatesPath = strcat(get_dropbox_path(),'vowels-test/samples/sample_Q1_0014_1_U1.wav');
[aTemplateY,aTemplateFs] = audioread(aTemplatesPath);
[eTemplateY,eTemplateFs] = audioread(eTemplatesPath);

fraction=0.3;
length=fraction*aTemplateFs;

y = aTemplateY(1:length,1); % extract the first channel
Fs = aTemplateFs;
y2 = eTemplateY(1:length,1); % extract the first channel
Fs2 = eTemplateFs;

% generate spectrogram data for each audio file
[spec,fMax,tMax] = make_spectrogram(y,64,Fs);
[spec2,fMax,tMax] = make_spectrogram(y2,64,Fs2);

%--------------------------------------
% Create Separate Template Spectrograms
%--------------------------------------
% Run the section above first
%%
figure('Name',sprintf('Separate Template Spectrograms'),'Color',[1.0 1.0 1.0]);

subplot(4,1,1);
plot(linspace(0,fraction,length),y,'Color',[0.0 0.0 0.0]);
xlabel('Time (sec)')
ylim([-1 1])

sp2=subplot(4,1,2);
imagesc([0 tMax],[0 fMax],spec);
colormap(sp2,pink);
xlabel('Time (sec)');
ylabel('Frequency');
set(gca,'YDir','normal');

subplot(4,1,3);
plot(linspace(0,fraction,length),y2,'Color',[0.0 0.0 0.0]);
xlabel('Time (sec)');
ylim([-1 1])

sp4=subplot(4,1,4);
imagesc([0 tMax],[0 fMax],spec2);
colormap(sp4,pink);
xlabel('Time (sec)');
ylabel('Frequency');
set(gca,'YDir','normal');
