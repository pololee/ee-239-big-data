% dataPath = 'C:\Users\tuanle.tuanle-PC\Dropbox\ee239as-proj\proj3-not-share\ml-100k\u.data'
% a=[1,0,2,3,4,7,3;9,7,0,0,10,1,2;5,6,7,8,9,5,4;4,0,6,2,7,9,5]

% [actual_predicted_results, ave_error_for_each_test_cell_array, ave_error_among_10_tests, lowest_error_value, highest_error_value] = question3(partOption)
% Test the recommendation system
% Input:
%   matrix obtained from calling originData(dataPath)
% Output:
%   actual_predicted_results: cell array X of 10 elements corresponding to
%       10 tests. Each element of X is another cell array contains {actual, predicted} pair.
%       Example: first_test_result = actual_predicted_results{1}
%                %length of first_test_result equal to the size of each test part
%                first_pair_of_first_test_result = first_test_result{i}
%                first_pair_actual = first_pair_of_first_test_result{1}
%                first_pair_predicted = first_pair_of_first_test_result{2}
%
%   ave_error_for_each_cell_array: cell array of 10 elements. Each element
%       is the averrage error for each test
%
%   ave_error_among_10_test: average error over all 10 tests
%
%   lowest_error_value: lowest average error among 10 tests
%
%   highest_error_value: highest average error among 10 tests

function [actual_predicted_results, ave_error_for_each_test_cell_array, ave_error_among_10_tests, lowest_error_value, highest_error_value] = question3(partOption)
    dataPath = './ml-100k/u.data';
    matrix = originData(dataPath);
    num_tests = 10;
    actual_predicted_results = {};
    
    % Step 1: generate a cell array where each element of the cell array is
    % of format [rating row col].
    %   - rating: non-zero value from matrix
    %   - row: row index of rating in matrix
    %   - col: col index of rating in matrix
    [nrows, ncols] = size(matrix);
    cell_array = {};
    k = 1;
    for i = 1:nrows
        for j=1:ncols
            if ne(matrix(i,j), 0)
                element = [matrix(i,j) i j];
                cell_array{k} = element;
                k = k+1;
            end
        end
    end
    
    disp('Step 1 done!')
    
    % Step 2: create a random ordering of the numbers 1 to N and regenerate
    % step1 result from this new ordering.
    cell_array_length = length(cell_array);
    rand_index_vector = randperm(cell_array_length);
    random_ordering_cell_array = {};
    
    for i = 1:cell_array_length
        random_ordering_cell_array{i} = cell_array{rand_index_vector(i)};
    end
    
    disp('Step 2 done!')
    
    % Step 3: Split the random_ordering_cell_array into 10 parts
    part_length = floor(cell_array_length / num_tests);
    % each part cell is a list that has part_length element where each
    % element if of the form [rating row col]
    
    ave_error_for_each_test_cell_array = {}; % each element will be an average error per test/part
    
    start_index = 1;
    for i = 1:num_tests % TODO: change this to 10
        actual_predicted_array_per_part = {};
        
        end_index = start_index + part_length - 1;
        % Note: end_index is never out of range since part_length is a
        % floor of cell_array_length/10
        part = random_ordering_cell_array(start_index : end_index);
        start_index = start_index + part_length;
    
        % Step 4: For each of the 10 parts, we generate a new matrix from the
        % original input matrix. We set matrix element corresponding to
        % element in each part to 0.
        part_matrix = matrix;
        for j = 1:part_length
            part_element_row = part{j}(2);
            part_element_col = part{j}(3);
            part_matrix(part_element_row, part_element_col) = 0;
        end
        
        disp('Step 4 done!')
        
        % Step 5: For each part, train the model and predict unknown rating
        [U, V] = getUV(part_matrix, 10, partOption); % Use a weight matrix containing 0s and 1s. Use k=10
        error_sum_per_part = 0;
        
        for j = 1:part_length
           R_actual = part{j}(1);
           unknown_row = part{j}(2);
           unknown_col = part{j}(3);
           U_row = U(unknown_row,:);
           V_col = V(:,unknown_col);
           R_predicted = dot(U_row,V_col); % dot product
           prediction_error = abs(R_predicted - R_actual);
           error_sum_per_part = error_sum_per_part + prediction_error;
           
           actual_predicted_pair = {R_actual,R_predicted};
           actual_predicted_array_per_part{j} = actual_predicted_pair;
        end
        
        disp('Step 5 done!')
        
        % Input to question 4
        actual_predicted_results{i} = actual_predicted_array_per_part;
        
        average_error_for_this_part = error_sum_per_part / part_length;
        ave_error_for_each_test_cell_array{i} = average_error_for_this_part;
    end
    
    % Step 6: Average among 10 tests
    %         Find the highest and lowest values of average error among 10
    %         tests
    sum_error_10_tests = 0;
    highest_error_value = 0;
    lowest_error_value = ave_error_for_each_test_cell_array{1};
    for i=1:num_tests
        sum_error_10_tests = sum_error_10_tests + ave_error_for_each_test_cell_array{i};
        if ave_error_for_each_test_cell_array{i} > highest_error_value
            highest_error_value = ave_error_for_each_test_cell_array{i};
        end
        if ave_error_for_each_test_cell_array{i} < lowest_error_value
            lowest_error_value = ave_error_for_each_test_cell_array{i};
        end
    end
    ave_error_among_10_tests = sum_error_10_tests / num_tests;
    
    disp('Step 6 done!')
    
end