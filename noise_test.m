[pxx_on_shield, f_on_shield] = check_ephys_noise('../data/raw/b151/noise_test_lights_on_top_bottom_single_shield_grounded/ephys/logger_13', false);
[pxx_on, f_on] = check_ephys_noise('../data/raw/b151/noise_test_211101_lights_on/ephys/logger_13', false);
[pxx_off, f_off] = check_ephys_noise('../data/raw/b151/noise_test_211101_lights_off/ephys/logger_13', false);

fm = 600; % Max freq to plot

figure;
tiledlayout(3,1);

ax1= nexttile;
plot(f_off(1:fm/2), 10*log10(pxx_off(1:fm/2)));
title('NIR Lights Off');
xlabel('Frequency (Hz)');
ylabel('Power (dB/Hz)');
xticks([60 120 180 240 300 360 420 480 540 600]);

ax2= nexttile;
plot(f_on(1:fm/2), 10*log10(pxx_on(1:fm/2)));
title('NIR Lights On');
xlabel('Frequency (Hz)');
ylabel('Power (dB/Hz)');
xticks([60 120 180 240 300 360 420 480 540 600]);

ax3 = nexttile;
plot(f_on_shield(1:fm/2), 10*log10(pxx_on_shield(1:fm/2)));
title('Shielded NIR Lights');
xlabel('Frequency (Hz)');
ylabel('Power (dB/Hz)');
xticks([60 120 180 240 300 360 420 480 540 600]);

sgtitle('Welchs Power Spectrum');
linkaxes([ax1,ax2, ax3], 'xy');

