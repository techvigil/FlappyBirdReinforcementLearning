# Reinforcement-Learning
Flappy Bird

Produce a Table of RL-based approaches (Policy Iteration, Value Iteration, Q Learning) 
where each row is an approach and each column is a dimension that differentiates the approaches such as model free, 
which of the quintuple each uses (State, Action, Transitions, Rewards, etc..), and other dimensions.


Flappybird is a side-scrolling game where the agent must successfully navigate through gaps between pipes. The up arrow causes the bird to accelerate upwards. If the bird makes contact with the ground or pipes, or goes above the top of the screen, the game is over. For each pipe it passes through it gains a positive reward. Each time a terminal state is reached it receives a negative reward.

Vertical distance from lower pipe
Horizontal distance from next pair of pipes
Life: Dead or Living

Actions
For each state, there two possible actions
Click
Do Nothing
1.4  Rewards
The reward structure is purely based on the "Life" parameter. One possible such structure could be the following (feel free to explore more):
+1 if Flappy Bird is still alive
-1000 if Flappy Bird is dead
1.5  Flappy Birds Simulator:
Please use the openai gym environment for this project:

https://gym.openai.com/envs/FlappyBird-v0/

*End Goal*

Determine a good policy for Flappy Birds using any one or more of the following algorithms (aim to get 140 points or more!):

Policy Iteration, Value Iteration, Q Learning, TD, Monte Carlo
You may have to discretize the space of following parameters.

*Folder Structure:*

| File | Description |
| --- | --- |
| flappy_bird_env_open_ai_gym.py | Python file. Flappy Bird Environment implementation derving from GYM ENVIRONMENT object. All the algorithms implemented in this project, except tabular Q-Learning, are using this file.  |
| flappy_bird_utils.py | Python file. Helper functions needed for flappy_bird_env_open_api_gym.py. |
| flappy_bird_env_py_game.py | Python file. Py Game based Flappy Bird Tabular Q-Learning is using this environment. Simple implementation but unfortunately, it needs to be cleaned up. Current implemetnation takes agent as into into the environment and they need to be decoupled. However, for some readon, PyGame driven Flappy Brid works better, in Windows OS, from  Jupyter Notebook compared to Open AI Gym implementation.|
| flappy_bird_tabular_qlearning.ipynb | Jupyter Notebook to explore the Tabular Temportal-Difference (TD) Q-Learning algorithm.|
| flappy_bird_va_linear_regression.ipnyb | Jupyter Notebook to explore the Linear/Stochastic Graident Descent value approximation function for Q-Learning algorithm.|
| flappy_bird_va_simple_network.ipnyb | Jupyter Notebook to explore the Simple three-layer neural network for Q-Learning algorithm.|
| flappy_bird_va_deep_learning.ipnyb | Jupyter Notebook to explore the Deep multi-layer deep neural network for Q-Learning algorithm.|
| flappy_bird_project_report.ipnyb | Jupyter Notebook to list project bird algorithm comparisons and related material.|
| assets folder| Folder to store all the images needed for the Flappy Bird Environment.|
| data folder| Folder. Contains: models saved in H5 and JSON format. Also all the statistics - epsiode, duration, reward, score saved in JSON format needed for the final report flappy_bird_project_report.ipnyb.|
| images folder| Folder to store all the images needed for the jupyter notebooks to render properly - equations, images, etc.|

*Requirements*
tensorflow
Keras
gym
pygame
pygame=2.0.0.dev4 (For macos mojave and above)
matplotlib
numpy
pandas