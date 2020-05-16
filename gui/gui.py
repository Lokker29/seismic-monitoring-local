import pygame
from colors_constant import web_colors as colors
from config import MONGO_DB_NAME, MONGO_DB_HOST, MONGO_DB_USER, MONGO_DB_PASSWORD, BASE_SEISMIC_COLLECTION
from db import DBClient
from gui.handlers import count_of_state, avg_mag, ai_today_mag
from gui.utils import text_objects
from plot import SeismicPlot


def connect(client):
    client.connect(host=MONGO_DB_HOST, user=MONGO_DB_USER, password=MONGO_DB_PASSWORD)

    client.set_db(MONGO_DB_NAME)

    client.set_collection(BASE_SEISMIC_COLLECTION)


def get_client_and_plot():
    client = DBClient()
    splot = SeismicPlot()

    connect(client)

    return client, splot


client, splot = get_client_and_plot()


def start_app(width=1000, height=600):
    pygame.init()

    active = True

    game_display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Seismic statistic")

    clock = pygame.time.Clock()

    while active:
        events_type = [event.type for event in pygame.event.get()]

        quit_was_happen = pygame.QUIT in events_type
        if quit_was_happen:
            pygame.quit()
            quit()

        mouse_click_down = pygame.MOUSEBUTTONDOWN in events_type

        game_display.fill(colors['bisque'])

        ####
        display_text(game_display, 'Выберите действие', colors['black'], 30, width / 2, height / 6)
        ####

        mouse = pygame.mouse.get_pos()
        ####
        btn_x_start, btn_y_start = width / 10, height / 6 * 2
        btn_width, btn_height = width / 6 * 5, height / 12
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        handler_btn(game_display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'state_statistic',
                    mouse_click_down)
        display_text(game_display, 'Количество сейсмических активностей по штатам за период', colors['white'], 20,
                     btn_x_start + btn_width / 2, btn_y_start + btn_height / 2)
        ####
        btn_y_start = height / 6 * 3
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        handler_btn(game_display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'avg_mag',
                    mouse_click_down)
        display_text(game_display, 'Средняя магнитуда по США по дням за период', colors['white'], 20,
                     btn_x_start + btn_width / 2, btn_y_start + btn_height / 2)
        ####
        btn_y_start = height / 6 * 4
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        handler_btn(game_display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'ai_today_mag',
                    mouse_click_down)
        display_text(game_display, 'Средняя магнитуда по США на сегодняшний день (Машинное обучение)', colors['white'],
                     20, btn_x_start + btn_width / 2, btn_y_start + btn_height / 2)
        ####

        pygame.display.update()
        clock.tick(20)

    pygame.quit()
    quit()


def handler_btn(display, mouse, pos, color_before, color_during, action=None, mouse_click=False):
    click = pygame.mouse.get_pressed()

    action_dict = {
        'state_statistic': count_of_state,
        'avg_mag': avg_mag,
        'ai_today_mag': ai_today_mag,
    }

    if pos[0] + pos[2] > mouse[0] > pos[0] and pos[1] + pos[3] > mouse[1] > pos[1]:
        pygame.draw.rect(display, color_during, pos)

        if mouse_click and click[0] == 1 and action in action_dict.keys():
            action_dict[action](client=client, splot=splot)
    else:
        pygame.draw.rect(display, color_before, pos)


def display_text(display, text, color, font_size, center_x, center_y):
    font_text = pygame.font.Font("freesansbold.ttf", font_size)
    text_surf, text_rect = text_objects(text, font_text, color)
    text_rect.center = (center_x, center_y)
    display.blit(text_surf, text_rect)
