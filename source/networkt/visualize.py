import pygame
from pygame.locals import *
import networkx as nx
from graph.graph import load_graph_from_database, get_statuses_for_screen_name
from pgu import gui


screen_width = 640
screen_height = 480
fps = 30
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
    nodes = {}
    layout = nx.spring_layout(graph)
    
    # draw the nodes
    for node in layout:
        nodey = Node(graph.node[node])
        nodey.position = true_position(layout[node])
        nodey.statuses = get_statuses_for_screen_name(nodey.screen_name)
        nodes[nodey.screen_name] = nodey
    
    for edge in graph.edges():
        pygame.draw.line(screen, BLACK, true_position(layout[edge[0]]), true_position(layout[edge[1]]))
        nodes[edge[0]].edges.append(nodes[edge[1]])
    
    menus = gui.Menus([
        ('File/Exit', None, None),
        ('Help/Help', None, None),
        ('Help/About', None, None)
    ])
    
    theme = gui.Theme("gray")
    app = gui.App(theme=theme)
    root_control = RootControl()
    inspector_view = InspectorView()
    c = gui.Container(align=-1, valign=-1)
    c.add(root_control, 20, 440)
    c.add(inspector_view, screen_width - 180, 30)
    c.add(menus, 0, 0)
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
            nodes[node].act(screen)
        
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
        self.tick = 0
        self.position = ''
        self.active_statuses = []
        self.edges = []
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
    
    def act(self, screen):
        # Draw Edges
        for edge in self.edges:
            pygame.draw.line(screen, BLACK, self.position, edge.position)
        # Draw Self
        pygame.draw.circle(screen, GREEN, self.position, 10, 0)
        
        # Animate Messages
        self.tick = self.tick + 1
        if (self.tick % 60 == 0):
            for edge in self.edges:
                self.active_statuses.append(Status(self.position, edge.position))
        
        valid_statuses = []
        for status_object in self.active_statuses:
            status_object.act(screen)
            if (status_object.alive):
                valid_statuses.append(status_object)
        self.active_statuses = valid_statuses


class Status(object):
    """Represents a status
    
    """
    def __init__(self, position, destination):
        self.position = position
        self.destination = destination
        self.true_position = self.position
        self.steps = 60
        self.dx = (self.destination[0] - self.position[0]) / self.steps
        self.dy = (self.destination[1] - self.position[1]) / self.steps
        self.alive = True
    
    def act(self, screen):
        # Maintain a Virtual Position that is more exact than pixels
        self.true_position = (self.true_position[0] + self.dx, self.true_position[1] + self.dy)
        self.position = (int(self.true_position[0]), int(self.true_position[1]))
        pygame.draw.circle(screen, BLACK, self.position, 5, 0)
        self.steps = self.steps - 1
        if (self.steps < 0):
            self.alive = False


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
        self.td(gui.Button('Play'))
        self.td(gui.Button('Pause'))
        self.td(gui.Button('Reset'))
        self.td(gui.Label("Speed: ", color=fg), align=1)
        e = gui.HSlider(100, -500, 500, size=20,
                        width=100, height=16, name='speed')
        self.td(e)


class InspectorView(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)
        
        def fullscreen_changed(btn):
            pygame.display.toggle_fullscreen()
            print("TOGGLE FULLSCREEN")
        
        def stars_changed(slider):
            print("Changed")
        
        self.tr()
        self.td(gui.Label("Inspector", cls="h4"))
        self.tr()
        my_list = gui.List(width=150, height=200)
        for i in range(0,100):
            my_list.add("item ", value=i)

        self.td(my_list)
        self.tr()
        self.td(gui.Button('Reset', width=150), align=-1)


if __name__ == "__main__":
    main()
