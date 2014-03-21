% Question 2
% Input: k value
% Output: 
%	U: matrix
% 	V: matrix
%	square_error: scalar
% set dataPath
% call originData_2
% call getUV_2
function [U, V, square_error] = question2(k)
dataPath = './ml-100k/u.data';
R = originData(dataPath);
W = R;
R = logical(W);

[U, V, numIter, tElapsed, finalResidual] = wnmfrule_2(R,W,k);
tmp = R - U*V;
tmp = max(tmp, eps);
square_error = sum(sum(W.*(tmp.^2)));
clear tmp;

uMatFile = strcat('Q2_U_', num2str(k),'.mat');
save(uMatFile,'U');
vMatFile = strcat('Q2_V_', num2str(k),'.mat');
save(vMatFile, 'V');
end