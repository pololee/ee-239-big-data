% This function constructs a new matrix from R with fraction % non-zero
% entries randomly removed
% Input:
%   R: original matrix
%   fraction: % of non-zero entries that need to be randomly removed
%             For example, fraction = 10 (mean 10%)
% Output:
%   removeR_matrix: A new matrix constructed from R with fraction % non-zero entries
%                   randomly removed
%   removeEntries: The cell array consists of entries that are removed

function [removeR_matrix,removedEntries] = randomRemove(R, fraction)
    % Step 1: generate a cell array where each element of the cell array is
    % of format [rating row col].
    %   - rating: non-zero value from matrix
    %   - row: row index of rating in matrix
    %   - col: col index of rating in matrix
    [nrows, ncols] = size(R);
    cell_array = {};
    k = 1;
    for i = 1:nrows
        for j=1:ncols
            if ne(R(i,j), 0)
                element = [R(i,j) i j];
                cell_array{k} = element;
                k = k+1;
            end
        end
    end
    
    % Step 2: create a random ordering of the numbers 1 to N and regenerate
    % step1 result from this new ordering.
    cell_array_length = length(cell_array);
    rand_index_vector = randperm(cell_array_length);
    random_ordering_cell_array = {};
    
    for i = 1:cell_array_length
        random_ordering_cell_array{i} = cell_array{rand_index_vector(i)};
    end
    
    % Step 3: Get random fraction % of non-zero entries from the list
    
    part_length = floor(cell_array_length * fraction / 100); %fraction should be equal to 10
    % each part cell is a list that has part_length element where each
    % element is of the form [rating row col]
    part = random_ordering_cell_array(1 : part_length);
    
    removedEntries = part;
    % Step 4: We generate a new matrix from the
    % the input R matrix. We set matrix element corresponding to
    % element in "part" cell array to 0.
    removeR_matrix = R;
    for j = 1:part_length
        part_element_row = part{j}(2);
        part_element_col = part{j}(3);
        removeR_matrix(part_element_row, part_element_col) = 0;
    end
end