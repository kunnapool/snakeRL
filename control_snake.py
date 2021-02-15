from game import SnakeGame, Direction, State
from time import sleep
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from threading import Thread
from threading import Lock
import time

mutex = Lock()

style.use('fivethirtyeight')

GAMMA = 0.7
EPSILON = 0.1 # such exploration, much wow
NUM_EPISODES = 10000
TOTAL_REWARD_SUM = 0.0

# initialize state-action array
state_action_q_vals = {}

action_space = [d for d in Direction]

all_rewards = []
mean_rewards = []

def play_game():

    global TOTAL_REWARD_SUM

    # play 10 episodes
    num_episodes = 0
    while num_episodes < NUM_EPISODES:

        game = SnakeGame()
        current_state = None
        total_reward = 0
        
        # one episode
        while True:
            
            # random.seed()
            do_explore = random.randint(1, 10)
            # exploitation
            if current_state != None and do_explore <= 7:
                current_action = max(state_action_q_vals[current_state])
            # exploration
            else:
                # print(do_explore, " EXPLORING!!!")
                current_action = random.choice(action_space)

            game_over, new_state, reward = game.play_step(current_action)
            current_state = new_state
            total_reward += reward
            
            if game_over:
                break

            if new_state not in state_action_q_vals:
                state_action_q_vals[new_state] = [0, 0, 0, 0]
                old_q = 0
            else:
                old_q = state_action_q_vals[current_state][current_action]

            new_q = old_q + GAMMA * (reward + max(state_action_q_vals[new_state]))
        
        num_episodes += 1
        TOTAL_REWARD_SUM += total_reward
        all_rewards.append(total_reward)

        mean_r = TOTAL_REWARD_SUM/len(all_rewards)
        mean_rewards.append(mean_r)
        
        print(num_episodes + 1, " Mean reward: ", mean_r)

start = time.time()
play_game()
end = time.time()

print("\n\n-----------------------------------------------\n\nTotal time: ", end-start)

plt.plot(mean_rewards)
plt.show()

