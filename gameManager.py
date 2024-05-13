import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import random
import time
from time import sleep
import numpy as np
import math

from Q_Learning import QLearning
from player_contoroller import get_input



class gameManager(QLearning, get_input):
    
    
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
        gameManager.show_play(play_area)
        inputter_count = first_inputter
        end_flg = 0
        while True:
            if (inputter_count % 2) == 1:
                print('Your turn!')
                play_area, player_input = QLearning.get_player_input(play_area, first_inputter)
                gameManager.show_play(play_area, inputter1, player_input)
                winner, end_flg = gameManager.judge(play_area, inputter1)
                if end_flg:
                    break
            elif (inputter_count % 2) == 0:
                print('AI\'s turn!\n.\n.\n.')
                play_area, ai_input = QLearning.get_AI_input(play_area, first_inputter, mode=0)
                sleep(3)
                gameManager.show_play(play_area, inputter2, ai_input)
                winner, end_flg = gameManager.judge(play_area, inputter2)
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

    def randomAI_vs_QLAI(first_inputter, q_table, epsilon=0):
        """
        AI(ランダム)とAI(Q学習)のゲームを実行する関数

        先手(1:AI(ランダム)、2:AI(Q学習))とQテーブルを受け取り、
        ゲームが終了するまで実行する
        """
        inputter1 = 'Random AI'
        inputter2 = 'QL AI'

        # Q学習退避用
        ql_input_list = []
        play_area_list = []

        play_area = list(range(1, 10))
        #show_play(play_area)
        inputter_count = first_inputter
        end_flg = 0
        ql_flg = 0
        reward = 0
        while True:
            # Q学習退避用
            play_area_tmp = play_area.copy()
            play_area_list.append(play_area_tmp)
            # Q学習実行フラグ
            ql_flg = 0
            # AI(Q学習)の手番
            if (inputter_count % 2) == 0:
                # QL AI入力
                play_area, ql_ai_input = get_input.get_AI_input(play_area, 
                                                    first_inputter,
                                                    mode=1, 
                                                    q_table=q_table, 
                                                    epsilon=epsilon)
                winner, end_flg = gameManager.judge(play_area, inputter2)
                # Q学習退避用
                ql_input_list.append(ql_ai_input)            
                # 勝利した場合
                if winner == inputter2:
                    reward = 1
                    ql_flg = 1
                play_area_before = play_area_list[-1]
                ql_ai_input_before = ql_input_list[-1]
            # AI(ランダム)の手番
            elif (inputter_count % 2) == 1:
                play_area, random_ai_input = get_input.get_AI_input(play_area, 
                                                        first_inputter+1, 
                                                        mode=0)
                winner, end_flg = gameManager.judge(play_area, inputter1)
                # AI(ランダム)が先手の場合の初手以外は学習
                if inputter_count != 1:
                    ql_flg = 1
            # Q学習実行
            if ql_flg == 1:
                ql_ai_input_before = ql_input_list[-1]
                q_table = QLearning.q_learning(play_area_before, ql_ai_input_before,
                                    reward, play_area, q_table, end_flg)
            if end_flg:
                break
            inputter_count += 1
        print('{} win!!!'.format(winner))
        return winner, q_table


    #===================================================================================================

    def player_vs_QLAI(self, first_inputter, q_table, epsilon = 0):
        """
        プレイヤーとAI(Q学習)のゲームを実行する関数

        先手(1:プレイヤー)、2:AI(Q学習))を受け取り、ゲームが終了するまで実行する
        """
        inputter1 = 'YOU'
        inputter2 = 'QL AI'

        # Q学習退避用
        ql_input_list = []
        play_area_list = []

        play_area = list(range(1, 10))
        
        gameManager.show_play(play_area)
        inputter_count = first_inputter
        end_flg = 0
        ql_flg = 0
        reward = 0
        while True:
            # Q学習退避用
            play_area_tmp = play_area.copy()
            play_area_list.append(play_area_tmp)
            # Q学習実行フラグ
            ql_flg = 0
            # AI(Q学習)の手番
            if (inputter_count % 2) == 0:
                # QL AI入力
                play_area, ql_ai_input = get_input.get_AI_input(play_area, 
                                                    first_inputter,
                                                    mode=1, 
                                                    q_table=q_table, 
                                                    epsilon=epsilon)
                gameManager.show_play(play_area, inputter2, ql_ai_input)
                winner, end_flg = gameManager.judge(play_area, inputter2)
                # Q学習退避用
                ql_input_list.append(ql_ai_input)            
                # 勝利した場合
                if winner == inputter2:
                    reward = 1
                    ql_flg = 1
                play_area_before = play_area_list[-1]
                ql_ai_input_before = ql_input_list[-1]
            # プレイヤーの手番
            elif (inputter_count % 2) == 1:
                print('Your turn!')
                # プレイヤーの入力受付
                play_area, player_input = get_input.get_player_input(play_area, first_inputter)
                gameManager.show_play(play_area, inputter1, player_input)
                winner, end_flg = gameManager.judge(play_area, inputter1)
                # プレイヤーが勝利した場合
                if winner == inputter1:
                    reward = -1
                # プレイヤーが先手の場合の初手以外は学習
                if inputter_count != 1:
                    ql_flg = 1
            # Q学習実行
            if ql_flg == 1:
    #            print('Q学習')
                ql_ai_input_before = ql_input_list[-1]
                q_table = QLearning.q_learning(play_area_before, ql_ai_input_before,
                                    reward, play_area, q_table, end_flg)
            if end_flg:
                break
            inputter_count += 1
        gameManager.show_play(play_area)
        print('{} win!!!'.format(winner))
        sleep(1)
        return winner, q_table
    
    #===================================================================================================
    
    def player_vs_player(first_inputter):
        """
        プレイヤーとプレイヤーのゲームを実行する関数

        先手(1:プレイヤー1、2:プレイヤー2)を受け取り、ゲームが終了するまで実行する
        """
        inputter1 = 'Player1'
        inputter2 = 'Player2'

        play_area = list(range(1, 10))
        gameManager.show_play(play_area)
        inputter_count = first_inputter
        end_flg = 0
        while True:
            if (inputter_count % 2) == 1:
                print('Player1\'s turn!')
                play_area, player_input = QLearning.get_player_input(play_area, first_inputter)
                gameManager.show_play(play_area, inputter1, player_input)
                winner, end_flg = gameManager.judge(play_area, inputter1)
                if end_flg:
                    break
            elif (inputter_count % 2) == 0:
                print('Player2\'s turn!')
                play_area, player_input = QLearning.get_player_input(play_area, first_inputter+1)
                gameManager.show_play(play_area, inputter2, player_input)
                winner, end_flg = gameManager.judge(play_area, inputter2)
                if end_flg:
                    break
            inputter_count += 1
        print('{} win!!!'.format(winner))