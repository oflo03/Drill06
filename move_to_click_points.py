from pico2d import *
import random
import math
from collections import deque

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)
ground = load_image('TUK_GROUND.png')
hand = load_image('hand_arrow.png')
run = [load_image('marin_run_back_right.png'), load_image('marin_run_back.png'),
       load_image('marin_run_back_left.png'), load_image('marin_run_front_left.png'),
       load_image('marin_run_front.png'), load_image('marin_run_front_right.png')]


def handle_events():
    global running, hands
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            hands.append((event.x, event.y * -1 + TUK_HEIGHT))


running = True
hands = deque()
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
face = 4

while running:
    clear_canvas()
    ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    for i in hands:
        hand.draw(i[0], i[1])
    run[face].clip_draw(frame * run[face].w // 6, 0, run[face].w // 6, run[face].h, x, y,
                        run[face].w // 6 * 4, run[face].h * 4)
    update_canvas()
    handle_events()
    if len(hands) != 0:
        x += (hands[0][0] - x) * 0.1
        y += (hands[0][1] - y) * 0.1
        face = int(math.acos((hands[0][0] - x) / math.sqrt(math.pow(hands[0][0] - x, 2) + math.pow(hands[0][1] - y, 2))) * 3 / math.pi)
        if hands[0][1] < y:
            face = face * -1 + 5
        if abs(hands[0][0] - x) < (hand.w + run[face].w) // 2 and abs(hands[0][1] - y) < (hand.h + run[face].h) // 2:
            hands.popleft()
    frame = (frame + 1) % 6
    delay(0.08)

close_canvas()
