import pygame

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


    def draw_simulation_clock(self, screen, font, time):
        clock_text = font.render(
            f"Simulation Time: {time[0]:.2f} years",
            True,
            (25,255,255)
        )

        screen.blit(clock_text, (10,10))


    def draw_tel_menu(self,screen,telemetry_rects, telemetry_options,font):
         options = [
             ("speed", "Speed"),
             ("mass", "Mass"),
             ("distance", "Distance"),
             ("velocity", "Velocity")
         ]

         x = 20
         y = 60

         for key, label in options:
             checkbox_rect = pygame.Rect(x,y, 18,18)

             pygame.draw.rect(screen, (255,255,255), checkbox_rect,2)

             if telemetry_options[key]:
                 pygame.draw.line(screen, (255,255,255), checkbox_rect.topleft, checkbox_rect.bottomright, 2)

             text = font.render(label, True, (255,255,255))
             screen.blit(text, (x+28, y - 2))

             telemetry_rects[key] = checkbox_rect

             y += 28

    def draw_delta_v_input(self, screen, font, rect, text, active):
        pygame.draw.rect(screen, (25,255,255), rect, 2)
        label = font.render("Δv (km/s)", True, (255,255,255))
        screen.blit(label, (rect.x, rect.y-20))

        value = font.render(text, True, (255,255,255))

        screen.blit(value, (rect.x + 5, rect.y + 6))


    def draw_launch_button(self, screen, font, rect):
        pygame.draw.rect(screen, (255,255,255), rect, 2)

        text = font.render("Launch", True, (255,255,255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, (text_rect))
