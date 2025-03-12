# **Q-Learning Pong Game** 🏓

A reinforcement learning project that combines the classic Pong game with an AI agent powered by Q-Learning. This project demonstrates how an agent learns and evolves to play Pong through trial and error.

---

## **Features** ✨

- **AI Training with Q-Learning**: 
  - Agents are trained to maximize their performance using Q-Learning and ε-greedy exploration.
- **Customizable Game Environment**: 
  - Easily adjust parameters like paddle speed, ball speed, and acceleration.
- **Real-time Visualization**: 
  - Watch the training process live with game simulations powered by **Pygame**.
- **Performance Metrics**: 
  - Visualize the agent's learning progress with reward trends and action statistics.

---
![image](https://github.com/Raytengo/Pong-with-RL/blob/main/img/Demo.png)

## **How It Works** ⚙️

1. **Environment**:

   - The game environment models the Pong mechanics, including ball dynamics, paddle movements, and collision physics.

2. **Q-Learning Agent**:

   - **State Space**: Includes ball position, direction, and paddle positions.
   - **Action Space**: Consists of paddle movements (up, down, stay).
   - **Learning Process**: The agent learns by updating its Q-table based on rewards from the environment.

3. **Reward System**:

   - **Positive Rewards**: For successful ball hits and scoring.
   - **Negative Rewards**: For missed balls or idle actions.

4. **Visualization**:

   - **Real-time Gameplay Display**: Powered by **Pygame**.
   - **Performance Metrics**: Post-training plots of agent performance metrics.

---

## **Challenges and Solutions** 🛠️

1. **Initial Agent Instability**:
   - **Problem**: In early training, the agent exhibited excessive vertical jittering, leading to inefficient gameplay and a poor visual experience.
   - **Solution**: Introduced a penalty for each movement to discourage unnecessary actions. By fine-tuning the penalty value, this issue was significantly improved.

2. **Lack of Ball Interaction**:
   - **Problem**: The agent was initially reluctant to engage with the ball, resulting in suboptimal performance.
   - **Solution**: Added a reward for each successful ball contact. This incentive encouraged more proactive gameplay and noticeably enhanced overall performance.

3. **Uneven AI Training**:
   - **Problem**: The right paddle's AI initially performed significantly worse than the left paddle's AI. Upon investigation, it was discovered that the default initialization of `AI()` was set for the left paddle, requiring `AI(False)` to properly train the right paddle.
   - **Solution**: Updated the initialization to correctly specify `AI(False)` for the right paddle, ensuring balanced training for both sides. This adjustment resolved the issue effectively.

---

## **File Overview** 🗂️

- **`main.py`**: 
  - The main script for training and running the Pong game. Handles the initialization of the environment, AI agents, and visualization during training. (Q-learning vs. Q-learning)
 
- **`main_track.py`**: 
  - Another main script for training and running the Pong game.(Q-learning vs. Paddle that always track the ball)

- **`ai.py`**: 
  - Contains the implementation of the Q-Learning agent, including the Q-table, action selection, and reward updates.

- **`environment.py`**: 
  - Defines the Pong game environment, including ball and paddle dynamics, collision detection, and reward calculation.

- **`config.py`**: 
  - Stores all configurable parameters such as game settings (e.g., screen size, paddle speed), Q-learning parameters (e.g., alpha, gamma), and reward values.

- **`play.py`**:
  - For player to play with agent.

