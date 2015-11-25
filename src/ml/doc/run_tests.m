%---------------------
% Author: Evan Bowling
% Class:  CS598PS
% Sem:    Fall 2015
% Assgn:  Homework 1
%---------------------

% Purpose: TDD support for matlab functions related to hw.

% Test "calc_overlap" with window larger that input
[padded_length,num_steps]=calc_overlap(32,64,0);
assert(padded_length==64,'calc_overlap: invalid result');
assert(num_steps==1,'calc_overlap: invalid result');


% Test "calc_overlap" with simple 0 percent overlaps
[padded_length,num_steps]=calc_overlap(128,64,0);
assert(padded_length==128,'calc_overlap: invalid result');
assert(num_steps==2,'calc_overlap: invalid result');


[padded_length,num_steps]=calc_overlap(110,64,0);
assert(padded_length==128,'calc_overlap: invalid result');
assert(num_steps==2,'calc_overlap: invalid result');

% Test "calc_overlap" with other overlaps
[padded_length,num_steps]=calc_overlap(128,64,0.50);
assert(padded_length==128,'calc_overlap: invalid result');
assert(num_steps==3,'calc_overlap: invalid result');


[padded_length,num_steps]=calc_overlap(128,64,0.25);
assert(padded_length==160,'calc_overlap: invalid result');
assert(num_steps==3,'calc_overlap: invalid result');


% Test "calc_overlap" with simple 0 percent overlaps
[padded_length,num_steps]=calc_overlap(128,64,0);
assert(padded_length==128,'calc_overlap: invalid result');
assert(num_steps==2,'calc_overlap: invalid result');
