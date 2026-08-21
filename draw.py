from constants import SCALE

import pygame

class Rendering:

    def __init__(self, screen, camera, font):
        self.screen = screen
        self.camera = camera
        self.font = font

    def draw_entity(self, screen, screen_position, renderable, identity, trail_positions, font):
        for point in trail_positions:
            pygame.draw.circle(screen, renderable.color, point, max(1, renderable.radius//2))

        pygame.draw.circle(screen, renderable.color, screen_position, renderable.radius)

        text= font.render(identity.name, True, (25,255,255))

        label_pos = (
            screen_position[0] + renderable.radius + 5,
            screen_position[1]
        )

        screen.blit(text, label_pos)

        return text.get_rect(topleft=label_pos)





    def to_screen_position(self, x, y):
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2

        screen_x = screen_center_x + (x - self.camera.x) * SCALE * self.camera.zoom
        screen_y = screen_center_y - (y - self.camera.y) * SCALE * self.camera.zoom

        return int(screen_x), int(screen_y)

    def update(self, renderables, positions, identities, trails):
        self.screen.fill((0, 0, 0))
        label_rects = {}
        for entity, renderable in renderables.items():
            position = positions[entity]
            identity = identities[entity]
            screen_position  = self.to_screen_position(position.x, position.y)

            trail = trails.get(entity)

            if trail:
                trail_position = [
                    self.to_screen_position(x,y)
                    for x, y in trail.points
                ]
            else:
                trail_position = []



            label_rects[entity] = self.draw_entity(self.screen, screen_position, renderable, identity, trail_position, self.font )


        return label_rects
