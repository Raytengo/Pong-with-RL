from environment import PongEnvironment
from ai import AI
from config import *
import numpy as np
import matplotlib.pyplot as plt

if DISPLAY:
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong AI Training - AI_A vs Tracking AI")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

env = PongEnvironment()
AI_A = AI()  # 左側球拍，使用 Q-learning 訓練
AI_B = AI()  # 右側球拍，使用追蹤球 AI 作為教練

# 加載訓練好的 Q 表（如果有的話）
try:
    AI_A.q_table = np.load("q_table_A.npy")
    print("Q-Table for AI_A successfully loaded.")
except:
    print("No pre-trained Q-table found for AI_A. Using new AI.")

AI_A.epsilon = EPSILON  # 設置 AI_A 的探索率
AI_B.epsilon = 0  # 追蹤球 AI 不需要探索

catch_counts_A = []  # 記錄 AI_A 接到球的次數
catch_counts_B = []  # 記錄 AI_B 接到球的次數

for episode in range(EPISODES2):
    state = env.reset()
    done = False
    total_reward_A = total_reward_B = 0
    catch_count_A = 0  # 當前回合 AI_A 接到球的次數
    catch_count_B = 0  # 當前回合 AI_B 接到球的次數

    # 判斷是否需要顯示當前回合的畫面
    show_display = DISPLAY and (episode + 1) > round2

    while not done:
        # AI_A 控制左側球拍
        state_A = AI_A.discretize_state(state)
        action_A = AI_A.choose_action(state_A)

        # 追蹤球 AI 控制右側球拍
        if state['ball_dx'] > 0:  # 只有當球向右時，追蹤球 AI 才會移動
            if state['ball_y'] > state['paddle1_B_y'] + PADDLE_HEIGHT / 2 + 10:  # 球在球拍下方
                action_B = 0  # 向下
            elif state['ball_y'] < state['paddle1_B_y'] + PADDLE_HEIGHT / 2 - 10:  # 球在球拍上方
                action_B = 1  # 向上
            else:
                action_B = 2  # 不動
        else:
            action_B = 2  # 球向左時，追蹤球 AI 不動

        # 更新遊戲狀態
        next_state, reward_A, reward_B, done = env.step(action_A, action_B)

        # 檢測是否接到球
        if reward_A == touch_point:  # AI_A 接到球
            catch_count_A += 1
        if reward_B == touch_point:  # AI_B 接到球
            catch_count_B += 1

        # 更新 AI_A 的 Q 表
        next_state_A = AI_A.discretize_state(next_state)
        AI_A.update_q_table(state_A, action_A, reward_A, next_state_A)

        total_reward_A += reward_A
        total_reward_B += reward_B
        state = next_state

        if show_display:
            # 清空屏幕
            screen.fill(BLACK)

            # 繪製球拍
            pygame.draw.rect(screen, WHITE, (50, env.paddle1_A_y, PADDLE_WIDTH, PADDLE_HEIGHT))  # 左側球拍
            pygame.draw.rect(screen, WHITE, (WIDTH - 70, env.paddle1_B_y, PADDLE_WIDTH, PADDLE_HEIGHT))  # 右側球拍

            # 繪製球
            pygame.draw.ellipse(screen, WHITE, (env.ball_x, env.ball_y, BALL_RADIUS * 2, BALL_RADIUS * 2))

            # 繪製中界線
            pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

            # 顯示比分
            score_text = font.render(f"Score: {env.score_A} - {env.score_B}", True, WHITE)
            screen.blit(score_text, (20, 10))  # 在左上角顯示比分

            # 顯示當前回合數
            episode_text = font.render(f"Episode: {episode + 1}", True, WHITE)
            screen.blit(episode_text, (WIDTH - 200, 10))  # 在右上角顯示回合數

            # 更新屏幕
            pygame.display.flip()
            pygame.event.pump()
            clock.tick(FPS)

    # 衰減 AI_A 的探索率
    AI_A.decay_epsilon()

    # 記錄當前回合的接到球次數
    catch_counts_A.append(catch_count_A)
    catch_counts_B.append(catch_count_B)

    print(f'Episode: {episode + 1}, Catch Count A: {catch_count_A}, Catch Count B: {catch_count_B}')

if DISPLAY:
    pygame.quit()

# 保存 AI_A 的 Q 表
np.save("q_table_B.npy", AI_A.q_table)

# 繪製折線圖
plt.figure(figsize=(10, 5))
plt.plot(catch_counts_A, label="AI_A Catch Count", linestyle='-', color='blue')  # AI_A 接到球的次數
plt.plot(catch_counts_B, label="AI_B Catch Count", linestyle='-', color='red')   # AI_B 接到球的次數
plt.xlabel("Episode")
plt.ylabel("Catch Count")
plt.title("AI_A and AI_B Catch Count Over Episodes")
plt.legend()
plt.grid(True)
plt.show()