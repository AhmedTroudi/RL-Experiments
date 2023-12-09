from abc import ABC, abstractmethod


class Learner(ABC):

    @abstractmethod
    def act_without_updating_policy(self, state: int) -> int:
        pass

    @abstractmethod
    def act(self, new_state: int, reward: float) -> int:
        pass

    @abstractmethod
    def select_action(self, state: int) -> int:
        pass
