function nmea2snr

%% to get mat file
lines = readlines("WESL001021.txt");

startPat = "210101.log";

n = find(lines == startPat); % index of strings that start messages

snrFile = zeros(length(n)*13, 5);
gpsmsg1 = strings(length(n), 1);
instances_counter = 1;

% populates snrFile matrix. Column 1 is time
for i = 1:length(n)
    gpsmsg1(i) = lines(n(i)+2);
    gpsmsg2 = lines(n(i)+3); % first GSV message
    h = str2double(extractBetween(gpsmsg1(i), 8, 9));
    m = str2double(extractBetween(gpsmsg1(i), 10, 11));
    s = str2double(extractBetween(gpsmsg1(i), 12, 13));
    tvec = 3600*h + 60*m + s;
    number_of_messages = str2double(extractBetween(gpsmsg2, 8, 8))-1;
    lines_to_consider = n(i)+3:n(i)+3+number_of_messages;
    for j = lines_to_consider
        currentmsg = lines(j);
        if strlength(currentmsg) > 27
            numMessages = floor((strlength(currentmsg)-17)/14);
            for k = 0:numMessages-1
                f = 15*k;
                prn = str2double(extractBetween(currentmsg, 15+f, 16+f));
                elev = str2double(extractBetween(currentmsg, 18+f, 19+f)); % degrees
                az = str2double(extractBetween(currentmsg, 21+f, 23+f)); % degrees
                snr = str2double(extractBetween(currentmsg, 25+f, 28+f)); % dB
                snrFile(instances_counter, :) = [tvec prn elev az snr];
                instances_counter = instances_counter+1;
            end
        end
    end
end

snrFile = snrFile(1:instances_counter-1, :);
save snrdata.mat snrFile
end