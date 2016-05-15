#!/usr/bin/python
import pygame
from pygame.locals import *
import networkx as nx
from graph.graph import load_graph_from_database


def main():
    # set up pygame
    pygame.init()
    
    # set up the window
    screen_width = 640
    screen_height = 480
    windowSurface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Network Simulation')
    
    # set up the colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 200, 0)
    
    # draw the white background onto the surface
    windowSurface.fill(WHITE)
    
    # generate a simple graph
    graph = load_graph_from_database('FactoryBerlin')
    layout = nx.spring_layout(graph)
    print(graph.node['FactoryBerlin']['screenname'])
    
    for edge in graph.edges():
        pygame.draw.line(windowSurface, BLACK, true_position(layout[edge[0]]), true_position(layout[edge[1]]))
        print(layout[edge[0]])
    
    # draw the nodes
    for node in layout:
        pygame.draw.circle(windowSurface, GREEN, true_position(layout[node]), 10, 0)
        print(graph.node[node]['screenname'])
    
    # button rectangle
    pygame.draw.rect(windowSurface, GREEN, (50, 400, 30, 30))
    
    # draw the window onto the screen
    pygame.display.update()
    
    # run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            print(pygame.mouse.get_pos())
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
    pygame.display.quit()


def true_position(coordinates):
    return (int(coordinates[0] * 250) + 50, int(coordinates[1] * 250) + 50)


class Node(object):
    """Class Representing a Node object, keeps track of position, edges, etc
    
    """
    def __init__(self, args):
        super(Node, self).__init__()
        self.args = args
        

if __name__ == "__main__":
    main()
