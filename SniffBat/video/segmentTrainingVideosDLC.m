fname = 'training_snippets.json'; 
fid = fopen(fname); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
segments = jsondecode(str);

for batId = fieldnames(segments)
    disp(batId{1})
    bat_segments = segments.(batId{1});
    for date = fieldnames(bat_segments)
        disp(date{1})
        fnames = dir(sprintf("raw/%s_%s_*",batId{1}(2:end),date{1}(2:end)));
        timestamps = bat_segments.(date{1});
        for i = 1:length(timestamps)
            disp(timestamps(i))
            s = timestamps(i).start;
            e = timestamps(i).end;
            for j = 1:length(fnames)
                path = fullfile(fnames(j).folder, fnames(j).name);
                out_path = strrep(path,'raw','processed');
                out_path = strrep(out_path,sprintf("%s_%s",batId{1}(2:end),date{1}(2:end)),sprintf('%s_%s_%d_%d',batId{1}(2:end),date{1}(2:end),s,e))
                disp(path)
                ffmpeg_cmd = sprintf("ffmpeg -ss %d -i %s -c copy -t %d %s",s,path,e-s, out_path)
                system(ffmpeg_cmd)
                disp(out_path)
            end
        end
    end
end