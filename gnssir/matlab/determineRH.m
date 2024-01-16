%% Determine reflector height code
% Author: Max Feinland
% Date created: 11/15/23
% Last modified: 11/30/23
% Purpose: to adapt Kristine Larson's code and use a GNSS receiver to
% determine water level heights.

clc
clear
close all

load snrdata.mat

nextDay = find(snrFile(:,1) == 0);

t = snrFile(1:nextDay(1),1);
prn = snrFile(1:nextDay(1),2);
elevf = snrFile(1:nextDay(1),3);
azf = snrFile(1:nextDay(1),4);
sNR = snrFile(1:nextDay(1),5);

% housekeeping/quality control
az1 = 250;
az2 = 330;
elev1 = 5;
elev2 = 17;
ediff_threshold = 5;

% myprn = 5; % for debugging purposes, I will only look at one prn at a time
doy = datetime('01/01/2021', 'InputFormat', 'dd/MM/uuuu');

figure()
%% only look at one satellite
total_prns = unique(prn);
maxrhmax = [];
% for idx = 1:length(total_prns)
for idx = 1:length(total_prns)
indices_ofcurrentprn = find(prn == total_prns(idx));
myprn = total_prns(idx);

% assign variables to restrict only to that one satellite
current_t = t(indices_ofcurrentprn);
current_elev = elevf(indices_ofcurrentprn);
current_snr = sNR(indices_ofcurrentprn);
current_az = azf(indices_ofcurrentprn);

nanTs = isnan(current_t);
current_t(nanTs) = [];
current_elev(nanTs) = [];
current_snr(nanTs) = [];
current_az(nanTs) = [];
tdiff = diff(current_t);

