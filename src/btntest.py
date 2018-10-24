import time
import ledmatrix
import joystick


matrix = ledmatrix.LedMatrix()
SLEEP_TIME = 0.01  # secconds betweent updates


def _show_btn_pressed():
    matrix.px(3, 3, True)


def _show_direction(wasd):
    offset = 4

    if wasd == 'w':
        matrix.px(offset, matrix.height - 1, True)
    elif wasd == 'a':
        matrix.px(0, offset, True)
    elif wasd == 's':
        matrix.px(offset, 0, True)
    elif wasd == 'd':
        matrix.px(matrix.width - 1, offset, True)


def main():
    print("Running pin test")
    while True:
        matrix.clear()

        if joystick.joy.btn_pressed():
            _show_btn_pressed()
            print('Button pressed')

        direction = joystick.joy.direction()
        print('Direction:', direction)
        _show_direction(direction)

        matrix.show()

        time.sleep(SLEEP_TIME)
