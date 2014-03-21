% Question 6
% Lauren Samy

function conv_R = convert_R(R)
    [users, items] = size(R);
    conv_R = zeros(users, items);
    
    for i = 1 : users
        for j = 1: items
            if R(i, j) > 0
                conv_R(i, j) = 1;
            end
        end
    end