import pygame
from environment import PongEnvironment
from ai import AI
import numpy as np
import time
from config import *

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("乒乓球遊戲 - AI vs 玩家")

# 初始化環境和 AI
env = PongEnvironment()
AI_A = AI()

try:
    AI_A.q_table = np.load("q_table_A.npy")
    print("Q-Table successfully loaded.")
except:
    print("No pre-trained Q-table found. Using new AI.")

AI_A.epsilon = 0 # 關閉探索,很重要

# 初始化遊戲變數
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
state = env.reset()
start_time = time.time()
round_time = 0
running = True
# 遊戲主循環
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 玩家控制
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and env.paddle1_B_y < (HEIGHT - PADDLE_HEIGHT):
        action_B = 0  # 向下
    elif keys[pygame.K_UP] and env.paddle1_B_y > 0:
        action_B = 1  # 向上
    else:
        action_B = 2  # 不動
    
    
    
    
    # AI 控制
    state_A = AI_A.discretize_state(state)
    action_A = AI_A.choose_action(state_A)
    
    # 更新遊戲狀態
    state, reward_A, reward_B, done = env.step(action_A, action_B)
    
    # 如果回合結束
    if done:
        round_time = time.time() - start_time
        print(f"Round Time: {round_time:.2f} seconds")
        state = env.reset()
        start_time = time.time()
        time.sleep(1)
    
    # 繪製畫面
    screen.fill(BLACK)
    
    # 球拍
    pygame.draw.rect(screen, WHITE, (50, env.paddle1_A_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - 70, env.paddle1_B_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # 球
    pygame.draw.ellipse(screen, WHITE, (env.ball_x, env.ball_y, BALL_RADIUS*2, BALL_RADIUS*2))
    
    # 中場線
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    # 分數顯示
    score_text = font.render(f"{env.score_A} - {env.score_B}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - 50, 20))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()