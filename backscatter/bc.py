import xlwt
import numpy as np
from backscatter_env_3 import BackscatterBlockchainEnv3
from rl.core import Processor

version = "1.0"
nb_steps = 10000000
nb_max_episode_steps = 200

class BackscatterProcessor3(Processor):
    def process_action(self, action):
        action_trans = action % BackscatterBlockchainEnv3.MAX_NB_ACT_TRANS
        action_back = action / BackscatterBlockchainEnv3.MAX_NB_ACT_TRANS

        backscatter1, backscatter2, backscatter3 = self.decode_action(BackscatterBlockchainEnv3.MAX_BACK, action_back)
        transmit1, transmit2, transmit3 = self.decode_action(BackscatterBlockchainEnv3.MAX_TRANS, action_trans)

        return [backscatter1, backscatter2, backscatter3, transmit1, transmit2, transmit3]

    def find_third_element(self, number):
        i = 0
        while number >= i * (i+1) * (i+2) / 6:
            i += 1
        return i - 1

    def find_second_element(self, number):
        i = 0
        while number >= i * (i+1) / 2:
            i += 1
        return i - 1

    def decode_action(self, max_action, action_nb):
        third_element = self.find_third_element(action_nb)
        action1 = max_action - third_element
        action_nb = action_nb - third_element * (third_element + 1) * (third_element + 2) / 6
        second_element = self.find_second_element(action_nb)
        action2 = max_action - action1 - second_element
        action_nb = action_nb - second_element * (second_element + 1) / 2
        first_element = action_nb
        action3 = max_action - action1 - action2 - first_element
        return action1, action2, action3

ENV_NAME = 'backscatter_blockchain'

# Get the environment and extract the number of actions.
env = BackscatterBlockchainEnv3()
nb_actions = env.nb_actions
processor = BackscatterProcessor3()
step = 1
episode = 1
# open workbook to store result
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('DQN')
while step < nb_steps - 1:
    episode_reward = np.float32(0)
    while (step % nb_max_episode_steps) != 0:
        action_nb = np.random.random_integers(0, nb_actions-1)
        action = processor.process_action(action_nb)
        action[3] = 0
        action[4] = 0
        action[5] = 0
        observation, reward, done, info = env.step(action)
        episode_reward += reward
        step += 1
    sheet.write(episode, 0, str(episode))
    sheet.write(episode, 1, str(episode_reward[0]))
    sheet.write(episode, 2, str(episode_reward[1]))
    sheet.write(episode, 3, str(episode_reward[2]))
    sheet.write(episode, 4, str(float(episode_reward[2])/episode_reward[1]))
    print (episode, episode_reward[0], episode_reward[1], episode_reward[2], float(episode_reward[2])/episode_reward[1])
    step += 1
    episode += 1
file_name = 'result_bc_v' + version
workbook.save('../results/' + file_name + '.xls')