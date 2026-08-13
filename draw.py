import pygame

class Rendering:
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
