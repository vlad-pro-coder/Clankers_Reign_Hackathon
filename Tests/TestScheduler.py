from Scheduler import Scheduler
import time
from typing import List, Callable, Any, Deque
from collections import deque
import math

scheduler = Scheduler()\
        .add_task(
            lambda: (
                print("hello")
            ),
            lambda: True
        )\
        .wait_seconds(3)\
        .add_task(
            lambda: (
                print("hello second 3")
            ),
            lambda: True
        )

while not scheduler.is_done():
    scheduler.update()