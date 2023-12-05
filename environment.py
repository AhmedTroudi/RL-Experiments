import random as rand
import numpy as np
from cell_type import CellType
from typing import Tuple
from learner import Learner


class Environment:
    def __init__(self, world: np.ndarray):
        self.world = world
        self.default_reward = -1
        self.mud_reward = -100
        self.goal_reward = 1
        self.random_action_chance = 0.1
        self.start_position = self.get_target_position(CellType.ROBOT.value)
        self.goal_position = self.get_target_position(CellType.GOAL.value)
        self.robot_moves = []

    def get_target_position(self, target: int):
        for row in range(self.world.shape[0]):
            for col in range(self.world.shape[1]):
                if self.world[row, col] == target:
                    return row, col
        return -100, -100

    def select_action(self, action: int):
        if rand.uniform(0.0, 1.0) <= self.random_action_chance:
            action = rand.randint(0, 3)  # choose the random direction
        return action

    @staticmethod
    def try_move(x: int, y: int, action: int):
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        x += moves[action][0]
        y += moves[action][1]
        return x, y

    def is_move_possible(self, x: int, y: int):
        return 0 <= x < self.world.shape[0] and 0 <= y < self.world.shape[1]

    def perform_move(self, x: int, y: int, previous_pos: Tuple):
        reward = self.default_reward
        cell_value = self.world[x, y]

        if cell_value == CellType.WALL.value:
            x, y = previous_pos
        elif cell_value == CellType.GOAL.value:
            reward = self.goal_reward
        elif cell_value == CellType.MUD.value:
            reward = self.mud_reward
            self.world[x, y] = CellType.IN_MUD.value
        elif cell_value == CellType.IN_MUD.value:
            reward = self.mud_reward

        return (x, y), reward

    def move_robot(self, previous_pos: Tuple, action: int):
        x, y = previous_pos

        action = self.select_action(action)

        x, y = self.try_move(x, y, action)

        if not self.is_move_possible(x, y):
            return previous_pos, self.default_reward

        return self.perform_move(x, y, previous_pos)

    @staticmethod
    def position_to_state(position: Tuple):
        return position[0] * 10 + position[1]

    def run_episode(self, epochs: int, learner: Learner, verbose: int):
        rewards = np.zeros((epochs, 1))

        for epoch in range(epochs):
            total_reward = 0
            robot_position = self.start_position
            state = self.position_to_state(robot_position)
            action = learner.act_without_updating_policy(state)
            count = 0
            # new episode, reset moves
            self.robot_moves = []

            while robot_position != self.goal_position and count < 10000:
                new_position, step_reward = self.move_robot(robot_position, action)

                if new_position == self.goal_position:
                    r = self.goal_reward
                else:
                    r = step_reward

                state = self.position_to_state(new_position)
                action = learner.act(state, r)

                robot_position = new_position
                total_reward += step_reward
                count += 1
                self.robot_moves.append(new_position)

            if count == 100000:
                print("timeout")

            if verbose:
                print(f"{epoch}, {total_reward}")

            rewards[epoch, 0] = total_reward

        return np.mean(rewards)