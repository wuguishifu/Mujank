clc
clear

data = readmatrix('history.csv');
time = readtable('history.csv').Var1;
time = datetime(time, 'InputFormat', 'MM_dd_uuuu HH_mm_ss');

id = [280451832675827712];

figure()
hold on
for i=2:size(data, 2)
    if ismember(data(1, i), id)
        var = i;
        plot(time(2:end), data(2:end, i))
    end
end
xlabel('Date')
ylabel('Balance (Jankcoins)')

t = days(time(2:end) - time(2));
fit = polyfit(t, data(2:end, var), 1);
regY = polyval(fit, t([1, end]));
plot(time([2, end]), regY)

legend('Wendy', 'Forecast')
