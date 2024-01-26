function nmea2snr_clean
clc
clear
%% to get mat file
lines = readlines("WESL001021.txt");

startPat = "210101.log";

n = find(lines == startPat); % index of strings that start messages

snrFile = zeros(length(n)*13, 5); % Initialize the file
instances_counter = 1; % initialize number of instances

% populates snrFile matrix. Column 1 is time
for i = 1:length(n)
    if strcmpi(lines(n(i)+2), "[DEBUG] filename (battery): 210101.bat")
        gga_msg = lines(n(i)+3);
        gsv_msg = lines(n(i)+4); % first GSV message
    else
        gga_msg = lines(n(i)+2);
        gsv_msg = lines(n(i)+3); % first GSV message
    end
    gga_split = split(gga_msg, ","); % split up things between commas
    h = str2double(extractBetween(gga_split(2), 1, 2)); % hour
    m = str2double(extractBetween(gga_split(2), 3, 4)); % minute
    s = str2double(extractBetween(gga_split(2), 5, 6)); % second
    seconds_elapsed = 3600*h + 60*m + s;
    gsv_split = split(gsv_msg, ","); % split up things between commas
    number_of_messages = str2double(gsv_split(2)); % total GSV messages in this block
    lines_to_consider = n(i)+3:n(i)+3+number_of_messages-1;
    for j = lines_to_consider % loop through each of the messages
        currentmsg = split(lines(j), ",");
        sats_in_this_message = (numel(currentmsg)-4)/4; % how many sats in the GSV message? 1-4
        for k = 0:sats_in_this_message-1 % loop through them all
            f = 4*k; % each message contains 4 fields
            prn = str2double(currentmsg(5+f)); % pseudorandom number (identifier; useful for arcs)
            elev = str2double(currentmsg(6+f)); % elevation in degrees
            az = str2double(currentmsg(7+f)); % azimuth in degrees
            if k == 3
                snr_placehold = currentmsg(8+f);
                last_index_of_snr = strfind(snr_placehold, '*');
                snr = str2double(extractBetween(snr_placehold, 1, last_index_of_snr-1));
            else
                snr = str2double(currentmsg(8+f));
            end
            snrFile(instances_counter, :) = [seconds_elapsed prn elev az snr]; % populate this row of the matrix
            instances_counter = instances_counter+1; % increment instances-- need this cause you don't know
            % how many satellites will be in view for each message
        end
    end
end

snrFile = snrFile(1:instances_counter-1, :);
% save snrdata.mat snrFile
end