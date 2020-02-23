import numpy
import random
import pygame as pg
import qlibrary
import time

windowwidth = 550
windowheight = 550

pg.init()
win = pg.display.set_mode((windowwidth, windowheight))
setup = True

width = 50
margin = 5

grid = numpy.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])


def update():
    global grid
    global win
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row, column] == 0:
                pg.draw.rect(win, pg.Color("White"), ((width + margin) * column, (width + margin) * row, width, width))
            if grid[row, column] == 1:
                pg.draw.rect(win, pg.Color("Green"), ((width + margin) * column, (width + margin) * row, width, width))
            if grid[row, column] == -1:
                pg.draw.rect(win, pg.Color("Red"), ((width + margin) * column, (width + margin) * row, width, width))
            if grid[row, column] == 2:
                pg.draw.rect(win, pg.Color("Blue"), ((width + margin) * column, (width + margin) * row, width, width))
    pg.display.update()
update()

while setup:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            setup = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            column = pos[0] // (width + margin)
            row = pos[1] // (width + margin)
            if event.button == 1:
                grid[row, column] = -1
            if event.button == 2:
                grid[row, column] = 0
            if event.button == 3:
                grid[row, column] = 1
            update()



total = qlibrary.total(grid)

q_matrix = qlibrary.get_q_matrix(grid, total)

reward_matrix = qlibrary.get_reward_matrix(grid, total)

for i in range(1000):
    state = random.choice(range(0, total, 1))
    action_range = qlibrary.available_actions(state, reward_matrix)
    action = qlibrary.sample_next_action(action_range)
    qlibrary.update_state(state, action, grid, q_matrix, reward_matrix)



obstacles = []

for row in range(len(grid)):
    for column in range(len(grid[row])):
        if grid[row, column] == -1:
            obstacles.append(len(grid[row]) * row + column)


for row in range(len(grid)):
    for column in range(len(grid[row])):
        if grid[row, column] == 1:
            goal = len(grid[row]) * row + column


for i in range(1000):
    current_state = 0
    steps = [current_state]
    while current_state != goal:
        if current_state in obstacles:
            print("I hit an obstacle!")
            break

        decision = qlibrary.educated_next_action(current_state, q_matrix, reward_matrix)

        current_state = qlibrary.update_state(current_state, decision, grid, q_matrix, reward_matrix)

        steps.append(current_state)

    for i in steps:
        grid[int(i/len(grid[0])), i%len(grid[0])] = 2
        update()
    for i in steps:
        if i != goal and i not in obstacles:
            grid[int(i/len(grid[0])), i%len(grid[0])] = 0
        if i in obstacles:
            grid[int(i/len(grid[0])), i%len(grid[0])] = -1
        if i == goal:
            grid[int(i / len(grid[0])), i % len(grid[0])] = 1
    update()

wait = True
for i in steps:
    grid[int(i / len(grid[0])), i % len(grid[0])] = 2
    if i == goal:
        grid[int(i / len(grid[0])), i % len(grid[0])] = 1
update()

print(steps)

while wait:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            wait = False
