% This function predicts the ratings for removeEntries using U, V matrixes
% obtained from ALS. Then, it sorts the ratings and returns the top L
% UNIQUE movie IDs based on the ratings.
%
% Input:
%   U: U matrix obtained from running ALS
%   V: V matrix obtained from running ALS
%   L: Top number of movies we want to obtain as recommendation set
%   removeEntries: cell array of testing data. Each element is of the form
%                  [actual_rating row col]
%
% Output:
%   recommandationSet: vector of top L movie IDs

function recommendationSet = getLRecommendation(U, V, L, removeEntries)
    recommendationSet = [];

    % Step 1: Use U and V to predict the rating for all entries in
    % removeEntries and store the predicted rating into
    % rating_movie_matrix where each row is of the form [predicted_rating
    % movie_id]
    rating_movie_matrix = []; % matrix where each row is: [predicted_rating movie_id]
    
    for i = 1:length(removeEntries)
        %actual_rating = removeEntries{i}(1);
        unknown_row = removeEntries{i}(2);
        unknown_col = removeEntries{i}(3); % this is the movie_id
        U_row = U(unknown_row,:);
        V_col = V(:,unknown_col);
        predicted_rating = dot(U_row,V_col); % dot product
        
        pair = [predicted_rating unknown_col];
        rating_movie_matrix = [rating_movie_matrix; pair]; % append a row into the matrix
       
        %display(actual_rating);
        %display(predicted_rating);
    end
    
    % Step 2: Sort the matrix based on the first column (predicted rating
    % value) using sortRows function. The result is in
    % ascending order from top to bottom. To get the descending order, we
    % call flipdim after sortrows
    sorted_rating_matrix = sortrows(rating_movie_matrix, 1);
    % using flipDim to obtain the descending order of rating from top to
    % bottom
    sorted_rating_matrix = flipdim(sorted_rating_matrix, 1);
    
    % Step 3: Iterate from top row to bottom row. Extract the top L movies
    % from top to bottom given that all the movies must be unique.
    [nrows, ncols] = size(sorted_rating_matrix);
    k = 1;
    for i = 1:nrows
        movie_id = sorted_rating_matrix(i,2); % second column is movie_id
        recommendation_set_length = length(recommendationSet);
        j = 1;
        while (j <= recommendation_set_length)
            % check to see if movie_id already belongs to the
            % recommendationSet
            if eq(movie_id, recommendationSet(j))
                break; 
            end
            j = j+1;
        end
        
        if eq(recommendation_set_length,0) || eq(j,recommendation_set_length+1)
            recommendationSet(k) = movie_id;
            k = k+1;
            if k > L
                break;
            end
        end
    end
end
