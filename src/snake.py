import uos
import ledmatrix
import uasyncio as asyncio
import network_joystick as joystick
# import joystick


class SnakeGame:
    """Snake Game. Controlled with an attached Joystick."""

    INIT_SNAKE_BODY = [(3, 1), (2, 1), (1, 1)]
    INIT_SNAKE_DIRECTION = [1, 0]

    def __init__(self, matrix, joystick):
        self.matrix = matrix
        self.snake_body = SnakeGame.INIT_SNAKE_BODY
        self.snake_direction = SnakeGame.INIT_SNAKE_DIRECTION
        self.pills = []
        self.max_pills = self.matrix.width // 4
        self.joystick = joystick
        self.reset()

    async def as_run(self):
        print("Starting snake game")
        while True:
            self.prepare()
            self.handle_input()
            self.update_screen()

            self.matrix.show()
            await asyncio.sleep_ms(10)

    def reset(self):
        print('Resetting game')
        self.snake_body = SnakeGame.INIT_SNAKE_BODY
        self.snake_direction = SnakeGame.INIT_SNAKE_DIRECTION
        for _i in range(self.max_pills):
            self.create_new_pill()

    def prepare(self):
        self.move_snake()
        if len(self.snake_body) != len(set(self.snake_body)):
            # snake eats itself
            self.reset()

        # if pills have been eaten, fill up with new ones
        while len(self.pills) <= self.max_pills:
            self.create_new_pill()

    def move_snake(self):
        # move the snakes head
        head = self.snake_body[0]
        new_head = ((head[0] + self.snake_direction[0]) % self.matrix.width,
                    (head[1] + self.snake_direction[1]) % self.matrix.height)

        if new_head in self.pills:
            # eat pill
            new_body = self.snake_body
            self.pills.remove(new_head)
        else:
            # move forward
            new_body = self.snake_body[:-1]
        self.snake_body = [new_head] + new_body

    def handle_input(self):
        xdir, ydir = self.snake_direction
        direction = self.joystick.direction()

        if direction == 'w' and ydir != 1:
            self.snake_direction = [0, -1]
        elif direction == 's' and ydir != -1:
            self.snake_direction = [0, 1]
        elif direction == 'd' and xdir != -1:
            self.snake_direction = [1, 0]
        elif direction == 'a' and xdir != 1:
            self.snake_direction = [-1, 0]

    def create_new_pill(self):
        new_pill = None
        while new_pill is None or \
                new_pill in self.snake_body or \
                new_pill in self.pills:

            rx, ry = uos.urandom(2)  # create two random bytes
            # create pill and fit into correct range
            new_pill = (rx * (self.matrix.width-1) // 255,
                        ry * (self.matrix.height-1) // 255)

        self.pills.append(new_pill)

    def update_screen(self):
        for x in range(self.matrix.width):
            for y in range(self.matrix.height):
                val = (x, y) in self.snake_body or (x, y) in self.pills
                self.matrix.px(x, y, val)


def main():
    matrix = ledmatrix.LedMatrix()
    game = SnakeGame(matrix=matrix, joystick=joystick.joy)

    loop = asyncio.get_event_loop()
    loop.create_task(joystick.as_handle_udp_packets())
    loop.create_task(game.as_run())
    loop.run_forever()

