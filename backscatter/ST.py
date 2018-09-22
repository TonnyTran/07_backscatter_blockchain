import random

class SecondTransmitor():
    QUEUE = 10
    ENERGY = 5
    def __init__(self, energy_harvest=1, data_backscatter=1, energy_transmit=1, data_transmit=2, data_rate=0.5):
        self.queue = random.randint(0, SecondTransmitor.QUEUE)
        self.energy = random.randint(0, SecondTransmitor.ENERGY)

        self.energy_harvest = energy_harvest
        self.data_backscatter = data_backscatter
        self.energy_transmit = energy_transmit
        self.data_transmit=data_transmit
        self.data_rate = data_rate

    def update(self, harvest_time, backscatter_time, transmit_time):
        throughtput = 0
        # harvest phase
        self.energy += harvest_time * self.energy_harvest
        self.energy = min(self.energy, SecondTransmitor.ENERGY)

        # backscatter phase
        backscatter_time = min(backscatter_time, self.queue/self.data_backscatter)
        data_transfer = backscatter_time * self.data_backscatter

        # if data_successful_ rate = 0.9
        t = data_transfer
        for i in range(0, t):
            if (random.uniform(0,1) > 0.9):
                data_transfer -= 1

        throughtput += data_transfer
        self.queue -= data_transfer

        # transmit phase
        transmit_time = min(transmit_time, self.queue/self.data_transmit, self.energy/self.energy_transmit)
        data_transfer = transmit_time * self.data_transmit
        energy_lose = transmit_time * self.energy_transmit

        # if data_successful_ rate = 0.9
        t = data_transfer
        for i in range(0, t):
            if (random.uniform(0, 1) > 0.9):
                data_transfer -= 1

        self.queue -= data_transfer
        self.energy -= energy_lose
        throughtput += data_transfer
        self.generateData()

        # return number of data transferred
        return throughtput

    def generateData(self):
        # generate data
        nb_data = 0
        for i in range(10):
            if (random.uniform(0, 1) < self.data_rate):
                nb_data += 1
        self.queue = min(SecondTransmitor.QUEUE, self.queue + nb_data)

    def reset(self):
        self.queue = random.randint(0, SecondTransmitor.QUEUE)
        self.energy = random.randint(0, SecondTransmitor.ENERGY)