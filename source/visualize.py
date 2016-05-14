import pygame
from pygame.locals import *
import sys
import networkx as nx
from graph.graph import load_graph_from_database


def main():
    # set up pygame
    pygame.init()
    
    # set up the window
    screen_width = 640
    screen_height = 480
    windowSurface = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption('Network Simulation')
    
    # set up the colors
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    
    # draw the white background onto the surface
    windowSurface.fill(WHITE)
    
    # generate a simple graph
    graph = load_graph_from_database('FactoryBerlin')
    print(graph.node['FactoryBerlin']['screenname'])
    
    layout = nx.spring_layout(graph)
    
    # draw the nodes
    for node in layout:
        pygame.draw.circle(windowSurface, GREEN,
                           (int(layout[node][0] * 250) + 50, int(layout[node][1] * 250) + 50), 2, 0)
    
    # draw the window onto the screen
    pygame.display.update()
    
    # run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


class Node(object):
    """Class Representing a Node object, keeps track of position, edges, etc
    
    """
    def __init__(self, args):
        super(Node, self).__init__()
        self.args = args
        

if __name__ == "__main__":
    main()
