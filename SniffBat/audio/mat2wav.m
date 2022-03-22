ttl_ch = load(sprintf('audio/192000/audioCh_%d.mat',1));

[r,lt,ut,ll,ul] = risetime(double(ttl_ch.audioData));

first_ttl_sample_ind = round(lt(1));
last_ttl_sample_ind = round(lt(end));

for i = 2:6
    disp(i)
    load(sprintf('audio/192000/audioCh_%d.mat',i))
    audiowrite(sprintf('mic_%d.wav',i),audioData(first_ttl_sample_ind:last_ttl_sample_ind),fs)
end