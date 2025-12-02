clear all;
clc;
close all;

data_shitTime = readtable("longftimetest.csv");
data_longTime = readtable("LONGTIMELONGTIME2.csv");

angles_shitTime = data_shitTime.Angles;
angles_shitTime = rad2deg(angles_shitTime);

angles_longTime = data_longTime.Angles;
angles_longTime = rad2deg(angles_longTime);
pos_longTime = data_longTime.POS;
time_longtime = data_longTime.Times;
time_longtime = time_longtime - time_longtime(1);

time_shitTime = data_shitTime.Times;
time_shitTime = time_shitTime - time_shitTime(1);
pos_shitTime = data_shitTime.POS;

rawRSSI_shitTime = data_shitTime.RSSI;              % cell array med '(x, y, z, w)'
rawRSSI_longTime = data_longTime.RSSI;


[RSSI_shitTime, maxRSSI_shitTime] = parseRSSI(rawRSSI_shitTime);
[RSSI_longTime, maxRSSI_longTime] = parseRSSI(rawRSSI_longTime);

% 4 individuelle arrays
RSSI1 = RSSI_longTime(:,1);
RSSI2 = RSSI_longTime(:,2);
RSSI3 = RSSI_longTime(:,3);
RSSI4 = RSSI_longTime(:,4);




% 
% plot(pos_longTime, -time_longtime)
% xlabel('opfattelse af TARM vinkel, mhs.t \theta i azimuth i grader relativt til den selv', Interpreter='latex')
% ylabel('Tid i megasekunder')

histogram(pos_longTime, 100)
qqplot(pos_longTime)
 % scatter(pos_longTime, maxRSSI_longTime)
 % xlim([-180 180])

% scatter(angles_longTime - 45, RSSI1)
% hold on
% scatter(angles_longTime-15, RSSI2)
% scatter(angles_longTime+15, RSSI3)
% scatter(angles_longTime+45, RSSI4)


function [RSSI, maxRSSI] = parseRSSI(rawRSSI)
% rawRSSI: cell array eller string array med RSSI-strenge
% Returnerer:
%   RSSI     : Nx4 matrix
%   maxRSSI  : Nx1 vector
%   RSSIcols : struct med kolonnerne som individuelle arrays

    N = length(rawRSSI);
    RSSI = zeros(N,4);
    maxRSSI = zeros(N,1);

    for i = 1:N
        s = rawRSSI{i};
        
        % Fjern parenteser
        s = strrep(s, "(", "");
        s = strrep(s, ")", "");
        
        % Split og konverter
        nums = str2double(split(s, ","));
        
        RSSI(i,:) = nums';          % række i matrix
        maxRSSI(i) = max(nums);     % max værdi
    end
end
