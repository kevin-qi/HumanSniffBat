% Script to extract epochs / trials where bat is close to human

% load data
ciholas2cortex = load('ciholas2cortex_scaling_factors.mat').ciholas2cortex;
ciholas = load('/home/batlab/Desktop/HumanBat/data/14592/processed/220123/b149f/ciholas/extracted_220123_cdp_1.mat')
cortex = load('/home/batlab/Desktop/HumanBat/data/14592/processed/220123/b149f/cortex/220123_14592_tracking_1_track.mat')

% Format the tracking Marker data
[Location, Location_interp] = ImBat_formatTracking(cortex.Markers);
Location_times = [1:length(cortex.AnalogSignals)];

% Segment the flights
[segmented_trajectories] =  ImBat_SegTrajectories(Location,Location_times);

