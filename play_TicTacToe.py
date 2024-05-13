import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import random
import time
from time import sleep
import numpy as np
import math

from gameManager import *
from player_contoroller import *
from Q_Learning import *

eta = 0.1  # 学習率
gamma = 0.9  # 時間割引率
initial_epsilon = 0.5  # ε-greedy法の初期値

# ランダム vs QL(学習)
# 試行数設定
'''episode = 1000000
winner_list = []
start = time.time()
for i in range(episode):
    epsilon = initial_epsilon * (episode-i) / episode
    winner, q_table = randomAI_vs_QLAI(1, q_table, epsilon)
    winner_list.append(winner)
    
save_q_table(q_table)
elapsed_time = time.time() - start


print ('elapsed_time:{0}'.format(elapsed_time) + '[sec]')


print('勝ち回数')
print('Random AI:{}'.format(winner_list.count('Random AI')))
print('QL AI    :{}'.format(winner_list.count('QL AI')))
print('NOBODY   :{}'.format(winner_list.count('NOBODY')))
print('QLの勝率 :{}'.format(winner_list.count('QL AI') / len(winner_list)))'''

# プレイヤー vs QL
# 試行数設定
episode = 1
winner_list = []

Q_Learning = QLearning()
playerController = get_input()
GameManager = gameManager()

q_table = QLearning.make_q_table()

q_table = Q_Learning.load_q_table('q_table.npy')

for i in range(episode):
    epsilon = initial_epsilon * (episode-i) / episode
    winner, q_table = GameManager.player_vs_QLAI(2, q_table, epsilon)
    winner_list.append(winner)