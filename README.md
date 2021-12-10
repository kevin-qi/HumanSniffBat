# HumanBat

Welcome to the Human Bat Project! 

This project consists of a battery of 3 tasks involving a human, a bat (or bats), and food reward that aim to elicit representation of the human in the bat's brain. Wireless electrophysiology will be used to record from hippocampus CA1 during the three tasks.  

Go to Projects to find the to do list for each task: 

Go here for room hardware specs: https://docs.google.com/spreadsheets/d/121AViHbAI2MZlo37yAVifF2lvB6FgzjzcyXfmlC5a6w/edit#gid=1704225061

Go here for experiment protocol: https://docs.google.com/document/d/1WkFO3U5VYU4Rk_AlELU-ytDVp02BDh6ZnfDxpJU5Jpg/edit?usp=sharing

Individual experimental setup protocols can be found in the `protocol/` folder

Task 1 - Individual discrimmination task (B151)

Task 2 - Individual flight task (B149f)

Task 3 - Group behavior task (B149b)

Each task requires a different set of tools to collect and analyze the data. Ultimately, the findings from these three tasks will be synthesized to report findings of the extent to which the human experimenter is represented in the bat's brain. 

Three types of data are necessary to make conclusions about neural data from CA1:

1. Positional Data (Bat)

2. Positional Data (Human)

3. Neural Data (Bat)

Accessory data are useful for further refining and examining behaviors in the tasks

1. Audio Data (trills, human noises)

2. Close-up Video (sniffing, body position)

Behaviors that we hope to observe and quantify, but not yet robustly quantified:

1. Hovering (tracking of human)

2. Sniffing (time-delayed)

Hypothesis Chart for Setup 2 in B149f

<img width="537" alt="Screen Shot 2021-10-19 at 3 34 45 PM" src="https://user-images.githubusercontent.com/9907501/137999971-5ce54c5c-9bfe-4243-b4a5-38a49ee684a8.png">

# Setup
```python
1. git clone # Clone the repository
2. cd humanbat
3. conda env create -f environment.yml # Install conda env
4. conda activate bathuman # Activate installed env
5. Install LoggerDataProcessing in utils/
6. Install q-bats in utils/
5. python setup.py # Run the python configuration script
6. Install matlab engine for python:
    - cd <matlabroot>\extern\engines\python 
        # replace <matlabroot> with your path to matlab
        # (e.g. C:\Program Files\MATLAB\R2021b)
    - python setup.py install
    - For more details, see: https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
```


