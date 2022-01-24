function [] = HumanBat_playAudioClip(audio_snip)

    % Plays audio clip
    obj = audioplayer(audio_snip);
    %obj.TimerFcn='showSeconds';
    %obj.TimerPeriod=1;

    play(obj);

end