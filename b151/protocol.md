# B151 Interaction Task Experiment Protocol

## Pre-experiment
1. Prepare smoothie in 2 syringes. Tap syringes together to remove air bubbles.
2. Attach syringes to feeders. Push smoothie all the way to the feeder port.
3. Check logger SD card is cleared and battery is charged.

## Experiment
4. Put a stimuli bat in cage setup to clean up any extra drippings from loading feeders
5. Turn Master8 ON
6. Set channel 1 to OFF (OFF, 1, ENTER)
7. Setup laptop in experiment room
  - Connect ethernet cable
  - Connect laptop charger
  - Remote desktop into both Basler B151 and Batman Audio B151 via NeuroBatGroup account on chrome
8. Setup all 4 Basler cameras (top, bottom, side, front)
  - If needed, load camera settings from file
  - Change recording save path to current date
  - Position camera windows to be visible during experiment via remote desktop
  - Check recording settings are correct (50 fps, mp4, record every frame, no recording stop limit)
9. Setup LoggerCommand3
  - Open LoggerCommand3
  - Synchronize
  - Load saved settings from file
  - Double check high pass frequency is 1hz and event channel (4) is INPUT,RISING and logged to SD card
10. Remove stimuli bat from cage setup

11. Start MOTU recording
  - `python python/record_mics.py a_bats <today's_date>_<bat_id>`
12. Run arduino task logic
  - `python python/main.py`
  - `a_bats`
  - `<today's_date>_<bat_id>`
  - `test`
13. Start recording on all 4 basler cameras
  - Ensure that the recording button is greyed out after clicking it. If it does not grey out, then the recording didnt start and the software needs to be restarted.
14. Start recording on LoggerCommand3
15. Turn Master8 channel 1 ON (FR, 1, ENTER)
16. Place subject bat in interaction zone and close door.
17. Begin experiment

## Trial structure
18. Trials always begin with subject bat in interaction zone and door closed
19. Select stimuli bat number
20. Present stimuli bat in interaction zone (Walk clockwise, the long way around the cage)
21. When subject bat triggers a feeder, remove stimuli bat (Walk C.C.W., the short way)
22. When reward (if any) has been consumed, reset subject bat to interaction zone and close door
23. Repeat steps 19-22

## Post-experiment
24. Remove subject bat from cage
25. Turn Master8 channel 1 OFF (OFF, 1, ENTER)
26. Stop Logger recording
27. Stop Arduino task recording (Ctrl+C)
28. Stop MOTU recording (Ctrl+C)
  - Script will wait for chunk to finish before closing. It is normal for it to not immediately stop.
29. Stop all 4 Basler camera recording
30. Return bats, and clean up room, and upload data to server
