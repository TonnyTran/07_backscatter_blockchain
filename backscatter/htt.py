from backscatter_env import BackscatterEnv
from ST import SecondTransmitor
import xlwt
import random

TIME_FRAME = 10
BUSY_TIMESLOT = 6

version = "1.2"
nb_steps = 1000000
nb_max_episode_steps = 200

class HTTenv():
    def __init__(self):
        self.ST1 = SecondTransmitor(data_rate=0.5)
        self.ST2 = SecondTransmitor(data_rate=0.5)
        self.ST3 = SecondTransmitor(data_rate=0.5)

    def step(self):
        backscatter_time_1 = 0
        # transmit_time_1 = random.randint(0, TIME_FRAME - BUSY_TIMESLOT)
        transmit_time_1 = random.randint(0, TIME_FRAME - BUSY_TIMESLOT) / 3
        backscatter_time_2 = 0
        transmit_time_2 = random.randint(0, TIME_FRAME - BUSY_TIMESLOT) / 3
        backscatter_time_3 = 0
        transmit_time_3 = TIME_FRAME - BUSY_TIMESLOT - transmit_time_1 - transmit_time_2
        reward = 0
        if ((backscatter_time_2 >= 0) and (transmit_time_2 >= 0)):
            harvest_time_1 = BUSY_TIMESLOT
            harvest_time_2 = BUSY_TIMESLOT
            harvest_time_3 = BUSY_TIMESLOT

            reward += self.ST1.update(harvest_time_1, backscatter_time_1, transmit_time_1)
            reward += self.ST2.update(harvest_time_2, backscatter_time_2, transmit_time_2)
            reward += self.ST3.update(harvest_time_3, backscatter_time_3, transmit_time_3)

        # print reward
        return int(reward)

env = HTTenv()
step = 1
episode = 1
# open workbook to store result
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('DQN')
while (step < nb_steps -1):
    episode_reward = 0.0
    while ((step % nb_max_episode_steps) != 0):
        episode_reward += env.step()
        step += 1
    sheet.write(episode , 0, str(episode))
    sheet.write(episode , 1, str(episode_reward))
    print (episode, episode_reward)
    step += 1
    episode += 1
file_name = 'result_v' + version + '_htt'
workbook.save('../results/' + file_name + '.xls')