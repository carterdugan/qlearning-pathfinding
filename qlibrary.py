import numpy
import random



'''
Return the total amount of elements in a numpy array.
'''
def total(grid):
    total = 0
    for row in grid:
        for column in row:
            total += 1
    return total


'''
Create the reward matrix based off of the provided grid
'''
def get_reward_matrix(grid, total):
    reward_matrix = numpy.array(numpy.zeros([total, len(grid[0])]))  # Initialize reward matrix
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


'''
Generate the Q-Matrix based off of the provided grid.
'''
def get_q_matrix(grid, total):
    q_matrix = numpy.array(numpy.zeros([total, len(grid[0])]))
    return q_matrix


'''
Get the maximum value from a list or array.
'''
def maximum(array):
    total = 0  # Initialize the total as zero
    for i in array:
        total += i  # Add to the total for each element in the array
    average = total/len(array)  # Calculate the average value of the array
    for i in array:
        if i > average:
            average = i  # Find the maximum value
    return average  # Return the maximum value


'''
Retrieve a list of valid actions based off of the current state and reward matrix.
'''
def available_actions(state, reward_matrix):
    current_state_row = reward_matrix[state, :]  # Gather the correct row from the matrix based on state
    av_act = []  # Initialize the list of available actions
    for i in range(len(current_state_row)):
        if current_state_row[i] != 0:
            av_act.append(i)  # Check for a valid movement value. This is either 1 or -1 but not 0.
    return(av_act)


'''
Return a random action based off of a given state.
'''
def sample_next_action(action_range):
    next_action = random.choice(action_range)  # Randomly choose action
    return next_action


'''
Updates the q value within the q matrix via the q-learning algorithm after an action is taken.
'''
def update_q(state, action, q_matrix, reward_matrix, new_state):
    action_points = []  # Initialize list of points for each action
    for i in available_actions(new_state, reward_matrix):
        action_points.append(q_matrix[new_state, i])
    new_q = q_matrix[state, action] + (0.1 * (reward_matrix[state, action] +  # Q-Learning
                (0.9 * (maximum(action_points))) - q_matrix[state, action]))  # Algorithm
    q_matrix[state, action] = new_q  # Change q-value within the q-matrix


'''
Changes the state within the q_matrix depending on the aciton taken. This calls the update_q function to
update the corresponding q value.
'''
def update_state(state, action, grid, q_matrix, reward_matrix):
    new_state = 0  # Initialize the new_state value
    if action == 0:
        new_state = state - 1
    elif action == 1:
        new_state = state + 1
    elif action == 2:
        new_state = state - len(grid[0])
    elif action == 3:
        new_state = state + len(grid[0])

    update_q(state, action, q_matrix, reward_matrix, new_state)  # Calls to update Q after selecting the new state
    return new_state


'''
As opposed to the sample_next_action function, makes an educated decision based on the best reward provided by a
list of possible actions. returns the decision so the update state function must be called manually.
'''
def educated_next_action(current_state, q_matrix, reward_matrix):
    state_actions = available_actions(current_state, reward_matrix)  # Creates list of actions for current state
    rewards = []  # Initializes the list of rewards
    for i in state_actions:
        rewards.append(q_matrix[current_state, i])
    maximum_reward = maximum(rewards)  # Finds the maximum reward from rewards list

    for i in state_actions:
        if q_matrix[current_state, i] == maximum_reward:
            decision = i  # Makes decision based off of maximum reward.
            break
    return decision