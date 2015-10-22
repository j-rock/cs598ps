function [ y ] = lowp_smooth( x, Fs, k)
    %% Thank you, https://en.wikipedia.org/wiki/Low-pass_filter#Discrete-time_realization
    N = length(x);
    y = zeros(1,N);
    dt = 1 / Fs;
    alpha = dt / (k + dt);
    for i = 2:N
        y(i) = y(i-1) * (1-alpha) + x(i) * alpha;
    end
end

