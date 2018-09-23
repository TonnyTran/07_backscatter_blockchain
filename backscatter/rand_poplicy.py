from backscatter_env import BackscatterEnv
from ST import SecondTransmitor
import xlwt
import random
import numpy as np

TIME_FRAME = 10
BUSY_TIMESLOT = 1
DATA_RATE = 0.3

version = "3_01"
nb_steps = 10000
nb_max_episode_steps = 200

class RANDenv():
    def __init__(self):
        self.ST1 = SecondTransmitor(data_rate=DATA_RATE)
        self.ST2 = SecondTransmitor(data_rate=DATA_RATE)
        self.ST3 = SecondTransmitor(data_rate=DATA_RATE)

    def step(self):
        backscatter_time_1 = random.randint(0, BUSY_TIMESLOT)
        transmit_time_1 = random.randint(0, TIME_FRAME - BUSY_TIMESLOT)
        backscatter_time_2 = random.randint(0, BUSY_TIMESLOT - backscatter_time_1)
        transmit_time_2 = random.randint(0, TIME_FRAME - BUSY_TIMESLOT - transmit_time_1)
        backscatter_time_3 = random.randint(0, BUSY_TIMESLOT - backscatter_time_1 - backscatter_time_2)
        transmit_time_3 = random.randint(0, TIME_FRAME - BUSY_TIMESLOT - transmit_time_1 - transmit_time_2)

        reward = 0
        if ((backscatter_time_2 >= 0) and (transmit_time_2 >= 0)):
            harvest_time_1 = BUSY_TIMESLOT - backscatter_time_1
            harvest_time_2 = BUSY_TIMESLOT - backscatter_time_2
            harvest_time_3 = BUSY_TIMESLOT - backscatter_time_3

            reward += self.ST1.update(harvest_time_1, backscatter_time_1, transmit_time_1)
            reward += self.ST2.update(harvest_time_2, backscatter_time_2, transmit_time_2)
            reward += self.ST3.update(harvest_time_3, backscatter_time_3, transmit_time_3)
            datawaiting_before = self.ST1.queue
            self.ST1.generateData()
            self.ST2.generateData()
            self.ST3.generateData()
            datawaiting = self.ST1.queue

        # print reward
        return [reward, datawaiting_before, datawaiting]

env = RANDenv()
step = 1
episode = 1
# open workbook to store result
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('DQN')
while (step < nb_steps -1):
    episode_reward = np.float32(0)
    while ((step % nb_max_episode_steps) != 0):
        episode_reward += env.step()
        step += 1
    sheet.write(episode, 0, str(episode))
    sheet.write(episode, 1, str(episode_reward[0]))
    sheet.write(episode, 2, str(episode_reward[1]))
    sheet.write(episode, 3, str(episode_reward[2]))
    print (episode, episode_reward)
    step += 1
    episode += 1
file_name = 'result_v' + version + '_rand'
workbook.save('../results/' + file_name + '.xls')