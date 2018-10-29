import network
import gc

import utaskmanager
import config
import snake
import ledmatrix
import text

if config.USE_NETWORK_JOYSTICK:
    import network_joystick as joystick
else:
    import joystick


class Menu(utaskmanager.Task):
    def __init__(self, matrix, jostick):
        super().__init__()
        self.options = ["Snake", "net", "mem"]
        self.matrix = matrix
        self.selected_option = 0
        self.joystick = jostick
        self.current_task = None
        self.text_scroller = text.TextScrollerTask(matrix)
        self.text_scroller.set_text(self.options[0])
        utaskmanager.add_task(self.text_scroller)

    def task_step(self):
        # do nothing if a task is currently running
        if self.current_task is not None and self.current_task.task_running:
            return
        else:
            self.text_scroller.unpause()

        wasd = self.joystick.direction()
        self._handle_input(wasd, self.joystick.btn_pressed())

    def _handle_input(self, wasd, btn_pressed):
        num_options = len(self.options)
        if wasd == 'a':
            self.selected_option = (self.selected_option + 1) % num_options
        elif wasd == 'd':
            self.selected_option = (self.selected_option - 1) % num_options

        if wasd in ('a', 'd'):
            opt = self.options[self.selected_option]
            print(opt, "selected")
            self.text_scroller.set_text(opt + ' ')

        if btn_pressed:
            self._select_current_option()

    def _select_current_option(self):
        option = self.options[self.selected_option]
        print("Selected", option)
        if option == 'Snake':
            self.text_scroller.pause()
            game = snake.SnakeGame(self.matrix, self.joystick)
            utaskmanager.add_task(game)
            self.current_task = game

        elif option == 'net':
            # show ip address
            sta = network.WLAN(network.STA_IF)
            tc = text.TextScroller(self.matrix)
            tc.scroll_text(" IP: " + sta.ifconfig()[0] + "  ")

        elif option == 'mem':
            mem_free = gc.mem_free()
            tc = text.TextScroller(self.matrix)
            tc.scroll_text("mem free " + str(mem_free) + " Bytes ")


def start():
    print("Starting firmware...")

    matrix = ledmatrix.LedMatrix()
    jstick = joystick.joy
    if config.USE_NETWORK_JOYSTICK:
        utaskmanager.add_task(joystick.joy)

    utaskmanager.add_task(Menu(matrix, jstick))

    utaskmanager.start()
