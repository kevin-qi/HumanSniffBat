function [interp_trajectory] = HumanBat_interpolate_nans(trajectory)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here 

x = trajectory;
nanx = isnan(x);
t    = 1:numel(x);
x(nanx) = interp1(t(~nanx), x(~nanx), t(nanx));

x_movmed = movmedian(x,20);

interp_trajectory  = x_movmed;
end