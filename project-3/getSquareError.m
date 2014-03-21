% function [square_error] = getSquareError(R,W,U,V)
% Input:    four matrix R W U V
% Output:   the square error
function [square_error] = getSquareError(R,W,U,V)
tmp = R - U*V;
tmp = max(tmp, eps);
square_error = sum(sum(W.*(tmp.^2)));
clear tmp;
end