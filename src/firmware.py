import uasyncio as asyncio

import utaskmanager
import config
import snake
import ledmatrix

if config.USE_NETWORK_JOYSTICK:
    import network_joystick as joystick
else:
    import joystick


class Menu(utaskmanager.Task):
    def __init__(self, matrix, jostick):
        super().__init__()
        self.options = ["S", "C"]
        self.matrix = matrix
        self.selected_option = 0
        self.joystick = jostick
        self.current_task= None

    def task_step(self):
        # do nothing if a task is currently running
        if self.current_task is not None and self.current_task.task_running:
            return

        wasd = self.joystick.direction()
        self._handle_input(wasd, self.joystick.btn_pressed())
        self.matrix.clear()
        opt = self.options[self.selected_option]
        self.matrix.write_char(opt)
        self.matrix.show()

    def _handle_input(self, wasd, btn_pressed):
        if wasd == 'a':
            self.selected_option = max(0, self.selected_option - 1)
        elif wasd == 'd':
            self.selected_option = min(len(self.options)-1, 
                                       self.selected_option + 1)
        if btn_pressed:
            self._select_current_option()

    def _select_current_option(self):
        print("Selected", self.options[self.selected_option])
        if self.options[self.selected_option] == 'S':
            self.hidden = True
            game = snake.SnakeGame(self.matrix, self.joystick)
            utaskmanager.add_task(game)
            self.current_task = game


def start():
    print("Starting firmware...")

    matrix = ledmatrix.LedMatrix()
    jstick = joystick.joy
    if config.USE_NETWORK_JOYSTICK:
        utaskmanager.add_task(joystick.joy)

    utaskmanager.add_task(Menu(matrix, jstick))

    utaskmanager.start()
