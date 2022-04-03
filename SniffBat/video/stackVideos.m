function [] = stackVideos(data_path, bat_id, date)
%STACKCAMERAS Summary of this function goes here
%   data_path : dir containing camera folders containing .mp4 file. 

dir(data_path)
stack_grid = {'left','right', 'front', 'bottom'};
for i = 1:length(stack_grid)
    camera_name = stack_grid{i};
    fname = dir(fullfile(data_path, camera_name,'*.mp4')).name;
    fpath{i} = fullfile(data_path, camera_name, fname);
end

vid_inputs = '';
for i = 1:length(stack_grid)
    vid_inputs = [vid_inputs ' -i ' fpath{i}];
end

scale_cmd = ['[0:v]scale=800:600[topleft];'...
             '[1:v]scale=800:600[topright];'...
             '[2:v]scale=800:600[botleft];'...
             '[3:v]scale=800:600[botright],'];

stack_cmd = ['[topleft][topright]hstack=inputs=2[top];'...
             '[botleft][botright]hstack=inputs=2[bottom];'...
             '[top][bottom]vstack=inputs=2[output]'];
out_fname = sprintf('%s_%s_stacked.mp4',num2str(bat_id), num2str(date));
out_path = strrep(data_path, 'raw', 'processed');
mkdir(out_path);
out_cmd = sprintf(' -map "[output]" %s',fullfile(out_path,out_fname));
cmd = ['ffmpeg' vid_inputs ' -filter_complex ' '"' scale_cmd stack_cmd '"' out_cmd];
%cmd = ['ffmpeg' '-i ' fpath{1} ' -t 30 -filter_complex ' '[0:v]scale=800:600[topleft]'];
disp(cmd)
system(cmd);

end

