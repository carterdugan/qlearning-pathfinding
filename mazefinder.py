import numpy
import random
import pygame as pg
import qlibrary


# Set width and height of UI window
windowwidth = 550
windowheight = 550

# Initialize PyGame
pg.init()

# Create PyGame window
win = pg.display.set_mode((windowwidth, windowheight))
pg.display.set_caption("Solomon the Pathfinding AI")

# Initialize loop for customizing maze grid
setup = True

# Set dimensions of cells and their margins
width = 50
margin = 5

# Initialize the maze grid
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

'''
Update the game window.
'''
def update():
    global grid
    global win
    for row in range(len(grid)):
        for column in range(len(grid[row])):

            # Draw empty cells
            if grid[row, column] == 0:
                pg.draw.rect(win, pg.Color("White"), ((width + margin) * column, (width + margin) * row, width, width))
            # Draw cells occupied by the end goal
            if grid[row, column] == 1:
                pg.draw.rect(win, pg.Color("Green"), ((width + margin) * column, (width + margin) * row, width, width))
            # Draw cells occupied by walls
            if grid[row, column] == -1:
                pg.draw.rect(win, pg.Color("Red"), ((width + margin) * column, (width + margin) * row, width, width))
            # Draw cells occupied by the path finder
            if grid[row, column] == 2:
                pg.draw.rect(win, pg.Color("Blue"), ((width + margin) * column, (width + margin) * row, width, width))
    pg.display.update()

# Initialize game window by calling update function
update()

'''
Loop for customizing game grid
'''
while setup:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            setup = False
        # Take user input for drawing game environment
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

# Initialize the total variable using qlibrary
total = qlibrary.total(grid)

# Initialize the q_matrix using qlibrary
q_matrix = qlibrary.get_q_matrix(grid, total)

# Initialize the reward matrix using qlibrary
reward_matrix = qlibrary.get_reward_matrix(grid, total)

'''
Initial 'exploration' training, 200 iterations
'''
for i in range(200):
    state = random.choice(range(0, total, 1)) # Picks random state
    action_range = qlibrary.available_actions(state, reward_matrix) # Evaluate all possible next actions
    action = qlibrary.sample_next_action(action_range) # Execute random action
    qlibrary.update_state(state, action, grid, q_matrix, reward_matrix) # Update the state and q-value of Q(s, a)

# Initialize list of obstacles for 'game over' check
obstacles = []

# Add obstacles to obstacle list
for row in range(len(grid)):
    for column in range(len(grid[row])):
        if grid[row, column] == -1:
            obstacles.append(len(grid[row]) * row + column)

# Locate user-placed end goal
for row in range(len(grid)):
    for column in range(len(grid[row])):
        if grid[row, column] == 1:
            goal = len(grid[row]) * row + column


'''
'Exploitation' training, 1000 iterations
'''
for i in range(1000):
    # Start Solomon in the top left-hand corner of the grid
    current_state = 0
    # Initialize list of steps taken
    steps = [current_state]
    # Loop that resets Solomon after he meets his end goal
    while current_state != goal:
        if current_state in obstacles:
            print("I hit an obstacle!")
            break

        # Make an educated decision based on maximum immediate reward
        decision = qlibrary.educated_next_action(current_state, q_matrix, reward_matrix)

        # Updates the state based on the educated decision
        current_state = qlibrary.update_state(current_state, decision, grid, q_matrix, reward_matrix)

        steps.append(current_state)

    # Color the cells to illustrate path that Solomon took to his end point
    for i in steps:
        grid[int(i/len(grid[0])), i%len(grid[0])] = 2
        update()

    # If any other significant cells were covered up, return them to their original color
    for i in steps:
        if i != goal and i not in obstacles:
            grid[int(i/len(grid[0])), i%len(grid[0])] = 0
        if i in obstacles:
            grid[int(i/len(grid[0])), i%len(grid[0])] = -1
        if i == goal:
            grid[int(i / len(grid[0])), i % len(grid[0])] = 1
    update()

# Initialize the final loop which displays the frame showing the final path
wait = True

# Display the steps taken via blue cells
for i in steps:
    grid[int(i / len(grid[0])), i % len(grid[0])] = 2
    if i == goal:
        grid[int(i / len(grid[0])), i % len(grid[0])] = 1
update()

# Print the coordinates of the final path taken
print(steps)

# Frozen frame loop
while wait:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            wait = False
