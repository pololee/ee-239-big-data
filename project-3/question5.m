% Question 5
% Input: 
%   k value
%   lambda value
% Output: 
%	U: matrix
% 	V: matrix
%	square_error: scalar
% set dataPath
% call originData_2
% call getUV_2
function [U, V, square_error] = question5(k,lambda)
dataPath = './ml-100k/u.data';
R = originData(dataPath);
W = R;
R = logical(W);
[U,V,tElapsed]=regWnmf(R,W,k,lambda);
    
tmp = R - U*V;
tmp = max(tmp, eps);
square_error = sum(sum(W.*(tmp.^2)));
clear tmp;

uMatFile = strcat('Q5_U_', num2str(k),'_');
uMatFile = strcat(uMatFile, strrep(num2str(lambda),'.',''));
uMatFile = strcat(uMatFile, '.mat');
save(uMatFile,'U');
vMatFile = strcat('Q5_V_', num2str(k),'_');
vMatFile = strcat(vMatFile, strrep(num2str(lambda),'.',''));
vMatFile = strcat(vMatFile, '.mat');
save(vMatFile, 'V');

% uFile = strcat('U_', num2str(k),'_');
% uFile = strcat(uFile, strrep(num2str(lambda),'.',''));
% uFile = strcat(uFile, '.txt');
% dlmwrite(uFile, U, 'precision', 4, 'delimiter', '\t');
% vFile = strcat('V_', num2str(k),'_');
% vFile = strcat(vFile, strrep(num2str(lambda),'.',''));
% vFile = strcat(vFile, '.mat');
% dlmwrite(vFile, V, 'precision', 4, 'delimiter', '\t');
end