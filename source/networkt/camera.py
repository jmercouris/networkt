class Camera(object):
    """Documentation for Camera
    
    """
    def __init__(self, **kwargs):
        super(Camera, self).__init__()
        self.position = (0, 0)
        self.zoom = 250
        self.move_speed = 10
        self.zoom_factor = 30
    
    def shift_up(self):
        self.position = (self.position[0], self.position[1] + self.move_speed)
    
    def shift_down(self):
        self.position = (self.position[0], self.position[1] - self.move_speed)
    
    def shift_left(self):
        self.position = (self.position[0] - self.move_speed, self.position[1])
    
    def shift_right(self):
        self.position = (self.position[0] + self.move_speed, self.position[1])
    
    def shift_offset(self, offset):
        self.position = (self.position[0] + offset[0], self.position[1] + offset[1])
    
    def zoom_in(self):
        self.zoom = self.zoom + self.zoom_factor
    
    def zoom_out(self):
        self.zoom = self.zoom - self.zoom_factor
