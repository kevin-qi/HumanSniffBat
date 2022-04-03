function [] = stackVideos(data_path)
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
          
out_cmd = ' -map "[output]" stacked.mp4';
cmd = ['ffmpeg' vid_inputs ' -t 10 -filter_complex ' '"' scale_cmd stack_cmd '"' out_cmd];
%cmd = ['ffmpeg' '-i ' fpath{1} ' -t 30 -filter_complex ' '[0:v]scale=800:600[topleft]'];
disp(cmd)
system(cmd);

end

