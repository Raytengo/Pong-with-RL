import numpy as np
from config import *

class PongEnvironment:
    def __init__(self):       
        self.acceleration = 0
        self.score_A = 0
        self.score_B = 0
        self.collision_cooldown = 0  # 初始化碰撞冷却时间
        self.reset()

    def reset(self):
        self.ball_x = WIDTH // 2
        self.ball_y = np.random.randint(int(HEIGHT)//2 - 50, int(HEIGHT)//2 + 50)
        self.ball_dx = BALL_SPEED * np.random.choice([-1, 1])
        self.ball_dy = (BALL_SPEED-5) * np.random.choice([-1, 1])
        self.paddle1_A_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.paddle1_B_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.acceleration = ACCELERATION
        self.collision_cooldown = 0  # 重置冷却时间
        return self.get_state()
    
    def get_state(self):
        return {
            'ball_x': self.ball_x,
            'ball_y': self.ball_y,
            'ball_dx': self.ball_dx,
            'ball_dy': self.ball_dy,
            'paddle1_A_y': self.paddle1_A_y,
            'paddle1_B_y': self.paddle1_B_y,
            'score_A': self.score_A,
            'score_B': self.score_B
        }
    
    def step(self, action_A, action_B):
        reward_A = reward_B = 0
        done = False

        # 更新碰撞冷卻時間
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

        # 更新球拍位置
        if action_A == 1 and self.paddle1_A_y > 0:
            self.paddle1_A_y = max(self.paddle1_A_y - PADDLE_SPEED, 0)
            reward_A -= MOVE
        elif action_A == 0 and self.paddle1_A_y < HEIGHT - PADDLE_HEIGHT:
            self.paddle1_A_y = min(self.paddle1_A_y + PADDLE_SPEED, HEIGHT - PADDLE_HEIGHT)
            reward_A -= MOVE

        if action_B == 1 and self.paddle1_B_y > 0:
            self.paddle1_B_y = max(self.paddle1_B_y - PADDLE_SPEED, 0)
            reward_B -= MOVE
        elif action_B == 0 and self.paddle1_B_y < HEIGHT - PADDLE_HEIGHT:
            self.paddle1_B_y = min(self.paddle1_B_y + PADDLE_SPEED, HEIGHT - PADDLE_HEIGHT)
            reward_B -= MOVE

        # 更新球的位置
        self.ball_x += self.ball_dx 
        self.ball_y += self.ball_dy
        

        # 球與上下牆壁的碰撞
        if self.ball_y <= 0:
            self.ball_dy = abs(self.ball_dy)
        elif self.ball_y >= HEIGHT:
            self.ball_dy = -abs(self.ball_dy)

        # 改進的球拍碰撞檢測
        if self.collision_cooldown == 0:
            # 左側球拍碰撞檢測
            if (self.ball_x <= 50 + PADDLE_WIDTH and  # 球在左側球拍範圍內
                self.paddle1_A_y <= self.ball_y <= self.paddle1_A_y + PADDLE_HEIGHT and  # 球在球拍高度範圍內
                self.ball_dx < 0):  # 球從右側（正面）接觸球拍
                self.ball_dx = abs(self.ball_dx)  # 反彈
                self.ball_dx *= self.acceleration
                offset = (self.ball_y - (self.paddle1_A_y + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2)
                self.ball_dy = offset * SPIN_FACTOR
                reward_A = touch_point  # AI_A 接到球
                self.collision_cooldown = 12  # 設置冷卻時間

            # 右側球拍碰撞檢測
            elif (self.ball_x >= WIDTH - 50 - PADDLE_WIDTH - BALL_RADIUS * 2 and  # 球在右側球拍範圍內
                self.paddle1_B_y <= self.ball_y <= self.paddle1_B_y + PADDLE_HEIGHT and  # 球在球拍高度範圍內
                self.ball_dx > 0):  # 球從左側（正面）接觸球拍
                self.ball_dx = -abs(self.ball_dx)  # 反彈
                self.ball_dx *= self.acceleration
                offset = (self.ball_y - (self.paddle1_B_y + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2)
                self.ball_dy = offset * SPIN_FACTOR
                reward_B = touch_point  # AI_B 接到球
                self.collision_cooldown = 12  # 設置冷卻時間

        # 球出界
        if self.ball_x <= 0:
            self.score_B += 1
            reward_A = lost_point
            reward_B = get_point
            done = True
        elif self.ball_x >= WIDTH:
            self.score_A += 1
            reward_A = get_point
            reward_B = lost_point
            done = True

        return self.get_state(), reward_A, reward_B, done