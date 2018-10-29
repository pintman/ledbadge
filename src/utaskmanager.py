'''
Task manager for tasks that should run pseudo-parallel in micropython. 

A demo application of this package is found inside the demo() method.

Part of this code based on the tutorial about the uasyncio upy package found
here: https://github.com/peterhinch/micropython-async/blob/master/TUTORIAL.md
'''
import uasyncio as asyncio


class Task:
    TASK_SLEEP_TIME_MS = 5

    def __init__(self, name=''):
        self.task_running = False
        self._paused = False
        self.name = name

    def pause(self):
        self._paused = True

    def unpause(self):
        self._paused = False

    def finish(self):
        self.task_running = False

    async def start(self):
        self.task_running = True
        while self.task_running:
            if not self._paused:
                self.task_step()

            await asyncio.sleep_ms(Task.TASK_SLEEP_TIME_MS)

    def task_step(self):
        '''
        This method must be overriden by each task. It provides the method 
        for each task step that runs in an endless loop or until 
        self.task_running is set to false. 

        Don't use time.sleep(3) in here, it will block the whole python
        process and other tasks cannot run.
        '''


def add_task(task):
    'Schedule a task for the tast manager.'
    loop = asyncio.get_event_loop()
    loop.create_task(task.start())


def start():
    'Start the task manager and run forever.'
    loop = asyncio.get_event_loop()
    loop.run_forever()


def demo():
    # Create a class that derives from Task and implement the task_step method
    class SampleTaskCounter(Task):
        'Demo task that counts between two values'

        def __init__(self, start_value=0, end_value=100):
            super().__init__(name='Demo task')  # call __init__ from Task class

            # init attributes
            self.counter = start_value
            self.end_value = end_value

        def task_step(self):
            'Print counter value and count up if necessary'
            print(self.counter)
            if self.counter < self.end_value:
                self.counter += 1
            else:
                self.finish()

    # Add instances of the demo class to the task manager and start it.
    add_task(SampleTaskCounter(start_value=0, end_value=10))
    add_task(SampleTaskCounter(start_value=1000, end_value=1015))
    start()
