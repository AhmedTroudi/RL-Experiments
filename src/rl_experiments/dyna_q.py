import random
from typing import Optional

import numpy as np

from rl_experiments.learner import Learner


class DynaQ(Learner):
    """
    Q-learning with Dyna option.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
            self,
            num_states: int = 100,
            num_actions: int = 4,
            alpha: float = 0.2,
            gamma: float = 0.9,
            epsilon: float = 0.5,
            epsilon_decay: float = 0.99,
            dyna: int = 0,
            verbose: bool = False,
    ):
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
        self.q_table = np.zeros((num_states, num_actions), dtype=float)

        if self.dyna > 0:
            self.reward_matrix = np.zeros(
                (self.num_states, self.num_actions), dtype=float
            )
            self.transition_matrix = np.zeros(
                (self.num_states, self.num_actions, self.num_states), dtype=float
            )
            self.experiences_count = np.full(
                (self.num_states, self.num_actions, self.num_states), 0.001)

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

        # update probability of taking random actions
        self.epsilon = self.epsilon * self.epsilon_decay

        self.update_qtable(self.state, self.action, new_state, reward)

        if self.dyna > 0:
            self.run_dyna(new_state, reward)

        self.action = action
        self.state = new_state

        if self.verbose:
            print(f"state = {new_state}, action = {action}, reward={reward}")

        return action

    def update_qtable(
        self,
        state: int,
        action: int,
        new_state: int,
        reward: Optional[float | np.ndarray],
    ):
        target = reward + self.gamma * np.max(self.q_table[new_state, :])
        current_value = self.q_table[state, action]
        self.q_table[state, action] = (
            1 - self.alpha
        ) * current_value + self.alpha * target

    def select_action(self, state: int) -> int:
        if random.uniform(0.0, 1.0) <= self.epsilon:
            action = random.randint(0, self.num_actions - 1)  # choose a random action
            return action
        # choose action to take using Q table
        action = int(np.argmax(self.q_table[state]))
        return action

    def update_transitions(self, new_state: int):
        # increment count for number of times this experience occurred
        self.experiences_count[self.state, self.action, new_state] += 1
        self.transition_matrix = self.experiences_count / np.sum(
            self.experiences_count, axis=0
        )

    def update_rewards(self, reward: float):
        self.reward_matrix[self.state, self.action] = self.reward_matrix[
            self.state, self.action
        ] + self.alpha * (reward - self.reward_matrix[self.state, self.action])

    def run_dyna(self, new_state: int, reward: float):
        self.update_transitions(new_state)
        self.update_rewards(reward)
        # simulate experiences
        for _ in range(0, self.dyna):
            state = random.randint(0, self.num_states - 1)
            action = random.randint(0, self.num_actions - 1)
            new_state = int(np.argmax(self.transition_matrix[state, action, :]))
            reward = self.reward_matrix[state, action]
            # update Q
            self.update_qtable(state, action, new_state, reward)
