import pygame
from colors_constant import web_colors as colors
from gui.utils import text_objects


def start_app(width=1000, height=600):
    pygame.init()

    active = True

    game_display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Seismic statistic")

    clock = pygame.time.Clock()

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(colors['bisque'])

        ####
        display_text(game_display, 'Выберите действие', colors['black'], 30, width / 2, height / 6)
        ####
        mouse = pygame.mouse.get_pos()
        ####
        btn_x_start, btn_y_start = width / 10, height / 6 * 2
        btn_width, btn_height = width / 6 * 5, height / 12
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        hover_mouse(game_display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'])
        display_text(game_display, 'Количество сейсмических активностей по штатам за период', colors['white'], 20,
                     btn_x_start + btn_width / 2, btn_y_start + btn_height / 2)
        ####
        btn_y_start = height / 6 * 3
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        hover_mouse(game_display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'])
        display_text(game_display, 'Средняя магнитуда по США по дням за период', colors['white'], 20,
                     btn_x_start + btn_width / 2, btn_y_start + btn_height / 2)
        ####
        btn_y_start = height / 6 * 4
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        hover_mouse(game_display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'])
        display_text(game_display, 'Средняя магнитуда по США на сегодняшний день (Машинное обучение)', colors['white'],
                     20, btn_x_start + btn_width / 2, btn_y_start + btn_height / 2)
        ####

        pygame.display.update()
        clock.tick(20)

    pygame.quit()
    quit()


def hover_mouse(display, mouse, pos, color_before, color_during):
    if pos[0] + pos[2] > mouse[0] > pos[0] and pos[1] + pos[3] > mouse[1] > pos[1]:
        pygame.draw.rect(display, color_during, pos)
    else:
        pygame.draw.rect(display, color_before, pos)


def display_text(display, text, color, font_size, center_x, center_y):
    font_text = pygame.font.Font("freesansbold.ttf", font_size)
    text_surf, text_rect = text_objects(text, font_text, color)
    text_rect.center = (center_x, center_y)
    display.blit(text_surf, text_rect)
