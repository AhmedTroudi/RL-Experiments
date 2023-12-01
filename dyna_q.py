import random

import numpy as np
from typing import Optional
from learner import Learner


class DynaQ(Learner):
    """
    Q-learning with Dyna option.
    """

    def __init__(self, num_states: int = 100, num_actions: int = 4, alpha: float = 0.2, gamma: float = 0.9,
                 epsilon: float = 0.5, epsilon_decay: float = 0.99, dyna: int = 0, verbose: bool = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.dyna = dyna
        self.state = 0
        self.action = 0
        self.Q = np.zeros((num_states, num_actions), dtype=float)

        if dyna > 0:
            self.R = np.zeros((self.num_states, self.num_actions), dtype=float)
            self.T = np.zeros((self.num_states, self.num_actions, self.num_states), dtype=float)
            self.Tc = np.full((self.num_states, self.num_actions, self.num_states), 0.001)

    def act_without_updating_policy(self, state: int) -> int:
        selected_action = self.select_action(state)

        self.state = state
        self.action = selected_action
        if self.verbose:
            print(f"state = {state}, action = {selected_action}")
        return selected_action

    def act(self, new_state: int, reward: float) -> int:

        # decide if we take random action or use q_table
        action = self.select_action(new_state)
        
        self.epsilon = self.epsilon * self.epsilon_decay  # update probability of taking random actions

        self.update_qtable(self.state, self.action, new_state, reward)

        if self.dyna > 0:
            self.run_dyna(new_state, reward)

        self.action = action
        self.state = new_state

        if self.verbose:
            print(f"state = {new_state}, action = {action}, reward={reward}")

        return action

    def update_qtable(self, state: int, action: int, new_state: int, reward: Optional[float | np.ndarray]):
        target = reward + self.gamma * np.max(self.Q[new_state, :])
        current_value = self.Q[state, action]
        self.Q[state, action] = (1 - self.alpha) * current_value + self.alpha * target

    def select_action(self, state: int) -> int:
        if random.uniform(0.0, 1.0) <= self.epsilon:
            action = random.randint(0, self.num_actions - 1)  # choose a random action
            return action
        
        # choose action to take using Q table
        action = np.argmax(self.Q[state])
        return action

    def update_transitions(self, new_state: int):
        self.Tc[self.state, self.action, new_state] += 1  # increment count for number of times this experience occurred
        self.T = self.Tc / np.sum(self.Tc, axis=0)

    def update_rewards(self, reward: float):
        self.R[self.state, self.action] = (self.R[self.state, self.action] +
                                           self.alpha * (reward - self.R[self.state, self.action]))

    def run_dyna(self, new_state: int, reward: float):
        self.update_transitions(new_state)
        self.update_rewards(reward)
        # simulate experiences
        for _ in range(0, self.dyna):
            state = random.randint(0, self.num_states - 1)
            action = random.randint(0, self.num_actions - 1)
            new_state = np.argmax(self.T[state, action, :])
            reward = self.R[state, action]
            # update Q
            self.update_qtable(state, action, new_state, reward)
