import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
from action_space import ActionSpace
from state_space import StateSpace
from gym.spaces import Discrete
from ST import SecondTransmitor
import random

class Backscatter02Env(gym.Env):
    TIME_FRAME = 10
    BUSY_RATE = 0.6

    def __init__(self):

        # System parameters
        self.nb_ST = 2
        self.state_size = 2 * self.nb_ST + 1
        self.nb_actions = (Backscatter02Env.TIME_FRAME+1) ** 3

        self.action_space = ActionSpace((Discrete(Backscatter02Env.TIME_FRAME+1),
                                         Discrete(Backscatter02Env.TIME_FRAME+1),
                                         Discrete(Backscatter02Env.TIME_FRAME+1)))

        self.observation_space = StateSpace((Discrete(SecondTransmitor.QUEUE), Discrete(SecondTransmitor.ENERGY),
                                             Discrete(SecondTransmitor.QUEUE), Discrete(SecondTransmitor.ENERGY),
                                             Discrete(Backscatter02Env.TIME_FRAME + 1)))

        # initialize Second Transmitters
        self.ST1 = SecondTransmitor()
        self.ST2 = SecondTransmitor()
        self.busy_slot = None

        self.viewer = None
        self.state = None
        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        harvest = action[0]
        backscatter_time_1 = action[1]
        transmit_time_1 = action[2]
        backscatter_time_2 = self.busy_slot - harvest - backscatter_time_1
        transmit_time_2 = Backscatter02Env.TIME_FRAME - self.busy_slot - transmit_time_1
        reward = 0
        if((backscatter_time_2 >= 0) and (transmit_time_2 >= 0)):
            harvest_time_1 = self.busy_slot - backscatter_time_1
            harvest_time_2 = self.busy_slot - backscatter_time_2

            reward += self.ST1.update(harvest_time_1, backscatter_time_1, transmit_time_1)
            reward += self.ST2.update(harvest_time_2, backscatter_time_2, transmit_time_2)

            state = [self.ST1.queue, self.ST1.energy, self.ST2.queue, self.ST2.energy, self.busy_slot]
            self.state = tuple(state)
            throughtput = reward
            self.updateBusyTime()

        else:   # in case, assignment is not suitable
            reward = -10
            throughtput = 0
            self.ST1.generateData()
            self.ST2.generateData()
            self.updateBusyTime()
            print(np.array(self.state), [reward, throughtput], action)

        done = False
        # print(np.array(self.state), reward, done, {})
        return np.array(self.state), [reward, throughtput], done, {}

    def reset(self):
        self.state = []
        self.ST1.reset()
        self.ST2.reset()
        self.updateBusyTime()
        state = [self.ST1.queue, self.ST1.energy, self.ST2.queue, self.ST2.energy, self.busy_slot]
        self.state = tuple(state)
        print(self.state)
        self.steps_beyond_done = None
        return np.array(self.state)

    def updateBusyTime(self):
        self.busy_slot = 0
        for i in range(Backscatter02Env.TIME_FRAME):
            if (random.uniform(0,1) < Backscatter02Env.BUSY_RATE):
                self.busy_slot += 1


    def updateObservation(self):
        return

    def render(self, mode='human', close=False):
       return

    def close(self):
        """Override in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        raise NotImplementedError()

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).

        # Returns
            Returns the list of seeds used in this env's random number generators
        """
        raise NotImplementedError()

    def configure(self, *args, **kwargs):
        """Provides runtime configuration to the environment.
        This configuration should consist of data that tells your
        environment how to run (such as an address of a remote server,
        or path to your ImageNet data). It should not affect the
        semantics of the environment.
        """
        raise NotImplementedError()

# env = BackscatterEnv()
# env.reset()
# for index in range(0, 1000):
#     env.step(env.action_space.sample())