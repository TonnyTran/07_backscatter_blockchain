import random
import numpy as np
import math


# Mempool stores all unconfirmed transactions.
# Mempool is public for all people
class Mempool():
    DEFAUT_FEE_RATE = 0.05
    MAX_FEE_RATE = 1.0
    NB_FEE_INTERVALS = 5
    MAX_SIZE = 50       # capacity of data units
    BLOCK_SIZE = 30     # data units
    NB_TRANSACTION_CREATED = 7
    TRANSACTION_SIZE_CREATED = 5

    def __init__(self):
        self.listTransactions = []
        self.mempoolSize = 0
        self.fee_interval = Mempool.MAX_FEE_RATE / Mempool.NB_FEE_INTERVALS
        self.mempoolState = np.zeros((Mempool.NB_FEE_INTERVALS,), dtype=int)

    def resetMempool(self):
        self.listTransactions = []
        self.mempoolSize = 0
        self.generateNewTransactions()
        self.updateMempoolState()

    def updateMempoolState(self):
        self.mempoolState = np.zeros((Mempool.NB_FEE_INTERVALS,), dtype=int)
        for transaction in self.listTransactions:
            category = int(math.floor(transaction.feeRate / self.fee_interval))
            self.mempoolState[category] += transaction.data_size

    def sortMempool(self):
        self.listTransactions.sort(key=lambda transaction: transaction.feeRate, reverse=True)

    def generateNewTransactions(self):
        for index in range(0, Mempool.NB_TRANSACTION_CREATED):
            newTransaction = Transaction(random.randint(1, Mempool.TRANSACTION_SIZE_CREATED))
            if self.mempoolSize + newTransaction.data_size < Mempool.MAX_SIZE:
                self.listTransactions.append(newTransaction)
                self.mempoolSize += newTransaction.data_size

    def addTransaction(self, transaction):
        self.listTransactions.append(transaction)
        self.mempoolSize += transaction.data_size

# define transaction
class Transaction():
    def __init__(self, data_size):
        self.feeRate = np.random.uniform(Mempool.DEFAUT_FEE_RATE, Mempool.MAX_FEE_RATE)
        self.data_size = data_size

    def estimateFeeRate(self, lastBlock):
        totalFee = 0
        if lastBlock.blockSize != 0:
            for transaction in lastBlock.blockTransaction:
                totalFee += transaction.data_size * transaction.feeRate
            self.feeRate = totalFee / lastBlock.blockSize
        else:
            self.feeRate = np.random.uniform(Mempool.DEFAUT_FEE_RATE, Mempool.MAX_FEE_RATE)

class Block():
    def __init__(self):
        self.blockTransaction = []
        self.blockSize = 0

    def mineBlock(self, mempool):
        self.blockTransaction = []
        self.blockSize = 0
        mempool.sortMempool()
        while mempool.mempoolSize != 0 and self.blockSize + mempool.listTransactions[0].data_size < Mempool.BLOCK_SIZE:
            self.addTransaction(mempool.listTransactions[0])
            mempool.mempoolSize = mempool.mempoolSize - mempool.listTransactions[0].data_size
            del mempool.listTransactions[0]

    def addTransaction(self, transaction):
        self.blockTransaction.append(transaction)
        self.blockSize += transaction.data_size

# #
# mempool = Mempool()
# mempool.resetMempool()
# mempool.sortMempool()
# for transaction in mempool.listTransactions:
#     print (str(transaction.feeRate) + "----" + str(transaction.data_size))
# mempool.updateMempoolState()
# lastBlock = Block()
# currentTransaction = Transaction(random.randint(1, Mempool.TRANSACTION_SIZE_CREATED))
# for index in range(0, 100):
#     print("------------------------------------")
#     print("Mempool size: " + str(mempool.mempoolSize))
#     lastBlock.mineBlock(mempool)
#     print("Block size: " + str(lastBlock.blockSize))
#     print("Mempool size: " + str(mempool.mempoolSize))
#     for transaction in lastBlock.blockTransaction:
#         print (str(transaction.feeRate) + "----" + str(transaction.data_size))
#     if currentTransaction in lastBlock.blockTransaction:
#         print("Yesssss")
#     else:
#         print("nooooo")
#     currentTransaction = Transaction(random.randint(0, Mempool.TRANSACTION_SIZE_CREATED))
#     currentTransaction.estimateFeeRate(lastBlock)
#     print ("new transaction:" + str(currentTransaction.feeRate) + "----" + str(currentTransaction.data_size))
#     mempool.generateNewTransactions()
#     mempool.listTransactions.append(currentTransaction)
#     mempool.mempoolSize += currentTransaction.data_size
#     print("Mempool size: " + str(mempool.mempoolSize))
#     mempool.updateMempoolState()
#     print(mempool.mempoolState)
# print(mempool.mempoolState)