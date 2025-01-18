# Pong-with-RL
Atari-inspired Pong game featuring a Q-Learning agent that learns and evolves through dynamic gameplay.

How It Works ⚙️
Environment:

The game environment models the Pong mechanics, including ball dynamics, paddle movements, and collision physics.
Q-Learning Agent:

State space includes ball position, direction, and paddle positions.
Action space consists of paddle movements (up, down, stay).
The agent learns by updating its Q-table based on rewards from the environment.
Reward System:

Positive rewards for successful ball hits and scoring.
Negative rewards for missed balls or idle actions.
Visualization:

Real-time gameplay display via Pygame.
Post-training plots of agent performance metrics.
Key Parameters 🔧
Learning Rate (α): 0.1
Discount Factor (γ): 0.9
Exploration Decay (ε-decay): 0.995
Episodes: 20,000
All parameters can be modified in the config.py file.

Results 📊
Learning Progress: Observe how the agent's performance improves across episodes through catch counts and rewards.
Q-Table Visualization: A snapshot of the Q-values for each state-action pair.
Future Improvements 🚀
Implement Deep Q-Learning (DQN) for better generalization.
Add noise and randomness to enhance training robustness.
Integrate multiplayer or online gameplay options.
Contributing 🤝
Feel free to submit issues or pull requests to improve this project. Contributions are always welcome!

License 📜
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments 🙌
Inspired by the classic Atari Pong.
Thanks to the open-source community for amazing libraries like NumPy, Matplotlib, and Pygame.
