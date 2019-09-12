import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy, MaxBoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from backscatter_env_3 import BackscatterBlockchainEnv3

class BackscatterProcessor3(Processor):
    def process_action(self, action):
        action_trans = action % BackscatterBlockchainEnv3.MAX_NB_ACT_TRANS
        action_back = action / BackscatterBlockchainEnv3.MAX_NB_ACT_TRANS

        backscatter1, backscatter2, backscatter3 = self.decode_action(BackscatterBlockchainEnv3.MAX_BACK, action_back)
        transmit1, transmit2, transmit3 = self.decode_action(BackscatterBlockchainEnv3.MAX_TRANS, action_trans)

        return tuple([backscatter1, backscatter2, backscatter3, transmit1, transmit2, transmit3])

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
np.random.seed(123)
# env.seed(123)
nb_actions = env.nb_actions

# Next, we build a very simple model.

model = Sequential()
model.add(Flatten(input_shape=(1, env.state_size)))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(nb_actions, activation='linear'))

print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = EpsGreedyQPolicy()

version = "8.8_2"
nb_steps = 2000000
nb_max_episode_steps = 200
anneal_steps = 1000000
processor = BackscatterProcessor3()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, processor=processor, nb_steps_warmup=100,
               target_model_update=1e-2, policy=policy, vary_eps=True, strategy='exponential', anneal_steps=anneal_steps)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=nb_steps, visualize=True, verbose=2, log_interval=1000, nb_max_episode_steps=nb_max_episode_steps, version=version)

# After training is done, we save the final weights.
dqn.save_weights('../save_weight/dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=0, visualize=True, nb_max_episode_steps=nb_max_episode_steps)