% find all arcs for this satellite
separate_arcs = [1 find(tdiff > 20)' length(current_t)];
arcs = cell(length(separate_arcs)-1, 1);

% determine which arcs are okay
for k = 1:length(separate_arcs)-1
    arcs{k} = separate_arcs(k)+1:separate_arcs(k+1);
    current_arc_t = current_t(arcs{k});
    current_arc_elev = current_elev(arcs{k});
    current_arc_snr = current_snr(arcs{k});
    current_arc_az = current_az(arcs{k});

    sampleevery5seconds = 1:10:length(current_arc_t);
    current_arc_t = current_arc_t(sampleevery5seconds);
    current_arc_elev = current_arc_elev(sampleevery5seconds);
    current_arc_snr = current_arc_snr(sampleevery5seconds);
    current_arc_az = current_arc_az(sampleevery5seconds);

    p = polyfit(current_arc_t, current_arc_elev, 2);
    hifielev = current_arc_t.^2*p(1) + current_arc_t*p(2) + p(3); % polynomial approximation

    % remove discontinuities in the elevation angle
    notokidx = find(abs(hifielev - current_arc_elev) > 10);
    current_arc_elev(notokidx) = [];
    current_arc_snr(notokidx) = [];
    current_arc_t(notokidx) = [];
    current_arc_az(notokidx) = [];

    % find indices that meet the elevation & azimuthal masks
    ok_indices = find(current_arc_elev >= elev1 & current_arc_elev <= elev2 &  ...
        current_arc_az >= az1 & current_arc_az <= az2);
    ediff = range(current_arc_elev(ok_indices));

    conditions = [~isempty(ediff), ediff > ediff_threshold, ...
        length(unique(current_arc_elev)) > 5,  length(unique(current_snr)) > 5, ...
        length(current_arc_t) > 100];

    % figure()
    % subplot(2,1,1)
    % plot(current_arc_t, current_arc_snr)
    % title('SNR vs. time')
    % xlabel('Seconds of day'), ylabel('SNR (dB)')
    % 
    % subplot(2,1,2)
    % plot(current_arc_t, current_arc_elev)
    % title('Elevation vs. time')
    % xlabel('Seconds of day'), ylabel('Elevation (^{\circ})')

    if all(conditions)

        p = polyfit(current_arc_t, current_arc_elev, 2);
        hifielev = current_arc_t.^2*p(1) + current_arc_t*p(2) + p(3); % polynomial approximation
    
        % figure()
        % sgtitle(['PRN-', num2str(myprn), ' (USA-180) arc ', num2str(k)])
        % subplot(3,1,1)
        % plot(current_arc_t/3600, current_arc_elev, 'LineWidth', 1, ...
        %     'DisplayName', 'Reported Elevation Angle')
        % title('Elevation vs. time')
        % xlabel('Hours of day'), ylabel('Elevation (^{\circ})')
        % xlim([min(current_arc_t/3600) max(current_arc_t/3600)])
        % ylim([min(current_arc_elev) - 5, max(current_arc_elev)+5])
        % hold on
        % plot(current_arc_t/3600, hifielev, 'r--', 'LineWidth', 1, ...
        %     'DisplayName', 'Interpolated Elevation Angle')
        % legend()
        % 
        % subplot(3,1,2)
        % plot(current_arc_t/3600, current_arc_snr, 'LineWidth', 1)
        % title('SNR vs. time')
        % xlabel('Hours of day'), ylabel('SNR (dB)')
        % xlim([min(current_arc_t/3600) max(current_arc_t/3600)])
        % 
        % subplot(3,1,3)
        % plot(current_arc_t/3600, current_arc_az, 'LineWidth', 1)
        % title('Azimuthal angle vs. time')
        % xlabel('Hours of day'), ylabel('Azimuth (^{\circ})')
        % xlim([min(current_arc_t/3600) max(current_arc_t/3600)])
        % ylim([min(current_arc_az) - 10, max(current_arc_az)+10])

        current_arc_t = current_arc_t(ok_indices);
        current_arc_elev = current_arc_elev(ok_indices);
        current_arc_az = current_arc_az(ok_indices);
        current_arc_snr = current_arc_snr(ok_indices);

        p = polyfit(current_arc_t, current_arc_elev, 2);
        hifielev = current_arc_t.^2*p(1) + current_arc_t*p(2) + p(3); % polynomial approximation

        
        hits5 = find(hifielev >= 5); % index at which the elevation angle = 5
        threshold_index = find(hifielev >= 25);
        [ni, mi] = max(hifielev);
        if isempty(threshold_index) || mi < threshold_index(1)
            index = mi;
        else
            index = threshold_index(1);
        end
        
        firstarc = hits5(1):index; % from e = 5 to maximum or e = 25, whichever comes first
        
        sine = sind(hifielev(firstarc));
        linearsnr = 10.^(current_arc_snr(firstarc)/20);
        p1 = polyfit(sine, linearsnr, 2);
        linearsnr = linearsnr - sine.^2*p1(1) - sine*p1(2) - p1(3);

        % figure()
        % plot(sine, current_snr(firstarc))

        negsnr = find(linearsnr < -200);
        sine(negsnr) = [];
        linearsnr(negsnr) = [];
        
        % figure()
        % sgtitle(['RPR at Wesel: PRN-', num2str(myprn) ' Arc ' num2str(k)])
        % subplot(2,1,1)
        % plot(doy + seconds(current_arc_t), current_arc_snr, 'b-', 'LineWidth', 1)
        % xlabel('Time (UTC)'), ylabel('SNR (dB Hz)')
        % title('SNR vs time')
        % grid on
        % 
        % subplot(2,1,2)
        % plot(sine, linearsnr, 'r-', 'LineWidth', 1)
        % xlabel('sin(e)'), ylabel('SNR (v/v)')
        % title('SNR vs elevation angle')
        % grid on
        % 
        cf = 0.1902936/2; % true for all GPS signals using this receiver
        [sortedX, j] = sort(sine);
        
        % sort the data so all tracks are rising
        sortedY = linearsnr(j);
        
        % get the oversampling factor and hifac. see code for more information
        [ofac,hifac] = get_ofac_hifac(hifielev(firstarc), cf, 15, 0.005);
              
        % call the lomb scargle code.  Input data have been scaled so that 
        % f comes out in units of reflector heights    (meters)
        [f, p2] = lombscargle(sortedX/cf, sortedY,ofac,hifac);
        lambda = 3e+8/1575.42e+6;

        if myprn ~= 1 && myprn ~= 4 && myprn ~= 10 && myprn ~= 18 && ...
                myprn ~= 4 && myprn ~= 20 && myprn ~= 23 && myprn ~= 24 && ...
                myprn ~= 28 && myprn ~= 19
        dispname = ['PRN-' num2str(myprn) ', arc ' num2str(k)];
        plot(f,p2,'linewidth',2, 'DisplayName', dispname)
        xlim([0 15])
        xlabel('Reflector Height (m)'), ylabel('Amplitude')
        legend()
        hold on
        grid on
        frange = [0 5];
        [maxRH, maxRHAmp, pknoise] = peak2noise(f,p2,frange);
        title('Lomb-Scargle Periodogram')
        [nn, mm] = max(p2);
        maxrhmax(end+1) = f(mm);
        end
    end
end
end

%% need to make this one my own
function [ofac, hifac] = get_ofac_hifac( elevAngles, cf, maxH, desiredPrecision)
% function [ofac, hifac] = get_ofac_hifac(elevAngles,cf,maxH,desiredPrecision)
%
% Authors: Kristine M. Larson and Carolyn Roesler, March 10, 2018
%
% This function computes two factors - ofac and hifac - that are inputs to the
% Lomb-Scargle Periodogram code lomb.m. The ofac (oversampling factor) and
% hifac (high frequency factor) define the LSP frequency grid spacing 
% and maximum frequency.
% We follow the terminology and discussion from Press et al. (1992)
% in their LSP algorithm description.
%----------------------------------------------------------------------------
% INPUT
%    elevAngles:  vector of satellite elevation angles in degrees 
%    cf:      (L-band wavelength/2 ) in meters    
%    maxH:    maximum LSP grid frequency in meters
%               i.e. how far you want the reflector height to be estimated
%    desiredPrecision:  the LSP frequency grid spacing in meters
%              i.e. how precise you want he LSP reflector height
%                   to be estimated
% ---------------------------------------------------------------------------
% OUPUT
%             ofac: oversampling factor
%             hifac: high-frequency factor
%----------------------------------------------------------------------------
%
% For the GNSS_-IR application, we can write:  SNR = A.cos( 2.pi.H.X)
% The SNR data points are sampled with the variable
%       X= ( 2.sin(elevAngles)/ wavelength ), in units of inverse meters
%  so that their  spectral content H is expressed in meters.
%
% 
% The oversampling factor (ofac) defines the grid spacing between the
% frequencies H in order to find the top of the spectral peak to
% a desired precision. 
% For N data observed during a rectangular window of length:
%                  W  =  Xmax - Xmin
%  the frequency peaks have a characteristic width 1/W and we oversample 
%  each peak by (ofac) using a grid spacing of 1/(ofac.W) (in meters)
% 
% NB: don't be surprised if (ofac) is much larger than the typical
%          4-10 given in   the literature.
%
% The (hifac) factor defines the frequency grid maximum frequency Hmax, 
% relative to the averaged-Nyquist frequency (fc) i.e. the Nyquist
% frequency if all the N  data samples were evenly spaced over the 
% span W of the observing window : 
%                fc = N/(2*W) and  hifac = maxH/fc; 
%
% NB: don't be surprised if (hifac) is much less than the typical
%          5 >= given in the literature 
%
% NB: (fc) is only a reference frequency. For non-uniformly sampled data this 
% averaged-Nyquist frequency (fc) may  have  nothing to do with the real 
% pseudo- Nyquist or Nyquist-like frequency limit that exists in the data
%  ( see VanderPlas, 2017)
%-------------------------------------------------------------------------------

% SNR expressed as a function of X
    X= sind(elevAngles)/cf;    % in units of inverse meters

 % number of observations
    N = length( X);

% observing Window length (or span)
     W = max(X) - min(X);        % units of inverse meters

% characteristic peak width
    characteristic_peak_width= 1/W;            % in meters

% oversampling factor
     ofac = characteristic_peak_width/desiredPrecision;

% Nyquist frequency if the N observed data samples were evenly spaced
% over the observing window span W
    fc = N/(2*W);               % in meters 

% The high-frequency factor is defined relative to fc
    hifac = maxH/fc; 
end

function [f,P] = lombscargle(t,h,ofac,hifac)
% LOMB(T,H,OFAC,HIFAC) computes the Lomb normalized periodogram (spectral
% power as a function of frequency) of a sequence of N data points H,
% sampled at times T, which are not necessarily evenly spaced. T and H must
% be vectors of equal size. The routine will calculate the spectral power
% for an increasing sequence of frequencies (in reciprocal units of the
% time array T) up to HIFAC times the average Nyquist frequency, with an
% oversampling factor of OFAC (typically >= 4).
%
% The returned values are arrays of frequencies considered (f), and the
% associated spectral amplitude(P)

% Copyright (c) 2009, Dmitry Savransky 
% All rights reserved.


 
%sample length and time span
N = length(h);
T = max(t) - min(t);
 
%mean and variance
mu = mean(h);
s2 = var(h);
 
%calculate sampling frequencies
f = (1/(T*ofac):1/(T*ofac):hifac*N/(2*T)).';
 
%angular frequencies and constant offsets
w = 2*pi*f;
tau = atan2(sum(sin(2*w*t.'),2),sum(cos(2*w*t.'),2))./(2*w);
 
%spectral power
cterm = cos(w*t.' - repmat(w.*tau,1,length(t)));
sterm = sin(w*t.' - repmat(w.*tau,1,length(t)));
P = (sum(cterm*diag(h-mu),2).^2./sum(cterm.^2,2) + ...
   sum(sterm*diag(h-mu),2).^2./sum(sterm.^2,2))/(2*s2);
 
% amplitude
P= 2.*sqrt(s2*P/N); % amplitude
end

