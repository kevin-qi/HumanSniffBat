# B151 Interaction Task Experiment Protocol

## Pre-experiment
1. Prepare smoothie in 2 syringes. Tap syringes together to remove air bubbles.
2. Attach syringes to feeders. Push smoothie all the way to the feeder port.
3. Check logger SD card is cleared and battery is charged.

## Experiment
4. Put a stimuli bat in cage setup to clean up any extra drippings from loading feeders
5. Turn Master8 ON
6. Set channel 1 to OFF (OFF, 1, ENTER)
7. Turn on NIR lights (power strip)
8. Setup laptop in experiment room
  - Connect ethernet cable
  - Connect laptop charger
  - Remote desktop into both Basler B151 and Batman Audio B151 via NeuroBatGroup account on chrome
9. Setup all 4 Basler cameras (top, bottom, side, front)
  - If needed, load camera settings from file
  - Change recording save path to current date
  - Position camera windows to be visible during experiment via remote desktop
  - Check recording settings are correct (50 fps, mp4, record every frame, no recording stop limit)
  - Capture a test image to ensure NIR lights are on / Use phone IR sensor 
10. Setup LoggerCommand3
  - Open LoggerCommand3
  - Synchronize
  - Load saved settings from file
  - Double check high pass frequency is 1hz and event channel (4) is INPUT,RISING and events are logged to SD card
11. Remove stimuli bat from cage setup

12. Start MOTU recording
  - `python python/record_mics.py a_bats <today's_date>_<bat_id>`
13. Run arduino task logic
  - `python python/main.py`
  - `a_bats`
  - `<today's_date>_<bat_id>`
  - `test`
14. Start recording on all 4 basler cameras
  - Ensure that the recording button is greyed out after clicking it. If it does not grey out, then the recording didnt start and the software needs to be restarted.
15. Start recording on LoggerCommand3
16. Turn Master8 channel 1 ON (FR, 1, ENTER)
17. Place subject bat in interaction zone and close door.
18. Begin experiment

## Trial structure
19. Trials always begin with subject bat in interaction zone and door closed
20. Select stimuli bat number
21. Present stimuli bat in interaction zone (Walk clockwise, the long way around the cage)
22. When subject bat triggers a feeder, remove stimuli bat (Walk C.C.W., the short way)
23. When reward (if any) has been consumed, reset subject bat to interaction zone and close door
24. Repeat steps 20-23

## Post-experiment
25. Remove subject bat from cage
26. Turn Master8 channel 1 OFF (OFF, 1, ENTER)
27. Stop Logger recording
28. Stop Arduino task recording (Ctrl+C)
29. Stop MOTU recording (Ctrl+C)
  - Script will wait for chunk to finish before closing. It is normal for it to not immediately stop.
30. Stop all 4 Basler camera recording
31. Return bats, and clean up room, and upload data to server
