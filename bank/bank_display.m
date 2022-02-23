clc
clear

data = readmatrix('history.csv');
figure()
hold on
lgd = {};
t = 0;
for i=2:size(data, 2)
    if sum(data(2:end, i)) ~= 0
        t = t + 1;
        plot(data(2:end, i))
        lgd{t} = strcat('userid: ', num2str(data(1, i), '%d'));
    end
end

% ylim([500, 700])
% legend(lgd)
