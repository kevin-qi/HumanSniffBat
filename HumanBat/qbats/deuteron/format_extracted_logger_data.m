function format_extracted_logger_data(logger_dir)
%format_extracted_logger_data Loads extracted data from individual .mat files and saves into a
%(num_channels, num_samples) format in both .mat and .bin

disp(logger_dir)
data = load_extracted_data_logger(fullfile(logger_dir, 'extracted_data'));


if(~isfile(fullfile(logger_dir, 'logger_data.mat')))
    disp("Saving logger data to .mat")
    save(fullfile(logger_dir, 'logger_data.mat'), 'data','-v7.3')
end

if(~isfile(fullfile(logger_dir, 'logger_data.bin')))
    disp("Saving logger data to .bin")
    fileID = fopen(fullfile(logger_dir, 'logger_data.bin'), 'w');
    fwrite(fileID, data.csc.', 'int16');
    fclose(fileID)
end

%if(~isfile(fullfile(logger_dir, 'logger_data.mat')))
%    disp("Saving CAR and HP filtered logger data to .bin")
%    for i=1:16
%        disp(sprintf('highpass filtered channel %d',i));
%        data.csc(:,i) = highpass(double(data.csc(:, i)), 300, 31250);
%    end
%    med_csc = median(data.csc.',1);
%    fileID = fopen(fullfile(logger_dir, 'logger_data_car.bin'), 'w');
%    fwrite(fileID, data.csc.' - med_csc, 'int16');
%    fclose(fileID)
%end


end