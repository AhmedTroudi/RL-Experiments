## RL Experiments

### Description
This is an example of the path the robot decides to take using Q-Learning
when the environment is stochastic (random action chance = 10%).
- red is mud (gives very bad negative rewards)
- grey are obstacles
- yellow is the path taken
- blue cells indicate that it stepped more than once there,
so the path shown here is not the optimal path.

In this example, it avoids the
path close to the red cells and decides to follow the slightly longer 'safer' path, 

![Demo-QLearner.png](images%2FDemo-QLearner.png)



