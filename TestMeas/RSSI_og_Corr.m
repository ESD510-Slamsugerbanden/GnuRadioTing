

clear all;
clc;
close all;

c = fopen('Correlation.bin', 'rb');
Correlation = fread(c, Inf, 'float');

r = fopen('RSSI.bin', 'rb');
RSSI = fread(r, Inf, 'float');


figure;

% Hovedplot
plot(RSSI)
hold on
plot(Correlation)
xlim([98e3 132e3])
legend('RSSI', 'Correlation')
rectangle('Position', [119.9e3, -1, (121e3-119.9e3), (1+0.6)], ...
          'EdgeColor', 'k', 'LineStyle', '--', 'LineWidth', 1.2);

% Zoom-indholdet
axInset = axes('Position',[0.5 0.55 0.25 0.25]);

plot(RSSI)
hold on
plot(Correlation)
xlim([119.9e3 121e3])     % Det område du vil zoome ind på
title('Zoom')
set(axInset, 'Box','on')