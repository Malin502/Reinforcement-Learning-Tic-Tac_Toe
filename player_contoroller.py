import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import random
import time
from time import sleep
import numpy as np
import math
import pygame
import sys



class get_input():

    def get_player_input(play_area, first_inputter):
        '''
        プレイヤーから入力を受け付ける関数
        '''
        choosable_area = [str(area) for area in play_area if type(area) is int]
        player_input = None  # 初期値を設定
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = x // 100
                    row = y // 100
                    player_input = row * 3 + col + 1
                    if str(player_input) in choosable_area:
                        break
            if player_input is not None and str(player_input) in choosable_area:
                break
        if first_inputter % 2 == 1:
            play_area[play_area.index(player_input)] = '○'
        elif first_inputter % 2 == 0:
            play_area[play_area.index(player_input)] = '×'
        return play_area, player_input
        
    #===================================================================================================
        
        
    #mode 0: ランダム, mode 1: Q学習
    def get_AI_input(play_area, first_inputter, mode = 1, q_table=None, epsilon=0):
        '''
        AIに入力を受け取る関数
        
        ゲームの状況をあらわすリストとAIのモードおよびその他のオプションを受け取り、
        AIの入力で更新したリストと入力を返す
        '''
        
        choosable_area = [str(area) for area in play_area if type(area) is int]
        if mode == 0:
            AI_input = random.choice(choosable_area)
            
        elif mode == 1:
            
            from Q_Learning import QLearning
            
            AI_input = QLearning.get_ql_action(play_area, choosable_area, q_table, epsilon)
            
        if first_inputter % 2 == 1:
            play_area[int(AI_input) - 1] = '×'
        elif first_inputter % 2 == 0:
            play_area[int(AI_input) - 1] = '○'
            
        return play_area, AI_input