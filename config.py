# Gaming Settings
WIDTH = 800
HEIGHT = 600
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
BALL_RADIUS = 10
BALL_SPEED = 7  # 初始速度
PADDLE_SPEED = 12
DISPLAY = True  # 设为True时显示游戏画面
# 新增的游戲設置
ACCELERATION = 1.01  # 球速加速度
SPIN_FACTOR = 7  # 撞擊偏移係數
FPS = 120

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Q-Learning Settings
ALPHA = 0.1 
GAMMA = 0.9 
EPSILON = 1.0 
EPSILON_DECAY = 0.995 
EPSILON_MIN = 0.01 
EPISODES = 20000
EPISODES2 = 5000
round = EPISODES-1
round2 = EPISODES2-1

# For Q
get_point = 10
lost_point = -10

touch_point = 8

MOVE = 0.005