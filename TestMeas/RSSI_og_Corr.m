

clear all;
clc;
close all;

c = fopen('Correlation.bin', 'rb');
Correlation = fread(c, Inf, 'float');

r = fopen('RSSI.bin', 'rb');
RSSI = fread(r, Inf, 'float');


Fs = 250e3;
N = length(RSSI);
t = (0:N-1)' / Fs;
N2 = length(Correlation);
t2 = (0:N2-1)' / Fs;
t_us    = t * 1e6;  
t_us2 = t2*1e6;
% t_ms    = t * 1e3; 

figure;

% Hovedplot
plot(t, RSSI)
hold on
plot(t2, Correlation)
xlim([1.04742 1.18698])
legend('RSSI', 'Correlation')
xlabel('Time [s]', 'Interpreter','latex')
ylabel('RSSI and Correlation value', Interpreter='latex')
rectangle('Position', [1.1706, -1, (1.17391-1.1706), (1+0.6)], ...
          'EdgeColor', 'k', 'LineStyle', '--', 'LineWidth', 1.2);

% Zoom-indholdet
axInset = axes('Position',[0.64 0.55 0.22 0.22]);

plot(t, RSSI)
hold on
plot(t2, Correlation)
xlim([1.1706 1.17391])     % Det område du vil zoome ind på
title('Zoom')
%xlabel(axInset, 'time [us]', Interpreter='latex')
set(axInset, 'Box','on')