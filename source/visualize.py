#!/usr/bin/python
import pygame
from pygame.locals import *
import networkx as nx
from graph.graph import load_graph_from_database
from pgu import gui

screen_width = 640
screen_height = 480
fps = 30


def main():
    # set up pygame
    pygame.init()
    
    # set up the window
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Network Simulation')
    
    # set up the colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 200, 0)
    
    # draw the white background onto the surface
    screen.fill(WHITE)
    
    # generate a simple graph
    graph = load_graph_from_database('FactoryBerlin')
    layout = nx.spring_layout(graph)
    
    for edge in graph.edges():
        pygame.draw.line(screen, BLACK, true_position(layout[edge[0]]), true_position(layout[edge[1]]))
        # print(layout[edge[0]])
    
    # draw the nodes
    for node in layout:
        pygame.draw.circle(screen, GREEN, true_position(layout[node]), 10, 0)
        # print(graph.node[node]['screenname'])
    
    theme = gui.Theme("gray")
    app = gui.App(theme=theme)
    root_control = RootControl()
    c = gui.Container(align=-1, valign=-1)
    c.add(root_control, 20, 440)
    app.init(c)
    
    # draw the window onto the screen
    pygame.display.update()
    
    # run the game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            # elif event.type == MOUSEBUTTONDOWN:
            #     print(pygame.mouse.get_pos())
            else:
                app.event(event)
        clock.tick(fps) / 1000.0
        app.paint()
        pygame.display.flip()
        pygame.display.update()
    pygame.display.quit()


def true_position(coordinates):
    return (int(coordinates[0] * 250) + 50, int(coordinates[1] * 250) + 50)


class RootControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)

        def fullscreen_changed(btn):
            pygame.display.toggle_fullscreen()
            print("TOGGLE FULLSCREEN")

        def stars_changed(slider):
            print("Changed")

        fg = (0, 0, 0)

        self.tr()

        self.td(gui.Label("Speed: ", color=fg), align=1)
        e = gui.HSlider(100, -500, 500, size=20,
                        width=100, height=16, name='speed')
        self.td(e)

        btn = gui.Button('Play')
        btn.connect(gui.CHANGE, fullscreen_changed, btn)
        self.td(btn)


if __name__ == "__main__":
    main()
