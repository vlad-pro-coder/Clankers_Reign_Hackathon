import time
from collections import deque
from typing import Callable, List
from Task import Task

class Scheduler:
    def __init__(self):
        self.tasks = deque()

    def add_task(self, actions: Callable[[], None], conditions: Callable[[], bool]) -> 'Scheduler':
        self.tasks.append(Task(actions, conditions))
        return self

    def is_done(self) -> bool:
        return len(self.tasks) == 0

    #def wait_for_still(self, localizer) -> 'Scheduler':
    #    return self.add_task(
    #        lambda: None,
    #        lambda: abs(localizer.get_velocity()['x']) < 10 and
    #                abs(localizer.get_velocity()['y']) < 10 and
    #                abs(localizer.get_velocity()['h']) < 3 * (3.141592 / 180)
    #    )

    def wait_seconds(self, sec: float) -> 'Scheduler':
        start_time = {'t': None}

        def action():
            start_time['t'] = None

        def condition():
            if start_time['t'] is None:
                start_time['t'] = time.time()
                return False
            if (time.time() - start_time['t']) >= sec:
                start_time['t'] = None
                return True
            return False

        return self.add_task(action, condition)

    def add_another_scheduler(self, other: 'Scheduler') -> 'Scheduler':
        self.tasks.extend(other.tasks)
        return self

    def clear(self):
        for task in self.tasks:
            task.ran_once = False
        self.tasks.clear()

    def update(self):
        if self.is_done():
            return
        task = self.tasks[0]
        if task.run():
            self.tasks.popleft()
