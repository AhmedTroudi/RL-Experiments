[![Python 3.11.0](https://img.shields.io/badge/python-3.11.0-blue.svg)](https://www.python.org/downloads/release/python-3120/)

# RL Experiments
This is an example of the path the robot decides to take using Q-Learning
when the environment is stochastic (random action chance = 10%).
- red is mud (gives very bad negative rewards)
- grey are obstacles
- yellow is the path taken
- blue cells indicate that it stepped there more than once (not shown in the example, but will show up in suboptimal paths).

In this example, it avoids the
path close to the red cells and decides to follow the slightly longer 'safer' path, 

![demo_q_learner.png](images%2Fdemo_q_learner.png)

## Prerequisites 
PDM: https://github.com/pdm-project/pdm/tree/main

For Linux/macOS:

```curl -sSL https://pdm-project.org/install-pdm.py | python3 -```

Alternatively, using Homebrew on macOS:

```brew install pdm```

## Usage
From project directory:

`
pdm run src/rl_experiments/main.py --epochs 5000 
`

Or:

`
pdm run src/rl_experiments/main.py --epochs 5000 --filename <file-path>
`

## Arguments:

`--epochs`: number of episodes

`--filename`: you can create your own map by providing your own csv file and 
feeding to the script using this argument. You can look into the enum `cell_type.py` to know how
to encode the cells (obstacles etc...)

`--dyna`: number of iterations for dyna, by default = 0 (disabled)

`--verbose`: to show some logs while running (work in progress)



