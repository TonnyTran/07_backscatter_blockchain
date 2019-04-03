from __future__ import print_function
from collections import deque
from rl.agents.tabular_q_learner import QLearner
from backscatter_env_3 import BackscatterBlockchainEnv3
import xlwt
from ST import SecondTransmitor
import numpy as np

ENV_NAME = 'Federated_Learning'

# Get the environment and extract the number of actions.
env = BackscatterBlockchainEnv3()

def digitalizeState(observation, env=None):
    state = 0
    for index in range(0, env.array_size):
        state += observation[index] * env.interval_value[index]
    return state

def digitalizeAction(action):
    action_trans = action % BackscatterBlockchainEnv3.MAX_NB_ACT_TRANS
    action_back = action / BackscatterBlockchainEnv3.MAX_NB_ACT_TRANS

    backscatter1, backscatter2, backscatter3 = decode_action(BackscatterBlockchainEnv3.MAX_BACK, action_back)
    transmit1, transmit2, transmit3 = decode_action(BackscatterBlockchainEnv3.MAX_TRANS, action_trans)

    return tuple([backscatter1, backscatter2, backscatter3, transmit1, transmit2, transmit3])

def find_third_element(number):
    i = 0
    while number >= i * (i+1) * (i+2) / 6:
        i += 1
    return i - 1

def find_second_element(number):
    i = 0
    while number >= i * (i+1) / 2:
        i += 1
    return i - 1

def decode_action(max_action, action_nb):
    third_element = find_third_element(action_nb)
    action1 = max_action - third_element
    action_nb = action_nb - third_element * (third_element + 1) * (third_element + 2) / 6
    second_element = find_second_element(action_nb)
    action2 = max_action - action1 - second_element
    action_nb = action_nb - second_element * (second_element + 1) / 2
    first_element = action_nb
    action3 = max_action - action1 - action2 - first_element
    return action1, action2, action3

state_dim = env.interval_value[0] * env.array[0]
num_actions = env.nb_actions
print([state_dim, num_actions, state_dim*num_actions])


nb_steps = 10000000
anneal_steps = 4000000
MAX_STEPS = 200
MAX_EPISODES = nb_steps / MAX_STEPS

version = '1.0_4'
q_learner = QLearner(state_dim, num_actions, anneal_steps=anneal_steps, e_vary=True)

# open workbook to store result
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('QL')

episode_history = deque(maxlen=100)
i_episode = 1
i_step = 1
while i_step < nb_steps:
    # initialize
    observation = env.reset()
    state = digitalizeState(observation, env)
    action = q_learner.initializeState(state)
    dAction = digitalizeAction(action)
    episode_reward = np.zeros(18, dtype=np.float32)
    done = False

    while not done:
        env.render()
        observation, reward, done, _ = env.step(dAction)

        state = digitalizeState(observation, env)

        episode_reward += reward
        action = q_learner.updateModel(state, reward[0])
        dAction = digitalizeAction(action)
        training_data = episode_reward[1]
        if i_step % MAX_STEPS == 0:
            done = True
        i_step += 1


    episode_history.append(episode_reward[0])
    mean_rewards = np.mean(episode_history)

    sheet.write(i_episode, 0, str(i_episode))
    sheet.write(i_episode, 1, str(episode_reward[0]))
    sheet.write(i_episode, 2, str(episode_reward[1]))
    sheet.write(i_episode, 3, str(episode_reward[2]))
    sheet.write(i_episode, 4, str(float(episode_reward[2]) / episode_reward[1]))

    print("Episode {}".format(i_episode))
    print("Reward for this episode: {}".format(episode_reward[0]))
    print(episode_reward[0]/MAX_STEPS)
    print("Average reward for last 100 episodes: {:.2f}".format(mean_rewards))
    i_episode += 1

file_name = 'result_v' + version + '_QL.xls'
workbook.save('../results/' + file_name)