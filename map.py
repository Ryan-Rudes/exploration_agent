import gym
import numpy as np
import cv2
from hashlib import sha256
import matplotlib.pyplot as plt
import networkx as nx
import pylab
import matplotlib.patches as mpatches
import matplotlib

def make_cell(state):
  cell = cv2.cvtColor(state, cv2.COLOR_RGB2GRAY)
  cell = cv2.resize(state, (11, 8), interpolation = cv2.INTER_AREA)
  cell = cell // (255 / 8)
  return cell

def make_reference(cell):
  reference = sha256(cell).hexdigest()
  return reference

def get_reference(state):
  cell = make_cell(state)
  reference = make_reference(cell)
  return reference
  
"""
def generate_rgba(n, alpha=1):
  rgb_values = []
  rgb = (np.random.random(size = 3) * 256).astype(int)
  step = 256 / n
  for i in range(n):
    rgb = rgb + step
    rgb = rgb.astype(int) % 256
    rgb_values.append((*tuple(rgb / 256), alpha))
  return rgb_values
"""

name = input("Enter OpenAI Gym environment ID (ie. Qbert-v0): ")
env = gym.make(name)
idx = 0

graph = nx.DiGraph()
cmap = matplotlib.cm.get_cmap("Paired")
colors = [cmap(x) for x in np.linspace(0, 1, num = env.action_space.n)]

state = env.reset()
prev_ref = get_reference(state)

references = [prev_ref]
restores = [env.env.clone_full_state()]
actions_taken = [list(range(env.action_space.n))]
explored = [0]
scores = [0]

edge_labels = {}

episodes = int(input("Number of episodes (ie. 100): "))
draw_frequency = int(input("Every ___ episodes, save the figure (ie. 10): "))

for episode in range(episodes):
  score = scores[idx]
  while True:
    if len(actions_taken[idx]) == 0:
      explored[idx] = 1
      actions_taken[idx] = list(range(env.action_space.n))

    action = np.random.choice(actions_taken[idx])
    actions_taken[idx].remove(action)
      
    state, reward, terminal, info = env.step(action)
    score += reward
    terminal = terminal or info['ale.lives'] < 3
    if terminal: break
    curr_ref = get_reference(state)
    if not curr_ref in references:
      references.append(curr_ref)
      graph.add_node(curr_ref)
      restores.append(env.env.clone_full_state())
      actions_taken.append(list(range(env.action_space.n)))
      explored.append(0)
      scores.append(score)

    graph.add_edge(prev_ref, curr_ref)
    edge_labels[(prev_ref, curr_ref)] = action
    prev_ref = curr_ref
    idx = references.index(prev_ref)
    
  if episode % draw_frequency == 0:
    edge_colors = [cmap(action / env.action_space.n) for action in list(edge_labels.values())]
    maxx = max(scores)
    node_colors = [(*((np.array([94, 255, 0]) * score / maxx) / 255), 1) for score in scores]
    widths = [0.1 for u, v in graph.edges]
    fig = plt.figure(figsize = (10, 10))
    pos = nx.spring_layout(graph)
    labels = {(ref1, ref2): env.env.get_action_meanings()[action] for (ref1, ref2), action in zip(edge_labels.keys(), edge_labels.values())}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = labels, font_size = 1)
    nx.draw_networkx_edges(graph, pos, arrowstyle = '-|>', arrowsize = 1, width = 0.1, edge_color = edge_colors)
    nx.draw_networkx_nodes(graph, pos, node_color = node_colors, node_size = 1)
    handles = [mpatches.Patch(color = color, label = label) for color, label in zip(colors, env.env.get_action_meanings())]
    plt.legend(handles = handles, title = "Actions")
    plt.title(name)
    pylab.close()
    fig.savefig("%s_map.jpeg" % name, dpi = 1000)
  
  p = 1 - np.array(explored)
  p = p / p.sum()
  idx = np.random.choice(np.arange(len(references)), p = p)
  env.reset()
  env.env.restore_full_state(restores[idx])
  prev_ref = references[idx]
  print ("Episode: %s, Cells: %s" % (episode + 1, len(references)))
