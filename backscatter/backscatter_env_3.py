import gym
from gym.utils import seeding
import numpy as np
from action_space import ActionSpace
from state_space import StateSpace
from gym.spaces import Discrete
from ST import SecondTransmitor
from mempool import Mempool, Transaction, Block
import random

class BackscatterBlockchainEnv3(gym.Env):

    # Network constants
    TIME_FRAME = 10
    BUSY_TIMESLOT = 9
    DATA_RATE = 0.4
    MAX_BACK = BUSY_TIMESLOT
    MAX_TRANS = TIME_FRAME - BUSY_TIMESLOT
    MAX_NB_ACT_BACK = (MAX_BACK + 1) * (MAX_BACK + 2) * (MAX_BACK + 3) / 6
    MAX_NB_ACT_TRANS = (MAX_TRANS + 1) * (MAX_TRANS + 2) * (MAX_TRANS + 3) / 6

    # Blockchain Constants
    SUCCESS_RATE = 3
    HASHRATE = 0.005

    def __init__(self):

        # System parameters
        self.nb_ST = 3
        self.state_size = 2 * self.nb_ST + Mempool.NB_FEE_INTERVALS
        self.nb_actions = BackscatterBlockchainEnv3.MAX_NB_ACT_BACK * BackscatterBlockchainEnv3.MAX_NB_ACT_TRANS

        # Blockchain parameters
        self.mempool = Mempool()
        self.userTransaction = Transaction(random.randint(0, Mempool.TRANSACTION_SIZE_CREATED))
        self.lastBlock = Block()
        self.hashRate = BackscatterBlockchainEnv3.HASHRATE
        self.doubleSpendSuccess = None

        # define action space
        self.action_space = ActionSpace((Discrete(BackscatterBlockchainEnv3.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterBlockchainEnv3.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterBlockchainEnv3.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterBlockchainEnv3.TIME_FRAME - BackscatterBlockchainEnv3.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterBlockchainEnv3.TIME_FRAME - BackscatterBlockchainEnv3.BUSY_TIMESLOT + 1),
                                         Discrete(BackscatterBlockchainEnv3.TIME_FRAME - BackscatterBlockchainEnv3.BUSY_TIMESLOT + 1)))

        # define state space
        self.observation_space = StateSpace((Discrete(SecondTransmitor.QUEUE), Discrete(SecondTransmitor.ENERGY),
                                             Discrete(SecondTransmitor.QUEUE), Discrete(SecondTransmitor.ENERGY),
                                             Discrete(SecondTransmitor.QUEUE), Discrete(SecondTransmitor.ENERGY),
                                             Discrete(Mempool.MAX_SIZE), Discrete(Mempool.MAX_SIZE),
                                             Discrete(Mempool.MAX_SIZE), Discrete(Mempool.MAX_SIZE),
                                             Discrete(Mempool.MAX_SIZE)))

        # initialize Second Transmitters
        self.ST1 = SecondTransmitor(data_rate=BackscatterBlockchainEnv3.DATA_RATE)
        self.ST2 = SecondTransmitor(data_rate=BackscatterBlockchainEnv3.DATA_RATE)
        self.ST3 = SecondTransmitor(data_rate=BackscatterBlockchainEnv3.DATA_RATE)

        self.viewer = None
        self.state = None
        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        self.reward = 0
        self.attacked = False
        data_transmitted = 0

        backscatter_time_1 = action[0]
        backscatter_time_2 = action[1]
        backscatter_time_3 = action[2]
        transmit_time_1 = action[3]
        transmit_time_2 = action[4]
        transmit_time_3 = action[5]
        harvest = BackscatterBlockchainEnv3.BUSY_TIMESLOT - backscatter_time_1 - backscatter_time_2 - backscatter_time_3
        idle_time = BackscatterBlockchainEnv3.TIME_FRAME - BackscatterBlockchainEnv3.BUSY_TIMESLOT - transmit_time_1 - transmit_time_2 - transmit_time_3

        queue1 = self.ST1.queue
        energy1 = self.ST1.energy
        queue2 = self.ST2.queue
        energy2 = self.ST2.energy
        queue3 = self.ST3.queue
        energy3 = self.ST3.energy
        if(harvest >= 0) and (idle_time >= 0):
            harvest_time_1 = BackscatterBlockchainEnv3.BUSY_TIMESLOT - backscatter_time_1
            harvest_time_2 = BackscatterBlockchainEnv3.BUSY_TIMESLOT - backscatter_time_2
            harvest_time_3 = BackscatterBlockchainEnv3.BUSY_TIMESLOT - backscatter_time_3

            # Step 1: data is transmitted to gateway
            data_transmitted += self.ST1.update(harvest_time_1, backscatter_time_1, transmit_time_1)
            data_transmitted += self.ST2.update(harvest_time_2, backscatter_time_2, transmit_time_2)
            data_transmitted += self.ST3.update(harvest_time_3, backscatter_time_3, transmit_time_3)

            # Step 2: User's transaction initialization
            self.userTransaction = Transaction(data_transmitted)
            self.userTransaction.estimateFeeRate(self.lastBlock)
            self.mempool.addTransaction(self.userTransaction)

            # Step 3: Mempool updates - some new transactions come
            self.mempool.generateNewTransactions()

            # Step 4: Miners start mining process, transactions which are included in Block will be removed from mempool
            self.lastBlock.mineBlock(self.mempool)
            transactionFee = self.userTransaction.data_size * self.userTransaction.feeRate

            # Step 5: Attack process
            self.doubleSpendSuccess = 2 * self.hashRate
            if np.random.rand() < self.doubleSpendSuccess:
                self.attacked = True

            # if user's transaction is successfully added in the block and not attacked -> reward success
            if self.userTransaction in self.lastBlock.blockTransaction and not self.attacked:
                self.reward = BackscatterBlockchainEnv3.SUCCESS_RATE * self.userTransaction.data_size - transactionFee
            else:
                self.reward = - transactionFee
                data_transmitted = 0

            # Step 6: environment is updated
            self.ST1.generateData()
            self.ST2.generateData()
            self.ST3.generateData()

            self.mempool.updateMempoolState()

            state = [self.ST1.queue, self.ST1.energy,
                     self.ST2.queue, self.ST2.energy,
                     self.ST3.queue, self.ST3.energy,
                     self.mempool.mempoolState[0], self.mempool.mempoolState[1],
                     self.mempool.mempoolState[2], self.mempool.mempoolState[3],
                     self.mempool.mempoolState[4]]
            self.state = tuple(state)

        else:   # in case, assignment is not suitable
            self.reward = -20
            data_transmitted = 0
            transactionFee = 0
            if (self.ST1.queue == SecondTransmitor.QUEUE and self.ST2.queue == SecondTransmitor.QUEUE
                and self.ST3.queue == SecondTransmitor.QUEUE):
                self.ST1.reset()
                self.ST2.reset()
                self.ST3.reset()
            else:
                self.ST1.generateData()
                self.ST2.generateData()
                self.ST3.generateData()
            state = [self.ST1.queue, self.ST1.energy,
                     self.ST2.queue, self.ST2.energy,
                     self.ST3.queue, self.ST3.energy,
                     self.mempool.mempoolState[0], self.mempool.mempoolState[1],
                     self.mempool.mempoolState[2], self.mempool.mempoolState[3],
                     self.mempool.mempoolState[4]]
            self.state = tuple(state)

        done = False
        # print(np.array(self.state), reward, done, {})
        return np.array(self.state), [self.reward, data_transmitted, transactionFee,
                                      queue1, energy1, BackscatterBlockchainEnv3.BUSY_TIMESLOT - backscatter_time_1,
                                      backscatter_time_1, transmit_time_1,
                                      queue2, energy2, BackscatterBlockchainEnv3.BUSY_TIMESLOT - backscatter_time_2,
                                      backscatter_time_2, transmit_time_2,
                                      queue3, energy3, BackscatterBlockchainEnv3.BUSY_TIMESLOT - backscatter_time_3,
                                      backscatter_time_3, transmit_time_3], done, {}

    def reset(self):
        self.state = []
        self.ST1.reset()
        self.ST2.reset()
        self.ST3.reset()
        self.mempool.resetMempool()
        state = [self.ST1.queue, self.ST1.energy,
                 self.ST2.queue, self.ST2.energy,
                 self.ST3.queue, self.ST3.energy,
                 self.mempool.mempoolState[0], self.mempool.mempoolState[1],
                 self.mempool.mempoolState[2], self.mempool.mempoolState[3],
                 self.mempool.mempoolState[4]]
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

# env = BackscatterEnv3()
# env.reset()
# for index in range(0, 1000):
#     env.step(env.action_space.sample())