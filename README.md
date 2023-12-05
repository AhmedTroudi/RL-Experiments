[![Python 3.12.0](https://img.shields.io/badge/python-3.12.0-blue.svg)](https://www.python.org/downloads/release/python-3120/)

## RL Experiments

## Description
This is an example of the path the robot decides to take using Q-Learning
when the environment is stochastic (random action chance = 10%).
- red is mud (gives very bad negative rewards)
- grey are obstacles
- yellow is the path taken
- blue cells indicate that it stepped more than once there,
so the path shown here is not the optimal path.

In this example, it avoids the
path close to the red cells and decides to follow the slightly longer 'safer' path, 

![demo_q_learner.png](images%2Fdemo_q_learner.png)

## Prerequisites

You only need Python 3.12 and `numpy==1.26.2` (or any new version should work)

## Usage
`
python main.py --epochs 5000
`
## Arguments:

`--epochs`: number of episodes

`--filename`: you can create your own n-by-n map by providing your own csv file and 
feeding to the script using this argument. You can look into `cell_type.py` to know how
to encode the cells (obstacles etc...)

`--dyna`: number of iterations for dyna, by default = 0 (disabled)

`--verbose`: to show some logs while running (work in progress)



