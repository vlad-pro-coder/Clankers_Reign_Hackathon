from typing import Callable

class Task:
    def __init__(self, actions: Callable[[], None], conditions: Callable[[], bool]):
        self.actions_func = actions
        self.conditions_func = conditions
        self.ran_once = False

    def run(self) -> bool:
        if not self.ran_once:
            self.ran_once = True
            self.actions_func()
        if self.conditions_func():
            self.ran_once = False
            return True
        return False