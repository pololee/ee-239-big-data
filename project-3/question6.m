function [precision, rateM] = question6()
% [precision, rateM] = question6()
% input:
% output:
%   precision: average precision for L =5
%   rateM: 3 x num of Remove Entries
%       first row: L
%       second row: average hit rate
%       third row: average false alarm rate
dataPath = './ml-100k/u.data';
originR = originData(dataPath);
[removeR, removeEn] = randomRemove(originR, 10);

[U,V] = getUV(removeR,10,5);
save('Q6_U.mat','U');
save('Q6_V.mat','V');

% average precision for L = 5
top_five_movies = getLRecommendation(U, V, 5, removeEn);
precision = getPrecision(originR, top_five_movies);

% hit rate and false alarm rate
numRemove = size(removeEn,2);
rateM = zeros(3,numRemove);
rateM(1,:) = 1:numRemove;

for L = 1:1261
    topLmovies = getLRecommendation(U, V, L, removeEn);
    [hit, falseAlarm] = getHitAndFalseRate(originR, topLmovies);
    rateM(2,L) = hit;
    rateM(3,L) = falseAlarm;
    L
end

save('Q6_rate.mat','rateM');

% Plot the value points
% numPoints = 1000;
% interval = int16(numRemove/numPoints);
% idx = 1:interval:numRemove;
y = rateM(2,1:1261); % hit rate on y axis
x = rateM(3,1:1261); % false-alarm rate on x axis
f = figure();
scatter(x,y,'r*')
saveas(f,'Q6.png');
end