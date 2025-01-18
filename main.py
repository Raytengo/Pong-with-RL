from environment import PongEnvironment
from ai import AI
from config import *
import numpy as np
import matplotlib.pyplot as plt

if DISPLAY:
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong AI Training")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

env = PongEnvironment()
AI_A = AI()
AI_B = AI(False) # 這邊要False, 因為預設訓練的是左邊的AI, 幹你娘因為這個東西卡超久

catch_counts_A = []  # 記錄 AI_A 接到球的次數
catch_counts_B = []  # 記錄 AI_B 接到球的次數

for episode in range(EPISODES):
    state = env.reset()
    done = False
    total_reward_A = total_reward_B = 0
    catch_count_A = 0  # 當前回合 AI_A 接到球的次數
    catch_count_B = 0  # 當前回合 AI_B 接到球的次數

    # 判斷是否需要顯示當前回合的畫面
    show_display = DISPLAY and (episode + 1) > round

    while not done:
        state_A = AI_A.discretize_state(state)
        action_A = AI_A.choose_action(state_A)

        state_B = AI_B.discretize_state(state)
        action_B = AI_B.choose_action(state_B)

        next_state, reward_A, reward_B, done = env.step(action_A, action_B)

        # 檢測是否接到球
        if reward_A == touch_point:  # AI_A 接到球
            catch_count_A += 1
        if reward_B == touch_point:  # AI_B 接到球
            catch_count_B += 1

        next_state_A = AI_A.discretize_state(next_state)
        AI_A.update_q_table(state_A, action_A, reward_A, next_state_A)
        next_state_B = AI_B.discretize_state(next_state)
        AI_B.update_q_table(state_B, action_B, reward_B, next_state_B)

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

    AI_A.decay_epsilon()
    AI_B.decay_epsilon()

    # 記錄當前回合的接到球次數
    catch_counts_A.append(catch_count_A)
    catch_counts_B.append(catch_count_B)

    print(f'Episode: {episode + 1}, Catch Count A: {catch_count_A}, Catch Count B: {catch_count_B}')

if DISPLAY:
    pygame.quit()

np.save("q_table_A.npy", AI_A.q_table)
np.save("q_table_A(right).npy", AI_B.q_table)

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