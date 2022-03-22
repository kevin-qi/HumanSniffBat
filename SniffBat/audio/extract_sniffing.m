[audio,Fs] = audioread('11702_29928/aligned_audio.wav');

noise_s = 1; % sec
noise_e = 6; % sec

sniff_s = 30; % sec
sniff_e = 35; % sec

%sniff_s = 60+18; % sec
%sniff_e = 60+23; % sec
sniff_s = 30; % sec
sniff_e = 30+120; % sec
y = audio;

figure;
tiledlayout(2,1)
nexttile
plot(y(sniff_s*Fs:sniff_e*Fs))
title('During sniffing')
set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', get(gca, 'XTick')/Fs)
xlim([0 Fs*(sniff_e-sniff_s)])
xlabel('seconds')
nexttile
plot(y(noise_s*Fs:noise_e*Fs))
title('During background noise (moving around, echolocating, flapping)')
set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', get(gca, 'XTick')/Fs) 
xlim([0 Fs*(noise_e-noise_s)])
xlabel('seconds')

y = decimate(audio, 10);
y = decimate(y, 5);
fs = Fs/50;
time_res = 3/1e3; % 10ms time resolution
freq_res = 1/time_res; % hz
window_size = round(fs*time_res); % hz
overlap_size = round(0.5*window_size);


figure;
tiledlayout(2,1)
nexttile
spectrogram(y(sniff_s*fs:sniff_e*fs), window_size, overlap_size, [], fs,'yaxis')
title('During sniffing')
set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', get(gca, 'XTick')/fs)
ylim()
nexttile
spectrogram(y(noise_s*fs:noise_e*fs), window_size, overlap_size, [], fs,'yaxis')
title('During background noise (moving around, echolocating, flapping)')
set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', get(gca, 'XTick')/fs) 

sniff_band = [150 650];
noise_band = [150, 900];
y_band = bandpass(y, sniff_band, fs);
y_noise = bandpass(y, noise_band, fs);
player = audioplayer(y_band(sniff_s*fs:sniff_e*fs)*3, fs);
%play(player);

player = audioplayer(y_noise(sniff_s*fs:sniff_e*fs)*3, fs);
%play(player);

player = audioplayer(y_band(noise_s*fs:noise_e*fs)*3, fs);
%play(player);

sniff_band_hilb = hilbert(y_band);
sniff_env = abs(sniff_band_hilb);

figure;
tiledlayout(2,1)
nexttile
plot(y_band(sniff_s*fs:sniff_e*fs))
hold on
plot(sniff_env(sniff_s*fs:sniff_e*fs))
title('During sniffing')
set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', get(gca, 'XTick')/fs)
xlim([0 fs*(sniff_e-sniff_s)])
xlabel('seconds')
nexttile
plot(y_band(noise_s*fs:noise_e*fs))
title('During background noise (moving around, echolocating, flapping)')
set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', get(gca, 'XTick')/fs) 
xlim([0 fs*(noise_e-noise_s)])
xlabel('seconds')


clear X
X(:,1) = y_band(sniff_s*fs:sniff_e*fs);
X(:,2) = y_noise(sniff_s*fs:sniff_e*fs);
sniff_band_hilb = hilbert(X(:,1));
sniff_env = abs(sniff_band_hilb);
%sniff_env = medfilt1(sniff_env, 3);
[pks, locs] = findpeaks(sniff_env, "MinPeakProminence",0.01, "MinPeakDistance",fs/20, "MaxPeakWidth",40, "WidthReference","halfheight","MinPeakHeight",0.02);
figure;
tiledlayout(2,1);
nexttile
support = linspace(0,length(X(:,1)),length(X(:,1)));
plot(support, sniff_env);
hold on
plot(support, X(:,1), support(locs), pks, 'pg')
nexttile
plot(X(:,2))

