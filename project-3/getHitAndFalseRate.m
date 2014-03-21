function [hitRate, falseRate]=getHitAndFalseRate(originR, topLmovies)
% [hitRate, falseRate]=getHitAndFalseRate(originR, topLmovies)
% input:
%   originR: origin data R matrix
%   topLmovies: top L movies
% output:
%   hitRate: average hit rate of all the users
%   falseRate: average false alarm rate of all the users

numUsers = 943;
numMovies = 1682;
% numUsers = size(originR, 1);
% numMovies = size(originR, 2);
hitrateSum = 0;
falserateSum = 0;
for user = 1:numUsers
% each user
% first row: movie id
% second row: ratings
    eachUser = zeros(2,numMovies);
    eachUser(1,:) = 1:numMovies;
    eachUser(2,:) = originR(user,:);
    likeidx = find(eachUser(2,:)>=4);
    myLiked = eachUser(1,likeidx);
    likeSize = size(myLiked,2);
    lessThanThree = find(eachUser(2,:)<=3);
    largerThanZero = find(eachUser(2,:)>0);
    dislikeidx = intersect(lessThanThree,largerThanZero);
    myDisliked = eachUser(1,dislikeidx);
    dislikeSize = size(myDisliked,2);
    likeInterSize = size(intersect(topLmovies,myLiked),2);
    dislikeInterSize = size(intersect(topLmovies,myDisliked),2);
    if likeInterSize ~= 0
        hitrateSum = hitrateSum + likeInterSize/likeSize;
    end
    if dislikeInterSize ~=0
        falserateSum = falserateSum + dislikeInterSize/dislikeSize;
    end
end
hitRate = hitrateSum/numUsers;
falseRate = falserateSum/numUsers;
end