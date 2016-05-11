from pygame.locals import *
import pygame
import sys
import networkx as nx
import pprint

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
graph.add_node(3)
graph.add_node(4)
graph.add_node(5)
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 4)
graph.add_edge(1, 5)

layout = nx.spring_layout(graph)
pprint.pprint(layout)

for node in layout:
    print(node, 'corresponds to', layout[node])
    pygame.draw.circle(windowSurface, GREEN,
                       (int(layout[node][0] * 250) + 100, int(layout[node][1] * 250) + 100), 20, 0)

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
