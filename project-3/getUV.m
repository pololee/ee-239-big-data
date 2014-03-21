% [U, V, finalResidual] = getUV(R, k)
% Input:
%   R: matrix you want to factorize
%   k: 
% Output:
%   U: matrix
%   V: matix
% In this function, we will construct a 0-1
% matrix for the input R matrix
function [U,V] = getUV(R,k,partOption)
if partOption == 1
    W = logical(R);
    [U, V, numIter, tElapsed, finalResidual] = wnmfrule_2(R,W,k);
elseif partOption == 2
    W = R;
    R = logical(W);
    [U, V, numIter, tElapsed, square_error] = wnmfrule_2(R,W,k);
elseif partOption == 5
    W = R;
    R = logical(W);
    lambda = 0.01;
    [U,V,tElapsed]=regWnmf(R,W,k,lambda);
else
    disp('unknown partOption');
end
if partOption == 1 || partOption == 2 || partOption == 5
    square_error = getSquareError(R,W,U,V);
    s=sprintf('square error: %0.4d',square_error);
    disp(s);
end
end