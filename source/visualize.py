import pygame
from pygame.locals import *
import networkx as nx
from graph.graph import load_graph_from_database
from pgu import gui
from pprint import pprint

screen_width = 640
screen_height = 480
fps = 5
# set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Network Simulation')
    
    # generate a simple graph
    graph = load_graph_from_database('FactoryBerlin')
    nodes = []
    layout = nx.spring_layout(graph)
    
    for edge in graph.edges():
        pygame.draw.line(screen, BLACK, true_position(layout[edge[0]]), true_position(layout[edge[1]]))
        # print(layout[edge[0]])
    
    # draw the nodes
    for node in layout:
        nodey = Node(graph.node[node])
        nodey.position = true_position(layout[node])
        nodes.append(nodey)
    
    theme = gui.Theme("gray")
    app = gui.App(theme=theme)
    root_control = RootControl()
    c = gui.Container(align=-1, valign=-1)
    c.add(root_control, 20, 440)
    app.init(c)
    
    # run the game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        # Handle Input
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            # if event.type == MOUSEBUTTONDOWN:
            #     print(pygame.mouse.get_pos())
            else:
                app.event(event)
        clock.tick(fps) / 1000.0
        # Clear Surface
        screen.fill(WHITE)
        # Draw
        for node in nodes:
            pygame.draw.circle(screen, GREEN, node.position, 10, 0)
        app.paint()
        pygame.display.flip()
        pygame.display.update()
    pygame.display.quit()


def true_position(coordinates):
    return (int(coordinates[0] * 250) + 50, int(coordinates[1] * 250) + 50)


class Node(object):
    """Documentation for Node
    
    """
    def __init__(self, dictionary):
        self.position = ''
        self.created_at = dictionary.get('createdat', None)
        self.description = dictionary.get('description', None)
        self.favorites_count = int(dictionary.get('favouritescount') or -1)
        self.followers_count = int(dictionary.get('followerscount') or -1)
        self.friends_count = int(dictionary.get('friendscount') or -1)
        self.id_str = dictionary.get('idstr', None)
        self.lang = dictionary.get('lang', None)
        self.listed_count = int(dictionary.get('listedcount') or -1)
        self.location = dictionary.get('location', None)
        self.name = dictionary.get('name', None)
        self.screen_name = dictionary.get('screenname', None)
        self.statuses_count = int(dictionary.get('statusescount') or -1)
        self.time_zone = dictionary.get('timezone', None)
        self.utc_offset = int(dictionary.get('utcoffset') or -1)
        self.verified = bool(dictionary.get('verified', False) or False)
        self.id = int(self.id_str)


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
        btn = gui.Button('Play')
        btn.connect(gui.CHANGE, fullscreen_changed, btn)
        self.td(btn)
        self.td(gui.Label("Speed: ", color=fg), align=1)
        e = gui.HSlider(100, -500, 500, size=20,
                        width=100, height=16, name='speed')
        self.td(e)


if __name__ == "__main__":
    main()
