import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import random
import time
from time import sleep
import numpy as np
import math

from gameManager import *
from player_contoroller import *



class QLearning():
    def make_q_table():
        '''
        Qテーブルを作成する関数
        '''
        n_columns = 9
        n_rows = 3 ** 9
        return np.zeros((n_rows, n_columns))

    #===================================================================================================


    def q_learning(play_area, ai_input, reward, play_area_next, q_table, end_flg, eta=0.1, gamma=0.9):
        '''
        Qテーブルを更新する関数

        ゲームの状況をあらわすリスト・AIの行動・報酬
        1手番後のゲームの状況をあらわすリスト・Qテーブル・勝利フラグ
        を受け取り、更新したQテーブルを返す
        '''
        
        #行番号を取得
        row_index = QLearning.find_q_row(play_area)
        row_index_next = QLearning.find_q_row(play_area_next)
        column_index = ai_input - 1
        
        #勝利または敗北した場合
        if end_flg == 1:
            q_table[row_index, column_index] = q_table[row_index, column_index] + eta*(reward - q_table[row_index, column_index])
        else:
            q_table[row_index, column_index] = q_table[row_index, column_index] + eta*(reward + gamma*np.nanmax(q_table[row_index_next, :]) - q_table[row_index, column_index])
        
        return q_table
        
    #===================================================================================================
        
        
    def find_q_row(play_area):
        '''
        参照時の状況(state)が参照すべき行番号を計算する関数

        ゲームの状況をあらわすリストを受け取り、行番号を返す
        '''
        
        row_index = 0
        
        for index in range(len(play_area)):
            if play_area[index] == '○':
                coef = 1
            elif play_area[index] == '×':
                coef = 2
            else:
                coef = 0
            row_index += coef * (3 ** index)
            
        return row_index

    #===================================================================================================


    def get_ql_action(play_area, choosable_area, q_table, epsilon):
        '''
        Q学習に基づいて行動を選択する関数

        ゲームの状況をあらわすリストとQテーブルを受け取り、行動を返す
        '''
        
        #確率epsionでランダムに行動
        if np.random.rand() < epsilon:
            ai_input = int(random.choice(choosable_area))
            
        #Qテーブルを参照して最適な行動を選択
        else:
            row_index = QLearning.find_q_row(play_area)
            first_choice_flg = 1
            
            for choice in choosable_area:
                if first_choice_flg == 1:
                    ai_input = int(choice)
                    first_choice_flg = 0
                else:
                    if q_table[row_index, ai_input - 1] < q_table[row_index, int(choice) - 1]:
                        ai_input = int(choice)
                        
        return ai_input

    #===================================================================================================

    def save_q_table(q_table):
        '''
        Qテーブルを保存する関数
        '''
        np.save('q_table.npy', q_table)
        print('Qテーブルを保存しました')

#===================================================================================================

    def load_q_table(self, filename):
        '''
        Qテーブルを読み込む関数
        '''
        q_table = np.load(filename)
        print('Qテーブルを読み込みました')
        return q_table