X_384hz = decimate(X(:,1),2);
fsds = fs/2;
for i = 2:length(locs)
    x0 = round(locs(i)/2);
    x1 = x0 - round(0.025*fsds/2);
    x2 = x0 + round(0.025*fsds/2);

    waveforms(i,:) = X_384hz(x1:x2)/max(X_384hz(x1:x2));
end


[idx, C] = kmeans(waveforms,2, 'Distance', 'sqeuclidean','Replicates',10);
figure;
tiledlayout('flow')
sniff_locs = [];
sniff_idx = [];
for i = 1:min(100, length(locs))
    nexttile
    colors = {'red', 'blue', 'black', 'green', 'cyan'};
    dist = norm(waveforms(i,:)-C(2,:));
    if(dist < 1.9)
        color = 'red';
        sniff_locs = [sniff_locs locs(i)];
        sniff_idx = [sniff_idx i]
    else
        color = 'blue';
    end
    plot(waveforms(i,:), 'Color', color)
    title(sprintf('%d', dist))
end

% Plot waveform
figure;
for i = 1:length(sniff_locs)
    pkLoc = sniff_s*fs + sniff_locs(i);
    plot(y_band(pkLoc-0.1*fs:pkLoc+0.1*fs), 'Color',[0 0 0 0.1]);
    hold on
end
xlim([0 fs*0.1*2])
xticks([0 384 384*2])
set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', 1000*get(gca, 'XTick')/fs - 100)
title('"Sniffing" waveform')
xlabel('time (ms)')
ylim([-0.2 0.2])

% Plot average spectrogram
time_res = 5/1e3; % 10ms time resolution
freq_res = 1/time_res; % hz
window_size = round(fs*time_res); % hz
overlap_size = round(0.5*window_size);

figure;
clear sgrams
for i = 1:length(sniff_locs)
    pkLoc = sniff_s*fs + sniff_locs(i);
    snippet = y_band(pkLoc-0.1*fs:pkLoc+0.1*fs);
    [S, f, t] = spectrogram(snippet, window_size, overlap_size, [], fs,'yaxis');
    sgrams(:,:,i) = abs(S);
    surf(t,f,abs(S),'EdgeColor','none'); 
    axis xy; axis tight; view(0,90);
    set(gca,'ColorScale','log')
end

figure;
surf(t,f,median(sgrams,3),'EdgeColor','none'); 
axis xy; axis tight; colormap("parula"); view(0,90);
set(gca,'ColorScale','linear')
set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', 1000*get(gca, 'XTick') - 100)
xlabel("time (ms)")
ylabel("frequency (hz)")
title('Average "Sniffing" spectrogram')
colorbar()

% Plot sniffing trace
sniff_band_hilb = hilbert(y_band);
sniff_env = abs(sniff_band_hilb);

figure;
tiledlayout(1,1);
nexttile;
plot(y_band(30*fs:35*fs))
hold on
plot(sniff_env(30*fs:35*fs))
xlim([0 fs*5])
xticks([0 fs 2*fs 3*fs 4*fs 5*fs])
set(gca, 'XTick',  get(gca, 'XTick'), 'XTickLabel', 1000*get(gca, 'XTick')/fs)
xlabel('Time (ms)')
title("Filtered audio 150hz to 650hz")

audiowrite("sniffing_snippet.wav",y_band(30*fs:35*fs), fs)

mixdata = prewhiten(X);
q = 2;
Mdl = rica(mixdata,q, 'Standardize', 0, 'VerbosityLevel', 1, 'Lambda', 1, 'IterationLimit',10000,'ContrastFcn','logcosh','NonGaussianityIndicator',ones(q,1)*1);
unmixed = transform(Mdl,mixdata);

figure
tiledlayout(q+1,1);
axs(1) = nexttile;
plot(mixdata(:,1));
for i = 1:q
    axs(i+1) = nexttile
    plot(unmixed(:,i));
    title(['Sound ',num2str(i)])
end
linkaxes(axs, 'xy')

player = audioplayer(unmixed(:,1),fs);
play(player)