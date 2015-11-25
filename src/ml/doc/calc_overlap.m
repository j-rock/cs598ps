%---------------------
% Author: Evan Bowling
% Class:  CS598PS
% Sem:    Fall 2015
% Assgn:  Homework 1
%---------------------

function [padded_length,num_steps] = calc_overlap(L, ww,overlap)
% DESCRIPTION: calculate the overlap stats for performing windowing
% functions on 1-D inputs.
%
% INPUT:
% L: the length of the input data to process
% ww: the window width to use on the input data
% overlap: the percentage of overlap for each window
%
% OUTPUT:
% padded_length: the final length
% num_steps: the number of steps that will be used

assert(L>0,'calc_overlap: L needs to be greater than 0 ');
assert(ww>0,'calc_overlap: ww needs to be greater than 0 ');
assert(overlap>=0,'calc_overlap: overlap needs to be in range [0,1) ');
assert(overlap<1,'calc_overlap: overlap needs to be in range [0,1) ');

% current limitations (only supports 0.25, or 0.5)
assert(or(overlap==0,or(overlap==0.25,overlap==0.5)),'calc_overlap: overlap needs to be in range [0,1) ');

% support the edge case - length is less than window
if L < ww
    padded_length = ww;
    num_steps = 1;
    return;
end

curr=ww;
num_steps = 1;
while curr < L
    step = (1 - overlap) * ww;
    curr=curr+step;
    num_steps=num_steps+1;
end
padded_length = curr;
