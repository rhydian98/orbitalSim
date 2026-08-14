class Camera:
    def __init__(self, screen):
        self.screen = screen
        self.zoom = 1.0
        self.target = None
        self.x = 0
        self.y = 0

    def clamp_zoom(self):
        self.zoom = max(0.1, min(self.zoom, 1_000_000))

    def zoom_out(self):
        self.zoom /= 1.2
        self.clamp_zoom()

    def zoom_in(self):
        self.zoom *= 1.2
        self.clamp_zoom()

    def focus_on(self,entity):
        self.target = entity

    def update(self, positions):
        if self.target == None:
            return

        position = positions[self.target]

        self.x = position.x
        self.y = position.y
