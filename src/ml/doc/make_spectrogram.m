%---------------------
% Author: Evan Bowling
% Class:  CS598PS
% Sem:    Fall 2015
% Assgn:  Homework 1
%---------------------

function [result,fMax,tMax] = make_spectrogram(data, window_size,Fs, overlap)
% DESCRIPTION: construct a spectrogram from the input data given the specified
% window size (non-overlapping windows).
%
% INPUT:
% data: input data to perform fft on
% window_size: the window size to perform each fft on
% Fs: the sampling frequency of the input audio (meant to be extracted via "audioread" cmd)
%     meant to be in Hz
% overlap: the percentage of overlap for each window
%
% OUTPUT:
% result: 2D matrix that can be visualized with imagesc


% ASIDE:
%  Visualize the Fourier Transform matrix with:
%  This displays the real part:           imshow(real(dftmtx(64)))
%  This displays the complex part:        imshow(conj(dftmtx(64)))

overlap=0;

% check to make sure the input is 1d (n rows x 1 col)
ndims = size(size(data),2);
if or(ndims ~= 2, size(data,2) ~= 1)
    disp('make_spectrogram - data arg is invalid');
end
if or(window_size < 0, isinteger(window_size) ~= 0)
    disp('make_spectrogram - window_size is invalid');
end
if size(data,1) < window_size
    disp('Warning: data input is smaller than specified window size');
end

rows=size(data,1);
cols=size(data,2);

% pad the end of the data input to accomodate windows size
[padded_length,num_windows] = calc_overlap(rows, window_size,overlap);
if padded_length > rows
    data((rows+1):padded_length)=0;
end

% identify the max frequency that can be obtained from fft analysis (half
% the sampling frequency)
fMax = round(Fs / 2);

% identify the time length (in seconds) of the data input
tMax = size(data,1) / Fs;
disp(sprintf('num_windows: %d, fMax: %d, tMax: %d',num_windows,fMax,tMax));


result=zeros((window_size/2),num_windows);
curr=1;
steps=1;
while curr < rows
    step = (1 - overlap) * window_size;
    w_end = curr+window_size-1;

    % abs - Absolute value and complex magnitude
    % arg - Argument (polar angle) of a complex number

    if w_end > size(data,1)
        break;
    end

    % multiply the DFT matrix by the input signal
    %res = fft(data(w_start:w_end));
    res=abs(dftmtx(window_size)*data(curr:w_end));

    % debug line to check overlap values
    %disp(sprintf('wi:%d  w_start:%d w_end: %d',wi,w_start,w_end));

    % % for real-valued input, only half the results are valid
    % % the values simply repeat after the middle
    result(1:(window_size/2),steps)=res(1:(window_size/2));
    
    % %DEBUG: use the whole window_size
    %result(1:(window_size),steps)=res(1:(window_size));

    curr=curr+step;
    steps=steps+1;
end
