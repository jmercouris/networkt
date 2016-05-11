import pygame
import sys
from pygame.locals import *
import networkx as nx
import matplotlib.pyplot as plt

# set up pygame
pygame.init()

# set up the window
screen_width = 700
screen_height = 400
windowSurface = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption('Network Simulation')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# draw the white background onto the surface
windowSurface.fill(WHITE)

# generate a simple graph
graph = nx.Graph()
graph.add_node(1)
graph.add_node(2)
graph.add_edge(1, 2)
nx.draw(graph)
plt.savefig("path.png")

# draw a blue circle onto the surface
pygame.draw.circle(windowSurface, BLUE, (300, 50), 20, 0)

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
