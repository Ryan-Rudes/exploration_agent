# Exploration Agent
A script that maps any environment in the OpenAI Gym repo.

<a href="https://ibb.co/GRTZNHp"><img src="https://i.ibb.co/7K43LkC/Qbert-v0-map.jpg" alt="Qbert-v0-map" border="0"></a>

Generates a figure like the above. Each node is a unique cell (downscaled representation of a frame). The edges connecting cells indicate actions you can take to arrive at one cell from the prior. The edges are color coded according to the action taken, and displayed on a legend. The color of the nodes indicate the score of the particular state represented by each node. Brighter green implies higher score areas, wheras dark green/black color indicates lower score states.

# Quickstart
```
git clone https://github.com/Ryan-Rudes/exploration_agent.git
cd exploration_agent/
python3 map.py
```
Then, you'll need to enter the environment ID of one of OpenAI gym's Atari environments. \
You can select one [here](https://gym.openai.com/envs/#atari).
