import numpy as np
import random
from config import *
STATE_SPACE = (WIDTH//10 , HEIGHT//10 , 2, 2, HEIGHT//10)
ACTION_SPACE = 3

class AI:
    def __init__(self, is_A=True): #超級無敵重要: 預設是左邊拍子, 如果要右邊拍子, 要初始化要AI(False)
        self.q_table = np.zeros(STATE_SPACE + (ACTION_SPACE,))
        self.epsilon = EPSILON
        self.is_A = is_A  # 標誌，True 表示控制左側球拍（A），False 表示控制右側球拍（B）

    def discretize_state(self, state):
        # 根據 is_A 選擇正確的球拍位置
        paddle_y = state['paddle1_A_y'] if self.is_A else state['paddle1_B_y']
        return (
            min(int(state['ball_x'] // 100), (WIDTH//100)-1),
            min(int(state['ball_y'] // 100), (HEIGHT//100)-1),
            0 if state['ball_dx'] < 0 else 1,
            0 if state['ball_dy'] < 0 else 1,
            min(int(paddle_y // 100), (HEIGHT//100)-1)  # 使用選擇的球拍位置
        )

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice([0, 1, 2])
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + GAMMA * self.q_table[next_state][best_next_action]
        self.q_table[state][action] += ALPHA * (td_target - self.q_table[state][action])

    def decay_epsilon(self):
        if self.epsilon > EPSILON_MIN:
            self.epsilon *= EPSILON_DECAY