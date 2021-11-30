import time
import board
from analogio import AnalogIn

analog_in_x = AnalogIn(board.A1)
analog_in_y = AnalogIn(board.A0)

last_broadcast_x = 0
last_broadcast_y = 0

def get_bite_value(input):
    val = round((input / 65536 * 512)) - 256
    if val <= 7 and val >= -7:
        val = 0
    return val

def broadcast_values(x, y):
    global last_broadcast_x
    global last_broadcast_y
    last_broadcast_x = x
    last_broadcast_y = y
    print(x, y)

def get_values():
    curr_x = get_bite_value(analog_in_x.value)
    curr_y = get_bite_value(analog_in_y.value)
    #print(curr_x, curr_y)
    if not curr_x == last_broadcast_x or not curr_y == last_broadcast_y:
        broadcast_values(curr_x, curr_y)

while True:
    get_values()
