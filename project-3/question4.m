% Lauren Samy
% Question 4
% actual_predicted_results: cell array of 10 tests
function [avg_p, max_p, min_p, avg_r, max_r, min_r] = question4(actual_predicted_results)
    precisions = [];
    recalls = [];
    
    [rows, num_tests] = size(actual_predicted_results);
    
    for i = 1 : num_tests
        [precision, recall] = compute_precision_and_recall(actual_predicted_results{i});
        [length, width] = size(precisions);
        precisions(length + 1, 1) = precision;
        recalls(length + 1, 1) = recall;
    end
    
    avg_p = mean(precisions);
    max_p = max(precisions);
    min_p = min(precisions);
    
    avg_r = mean(recalls);
    max_r = max(recalls);
    min_r = min(recalls);
        
    