import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy, MaxBoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from backscatter_env import BackscatterEnv
from backscatter_env_3 import BackscatterEnv3
from backscatter_env_4 import BackscatterEnv4
from backscatter02_env import Backscatter02Env

class BackscatterProcessor(Processor):
    def process_action(self, action):
        transmit = action % (BackscatterEnv.TIME_FRAME - BackscatterEnv.BUSY_TIMESLOT+1)
        action = action / (BackscatterEnv.TIME_FRAME - BackscatterEnv.BUSY_TIMESLOT+1)
        backscatter = action % (BackscatterEnv.BUSY_TIMESLOT+1)
        action = action / (BackscatterEnv.BUSY_TIMESLOT+1)
        harvest = action
        return tuple([harvest, backscatter, transmit])

class Backscatter02Processor(Processor):
    def process_action(self, action):
        transmit1 = action % (Backscatter02Env.TIME_FRAME+ 1)
        action = action / (Backscatter02Env.TIME_FRAME+ 1)

        backscatter1 = action % (Backscatter02Env.TIME_FRAME + 1)
        action = action / (Backscatter02Env.TIME_FRAME + 1)
        harvest = action
        return tuple([harvest, backscatter1, transmit1])

class BackscatterProcessor3(Processor):
    def process_action(self, action):
        transmit2 = action % (BackscatterEnv3.TIME_FRAME - BackscatterEnv3.BUSY_TIMESLOT+1)
        action = action / (BackscatterEnv3.TIME_FRAME - BackscatterEnv3.BUSY_TIMESLOT+1)
        transmit1 = action % (BackscatterEnv3.TIME_FRAME - BackscatterEnv3.BUSY_TIMESLOT + 1)
        action = action / (BackscatterEnv3.TIME_FRAME - BackscatterEnv3.BUSY_TIMESLOT + 1)

        backscatter2 = action % (BackscatterEnv3.BUSY_TIMESLOT+1)
        action = action / (BackscatterEnv3.BUSY_TIMESLOT+1)
        backscatter1 = action % (BackscatterEnv3.BUSY_TIMESLOT + 1)
        action = action / (BackscatterEnv3.BUSY_TIMESLOT + 1)
        harvest = action
        return tuple([harvest, backscatter1, backscatter2, transmit1, transmit2])

class BackscatterProcessor4(Processor):
    def process_action(self, action):
        transmit3 = action % (BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT + 1)
        action = action / (BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT + 1)
        transmit2 = action % (BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT+1)
        action = action / (BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT+1)
        transmit1 = action % (BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT + 1)
        action = action / (BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT + 1)

        backscatter3 = action % (BackscatterEnv4.BUSY_TIMESLOT + 1)
        action = action / (BackscatterEnv4.BUSY_TIMESLOT + 1)
        backscatter2 = action % (BackscatterEnv4.BUSY_TIMESLOT+1)
        action = action / (BackscatterEnv4.BUSY_TIMESLOT+1)
        backscatter1 = action % (BackscatterEnv4.BUSY_TIMESLOT + 1)
        action = action / (BackscatterEnv4.BUSY_TIMESLOT + 1)
        harvest = action
        return tuple([harvest, backscatter1, backscatter2, backscatter3, transmit1, transmit2, transmit3])

ENV_NAME = 'back_scatter'

# Get the environment and extract the number of actions.
env = BackscatterEnv3()
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

version = "3.0_3ST_09"
nb_steps = 1000000
nb_max_episode_steps = 200
anneal_steps = 400000
processor = BackscatterProcessor3()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, processor=processor, nb_steps_warmup=100,
               target_model_update=1e-2, policy=policy, vary_eps=True, anneal_steps=anneal_steps)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=nb_steps, visualize=True, verbose=2, log_interval=1000, nb_max_episode_steps=nb_max_episode_steps, version=version)

# After training is done, we save the final weights.
dqn.save_weights('../save_weight/dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=0, visualize=True, nb_max_episode_steps=nb_max_episode_steps)
