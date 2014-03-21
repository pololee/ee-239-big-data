function precision = getPrecision(originR, topLmovies)
% precision = getPrecision(originR, topLmovies)
% input:
%   originR: origin data R matrix
%   topLmovies: top L movies (recommendation set)
% output:
%   precision: average precision of all the users
L = size(topLmovies, 2);
% numUsers = size(originR, 1);
% numMovies = size(originR, 2);
numUsers = 943;
numMovies = 1682;
% eachUser
% first column: ratings
% second column: movie-Id
precisionSum = double(0);
for user = 1:numUsers
    eachUser = zeros(numMovies, 2);
    eachUser(:,2) = 1:numMovies;
    eachUser(:,1) = originR(user,:);
    eachUser = sortrows(eachUser,1);
    myTopLmovies = eachUser(numMovies-L+1:numMovies,2);
    intersecSize = size(intersect(topLmovies,myTopLmovies),2);
    if intersecSize ~= 0
        precisionSum = precisionSum + double(intersecSize/L);
    end
end
precision = precisionSum/numUsers;
end