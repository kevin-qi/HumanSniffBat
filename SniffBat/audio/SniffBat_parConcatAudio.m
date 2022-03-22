function [] = SniffBat_parConcatAudio(data_dir)
% Concatenate audio data
% data_dir : folder containing .mat audio chunks

files = dir(sprintf('%s/*audio*mat', data_dir));
numFiles = length(files);

testChunk = load(sprintf('%s/audio_%d.mat',data_dir,0));
fs = testChunk.fs;

outPath = strrep(data_dir,'raw','processed');
if(~exist(outPath, 'dir'))
    mkdir(outPath);
end

for channel = 1:6
    disp(sprintf('Concatenating channel %d', channel))
    tic
    audioData = [];
    fs = testChunk.fs;
    parfor i = 1:numFiles
        dataChunk = load(sprintf('%s/audio_%d.mat',data_dir,i-1)); % Start from audio_0
        fs = dataChunk.fs;
        audioData = [audioData dataChunk.data(channel,:)];
    end
    if(~exist(fullfile(outPath, num2str(fs))))
        mkdir(fullfile(outPath, num2str(fs)));
    end
    save(fullfile(outPath,sprintf('%d/audioCh_%d.mat',fs,channel)), "audioData", "fs", "channel")
    audioData = decimate(double(audioData), 10);
    audioData = decimate(audioData, 10);
    fs = fs/100;
    if(~exist(fullfile(outPath, num2str(fs))))
        mkdir(fullfile(outPath, num2str(fs)));
    end
    save(fullfile(outPath,sprintf('%d/audioCh_%d.mat',fs,channel)), "audioData", "fs", "channel")
    toc
end



end