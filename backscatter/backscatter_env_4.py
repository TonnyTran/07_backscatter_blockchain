import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
from action_space import ActionSpace
from state_space import StateSpace
from gym.spaces import Discrete
from ST import SecondTransmitor

class BackscatterEnv4(gym.Env):
    TIME_FRAME = 10
    BUSY_TIMESLOT = 6

    def __init__(self):

        # System parameters
        self.nb_ST = 4
        self.state_size = 2 * self.nb_ST
        self.nb_actions = (BackscatterEnv4.BUSY_TIMESLOT + 1) ** 4 * (BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT + 1) ** 3

        self.action_space = ActionSpace((Discrete(BackscatterEnv4.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterEnv4.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterEnv4.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterEnv4.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT + 1)))

        self.observation_space = StateSpace((Discrete(SecondTransmitor.QUEUE), Discrete(SecondTransmitor.ENERGY),
                                             Discrete(SecondTransmitor.QUEUE), Discrete(SecondTransmitor.ENERGY),
                                             Discrete(SecondTransmitor.QUEUE), Discrete(SecondTransmitor.ENERGY),
                                             Discrete(SecondTransmitor.QUEUE), Discrete(SecondTransmitor.ENERGY)))

        # initialize Second Transmitters
        self.ST1 = SecondTransmitor(data_rate=0.5)
        self.ST2 = SecondTransmitor(data_rate=0.5)
        self.ST3 = SecondTransmitor(data_rate=0.5)
        self.ST4 = SecondTransmitor(data_rate=0.5)

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
        backscatter_time_2 = action[2]
        backscatter_time_3 = action[3]
        transmit_time_1 = action[4]
        transmit_time_2 = action[5]
        transmit_time_3 = action[6]
        backscatter_time_4 = BackscatterEnv4.BUSY_TIMESLOT - harvest - backscatter_time_1 - backscatter_time_2 - backscatter_time_3
        transmit_time_4 = BackscatterEnv4.TIME_FRAME - BackscatterEnv4.BUSY_TIMESLOT - transmit_time_1 - transmit_time_2 - transmit_time_3
        reward = 0
        if((backscatter_time_3 >= 0) and (transmit_time_3 >= 0)):
            harvest_time_1 = BackscatterEnv4.BUSY_TIMESLOT - backscatter_time_1
            harvest_time_2 = BackscatterEnv4.BUSY_TIMESLOT - backscatter_time_2
            harvest_time_3 = BackscatterEnv4.BUSY_TIMESLOT - backscatter_time_3
            harvest_time_4 = BackscatterEnv4.BUSY_TIMESLOT - backscatter_time_4

            reward += self.ST1.update(harvest_time_1, backscatter_time_1, transmit_time_1)
            reward += self.ST2.update(harvest_time_2, backscatter_time_2, transmit_time_2)
            reward += self.ST3.update(harvest_time_3, backscatter_time_3, transmit_time_3)
            reward += self.ST4.update(harvest_time_4, backscatter_time_4, transmit_time_4)

            throughtput = reward

            state = [self.ST1.queue, self.ST1.energy, self.ST2.queue, self.ST2.energy,
                     self.ST3.queue, self.ST3.energy, self.ST4.queue, self.ST4.energy]
            self.state = tuple(state)

        else:   # in case, assignment is not suitable
            reward = -10
            throughtput = 0
            self.ST1.generateData()
            self.ST2.generateData()
            self.ST3.generateData()
            self.ST4.generateData()
            print(np.array(self.state), reward, action)

        done = False
        # print(np.array(self.state), reward, done, {})
        return np.array(self.state), [reward, throughtput], done, {}

    def reset(self):
        self.state = []
        self.ST1.reset()
        self.ST2.reset()
        self.ST3.reset()
        self.ST4.reset()
        state = [self.ST1.queue, self.ST1.energy, self.ST2.queue, self.ST2.energy,
                 self.ST3.queue, self.ST3.energy, self.ST4.queue, self.ST4.energy]
        self.state = tuple(state)
        print(self.state)
        self.steps_beyond_done = None
        return np.array(self.state)

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