import numpy
import random


def total(grid):
    total = 0
    for row in grid:
        for column in row:
            total += 1
    return total

def get_reward_matrix(grid, total):
    reward_matrix = numpy.array(numpy.zeros([total, len(grid[0])]))
    for row in range(len(grid)):
        for column in range(len(grid[row])):

            # Check for 0s, -1s, and 1s to the left of each cell
            if column > 0:
                if grid[row, column - 1] == 0:
                    reward_matrix[row * len(grid[row]) + column, 0] = -1
                elif grid[row, column - 1] == -1:
                    reward_matrix[row * len(grid[row]) + column, 0] = -100
                elif grid[row, column - 1] == 1:
                    reward_matrix[row * len(grid[row]) + column, 0] = 5

            # Check for 0s, -1s, and 1s to the right of each cell
            if column < len(grid[row]) - 1:
                if grid[row, column + 1] == 0:
                    reward_matrix[row * len(grid[row]) + column, 1] = -1
                elif grid[row, column + 1] == -1:
                    reward_matrix[row * len(grid[row]) + column, 1] = -100
                elif grid[row, column + 1] == 1:
                    reward_matrix[row * len(grid[row]) + column, 1] = 5

            # Check for 0s, -1s, and 1s above each cell
            if row > 0:
                if grid[row - 1, column] == 0:
                    reward_matrix[row * len(grid[row]) + column, 2] = -1
                elif grid[row - 1, column] == -1:
                    reward_matrix[row * len(grid[row]) + column, 2] = -100
                elif grid[row - 1, column] == 1:
                    reward_matrix[row * len(grid[row]) + column, 2] = 5

            # Check for 0s, -1s, and 1s below each cell
            if row < len(grid[row]) - 1:
                if grid[row + 1, column] == 0:
                    reward_matrix[row * len(grid[row]) + column, 3] = -1
                elif grid[row + 1, column] == -1:
                    reward_matrix[row * len(grid[row]) + column, 3] = -100
                elif grid[row + 1, column] == 1:
                    reward_matrix[row * len(grid[row]) + column, 3] = 5

    return reward_matrix


def get_q_matrix(grid, total):
    q_matrix = numpy.array(numpy.zeros([total, len(grid[0])]))
    return q_matrix


def maximum(array):
    total = 0
    for i in array:
        total += i
    average = total/len(array)
    for i in array:
        if i > average:
            average = i
    return average


def available_actions(state, reward_matrix):
    current_state_row = reward_matrix[state, :]
    av_act = []
    for i in range(len(current_state_row)):
        if current_state_row[i] != 0:
            av_act.append(i)
    return(av_act)


def sample_next_action(action_range):
    next_action = random.choice(action_range)
    return next_action


def update_q(state, action, q_matrix, reward_matrix, new_state):
    action_points = []
    for i in available_actions(new_state, reward_matrix):
        action_points.append(q_matrix[new_state, i])
    new_q = q_matrix[state, action] + (0.1 * (reward_matrix[state, action] + (0.9 * (maximum(action_points))) - q_matrix[state, action]))
    q_matrix[state, action] = new_q

def update_state(state, action, grid, q_matrix, reward_matrix):
    new_state = 0
    if action == 0:
        new_state = state - 1
    elif action == 1:
        new_state = state + 1
    elif action == 2:
        new_state = state - len(grid[0])
    elif action == 3:
        new_state = state + len(grid[0])

    update_q(state, action, q_matrix, reward_matrix, new_state)
    return new_state


def educated_next_action(current_state, q_matrix, reward_matrix):
    state_actions = available_actions(current_state, reward_matrix)
    rewards = []
    for i in state_actions:
        rewards.append(q_matrix[current_state, i])
    maximum_reward = maximum(rewards)

    for i in state_actions:
        if q_matrix[current_state, i] == maximum_reward:
            decision = i
            break
    return decision