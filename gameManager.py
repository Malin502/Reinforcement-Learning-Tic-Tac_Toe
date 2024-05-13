import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import random
import time
from time import sleep
import numpy as np
import math


class gameManager:
    
    
    def show_play(play_area, inputter=0, inputted=0):
        
        '''
        TIC TAC TOEの画面を表示する関数

        表示すべきリスト(1～9の数値、○、×から成る)と
        直前の入力者および入力を受け取り、表示する
        '''
    
        print('=====================')
        for i in range(0, 9, 3): # 0, 3, 6が格納される
            print('|', play_area[i], '|', play_area[i + 1], '|', play_area[i + 2], '|')
            print('---------------------')
            
        if inputter != 0:
            print('{} choose {}'.format(inputter, inputted))
        print('===================== \n')
    
    
#===================================================================================================
    
def judge(play_area, inputter):
    '''
    ゲーム終了及び勝者を判定する

    ゲームの状況をあらわすリストと直前の入力者を受け取り、
    ゲームが終了していれば勝者と終了判定を返す
    '''
    
    end_flg = 0
    winner = "NOBODY"
    
    first_list = [0, 3, 6, 0, 1, 2, 0, 2]
    second_list = [1, 4, 7, 3, 4, 5, 4, 4]
    third_list = [2, 5, 8, 6, 7, 8, 8, 6]
    
    for first, second, third in zip(first_list, second_list, third_list):
        if play_area[first] == play_area[second] == play_area[third]:
            
            winner = inputter
            end_flg = 1
            break
    
    choosable_area = [str(area) for area in play_area if type(area) is int]
    if len(choosable_area) == 0 :
        end_flg = 1
        
    return winner, end_flg
            
       
       #===================================================================================================
       
            
def player_vs_randomAI(first_inputter):
    """
    プレイヤーとAI(ランダム)のゲームを実行する関数

    先手(1:プレイヤー、2:AI)を受け取り、ゲームが終了するまで実行する
    """
    inputter1 = 'YOU'
    inputter2 = 'AI'

    play_area = list(range(1, 10))
    show_play(play_area)
    inputter_count = first_inputter
    end_flg = 0
    while True:
        if (inputter_count % 2) == 1:
            print('Your turn!')
            play_area, player_input = get_player_input(play_area, first_inputter)
            show_play(play_area, inputter1, player_input)
            winner, end_flg = judge(play_area, inputter1)
            if end_flg:
                break
        elif (inputter_count % 2) == 0:
            print('AI\'s turn!\n.\n.\n.')
            play_area, ai_input = get_AI_input(play_area, first_inputter, mode=0)
            sleep(3)
            show_play(play_area, inputter2, ai_input)
            winner, end_flg = judge(play_area, inputter2)
            if end_flg:
                break
        inputter_count += 1
        
    print('{} win!!!'.format(winner))
    
    
    
def make_q_table():
    '''
    Qテーブルを作成する関数
    '''
    n_columns = 9
    n_rows = 3 ** 9
    return np.zeros((n_rows, n_columns))

#===================================================================================================