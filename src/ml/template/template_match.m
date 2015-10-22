function [ smoothed ] = template_match(template, audio, Fs, smooth_k)
  %% Smooth_k should be something small like 0.1

  matches = conv(template, audio);
  smoothed = lowp_smooth(convd .^ 4, Fs, smooth_k);
end
