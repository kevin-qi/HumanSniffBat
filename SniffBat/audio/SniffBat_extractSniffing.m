function [sniffing_timestamps_ms] = SniffBat_extractSniffing(processedAudioDir, micChannels)
%HumanBat_extractSniffing Extract the timestamp of each "sniff"
%   processedAudioDir : Directory containing concatenated audio .mat
%   files (1 for each audio channel)
%
%   micChannels : array of channels (between 1 and 6) to use. 
%   E.g. [2 3 4 5 6]
%
%   audio struct: 
%       audio.audio:
%           audio containing sniffing sounds
%           (n_channels, n_samples)
%       audio.fs:
%           sampling rate of audio
%
%

% Decimate audio by factor of 100

for i = 1:length(micChannels)
    ch = micChannels(i);
    audioData = load(fullfile(processedAudioDir, sprintf('audioCh_%d.mat',ch)));
    audio(:,i) = audioData.audioData;
    fs = audioData.fs;
end
disp(size(audio))


time_res = 10/1e3; % 10ms time resolution
freq_res = 1/time_res; % hz
window_size = round(fs*time_res); % hz
overlap_size = round(0.5*window_size);

figure;
tiledlayout(length(micChannels),1)
for i = 1:length(micChannels)
    nexttile
    spectrogram(audio(:,i), window_size, overlap_size, [], fs,'yaxis')
    title(sprintf('Channel %d', micChannels(i)))
    %set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', get(gca, 'XTick')/fs)
end

sniff_band_freq = [150 450];
sniff_band = bandpass(audio, sniff_band_freq, fs);

figure;
tiledlayout(length(micChannels),1)
for i = 1:length(micChannels)
    axs(i) = nexttile
    plot(sniff_band(30*fs:35*fs,i))
    title(sprintf('Channel %d', micChannels(i)))
    %set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', get(gca, 'XTick')/fs)
end
linkaxes(axs,'xy');

sniff_band_hilb = hilbert(audio);
sniff_env = abs(sniff_band_hilb);
figure;
tiledlayout(length(micChannels),1)
for i = 1:length(micChannels)
    nexttile
    support = linspace(0,length(audio(:,i)),length(audio(:,i)));
    plot(support, sniff_env(:,i));
    hold on
    [pks, locs] = findpeaks(medfilt1(sniff_env(:,i), 15), "MinPeakProminence",0.01, "MinPeakDistance",fs/20, "MaxPeakWidth",40, "WidthReference","halfheight","MinPeakHeight",0.02);
    plot(support, audio(:,i), support(locs), pks, 'pg')
    title(sprintf('Channel %d', micChannels(i)))
end

[pks, locs] = findpeaks(medfilt1(sniff_env(:,1), 15), "MinPeakProminence",0.01, "MinPeakDistance",fs/20, "MaxPeakWidth",40, "WidthReference","halfheight","MinPeakHeight",0.02);
    

for i = 1:length(micChannels)
    audio_ds(:,i) = decimate(audio(:,i),2);
end
fsds = fs/2;
figure;
for i = 2:length(locs)
    if(locs(i)<33600 & locs(i) > 28800)
    x0 = round(locs(i)/2);
    x1 = x0 - round(0.02*fsds); % 20ms before
    x2 = x0 + round(0.02*fsds); % 20ms after

     wf = audio_ds(x1:x2,:)./max(abs(audio_ds(x1:x2,:)));
     wf = reshape(wf, 1, []);
     plot(audio_ds(x1:x2,:))
     title(i)
     pause(1)
     waveforms(i-1,:) = wf;
    end
end

% Plot a few waveforms at random
num_examples = 25;
examples = datasample(waveforms, num_examples ,1);
figure;
tiledlayout('flow')
for i = 1:num_examples
    axs(i) = nexttile;
    plot(examples(i,:))
end
linkaxes(axs, 'xy');

figure;
tiledlayout('flow')
for i = 1:num_examples
    axs(i) = nexttile;
    plot(examples(i,1:39))
end
linkaxes(axs, 'xy');

[idx, C] = kmeans(waveforms,2, 'Distance', 'sqeuclidean','Replicates',10);
figure;
tiledlayout('flow')
sniffs = []
for i = 1:min(100, length(locs))
    nexttile
    colors = {'red', 'blue', 'black', 'green', 'cyan'};
    dist = norm(waveforms(i,:)-C(1,:));
    if(dist < 1.9)
        color = 'red';
        sniffs = [sniffs locs(i)];
    else
        color = 'blue';
    end
    plot(waveforms(i,1:26), 'Color', color)
    title(sprintf('%d', dist))
end


%mixdata = prewhiten(audio);
%q = 2;
%Mdl = rica(mixdata,q, 'Standardize', 0, 'VerbosityLevel', 1, 'Lambda', 1, 'IterationLimit',10000,'ContrastFcn','logcosh','NonGaussianityIndicator',ones(q,1)*1);
%unmixed = transform(Mdl,mixdata);

%figure
%tiledlayout(q+1,1);
%axs(1) = nexttile;
%plot(mixdata(:,1));
%for i = 1:q
%    axs(i+1) = nexttile
%    plot(unmixed(:,i));
%    title(['Sound ',num2str(i)])
%end
%linkaxes(axs, 'xy')

end