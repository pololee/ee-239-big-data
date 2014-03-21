% Lauren Samy
% Question 4
% test_x: cell array of predicted_actual pairs for a single test.

function [precision, recall] = compute_precision_and_recall(test_x)
    num_predicted_likes = 0;
    num_actual_likes = 0;
    precision = 0;
    recall = 0;
	actual_values = [];
	predicted_values = [];
    
    %get dimensions of matrix B
    [rows, num_pairs] = size(test_x);
    
	for i = 1 : num_pairs
	    [rows, columns] = size(actual_values);
		actual_values(rows + 1, 1) = test_x{i}{1};
		predicted_values(rows + 1, 1) = test_x{i}{2};
	end

    %get values that are > =4, mark position
    for i = 1 : rows
        if predicted_values(i) >= 4
            num_predicted_likes = num_predicted_likes + 1;
            %if actual rating for the same position is also a like 
            if actual_values(i) >= 4
                num_actual_likes = num_actual_likes + 1;
            end
        end
    end
    
    if(num_predicted_likes > 0)
        %calculate precision
        precision = num_actual_likes / num_predicted_likes;
    else
        S = sprintf('None of the predicted ratings was a like');
        disp(S)
    end
    
    num_actual_likes = 0;
    num_predicted_likes = 0;
    
    for i = 1 : rows
        if actual_values(i) >= 4
            num_actual_likes = num_actual_likes + 1;
            %if actual rating for the same position is also a like 
            if predicted_values(i) >= 4
                num_predicted_likes = num_predicted_likes + 1;
            end
        end
    end
   
    if(num_actual_likes > 0)
        %calculate recall
        recall = num_predicted_likes / num_actual_likes;
    else
        S = sprintf('None of the actual ratings was a like');
        disp(S)
    end