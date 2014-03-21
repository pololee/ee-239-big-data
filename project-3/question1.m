% Question 1
% Input: k value
% Output: 
%	U: matrix
% 	V: matrix
%	square_error: scalar
function [U, V, square_error] = question1(k)
dataPath = './ml-100k/u.data';
R = originData(dataPath);
W = logical(R);

[U, V, numIter, tElapsed, finalResidual] = wnmfrule_2(R,W,k);
tmp = R - U*V;
tmp = max(tmp, eps);
square_error = sum(sum(W.*(tmp.^2)));
clear tmp;

uMatFile = strcat('Q1_U_', num2str(k),'.mat');
save(uMatFile,'U');
vMatFile = strcat('Q1_V_', num2str(k),'.mat');
save(vMatFile, 'V');
end