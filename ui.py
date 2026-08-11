import pygame
from helpers import get_distance, get_speed
from components import Identity


class Ui:
    def draw_info_box(self, screen, screen_position, font, lines ):

        box_x = screen_position[0] + 20
        box_y = screen_position[1] + 20

        box_width=220
        box_height=80

        pygame.draw.rect(screen, (30,30,30), (box_x, box_y, box_width, box_height))

        y=box_y +8
        for line in lines:
            text = font.render(line, True, (255,255,255))
            screen.blit(text, (box_x + 8, y))
            y +=22
