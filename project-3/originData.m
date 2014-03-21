% R = originData(dataPath)
% Create R matrix
% Input:
%   dataPath: the path of u.data file
% Output:
%   R: matrix
%   containing user ratings with 
%   user on rows and movies on columns
%   943 users
%   1682 items
function R = originData(dataPath)
fid = fopen(dataPath);
if fid == -1
    disp('Cannot open the file');
    return;
else
    inputText = textscan(fid,'%d%d%d%d');

    % 100000 ratings
    % Put all the input data into 
    % a matrix (100000*3)
    % Column 1: user id
    % Column 2: item id
    % Column 3: rating
    originData = zeros(100000, 3);
    originData(:,1) = inputText{1};
    originData(:,2) = inputText{2};
    originData(:,3) = inputText{3};

    % Create the matrix R
    % containing user ratings with 
    % user on rows and movies on columns
    % 943 users
    % 1682 items
    R = zeros(943, 1682);
    for i = 1:100000
       oneEntry = originData(i,:);
       R(oneEntry(1),oneEntry(2)) = oneEntry(3);
    end
    fclose(fid)
    RMatFile = 'R.mat';
    save(RMatFile,'R');
end