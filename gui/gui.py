from datetime import date

import pygame
from colors_constant import web_colors as colors
from config import MONGO_DB_NAME, MONGO_DB_HOST, MONGO_DB_USER, MONGO_DB_PASSWORD, BASE_SEISMIC_COLLECTION
from db import DBClient
from gui.handlers import count_of_state, avg_mag
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

    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Seismic statistic")

    clock = pygame.time.Clock()

    while active:
        events_type = [event.type for event in pygame.event.get()]

        quit_was_happen = pygame.QUIT in events_type
        if quit_was_happen:
            pygame.quit()
            quit()

        mouse_click_down = pygame.MOUSEBUTTONDOWN in events_type

        display.fill(colors['bisque'])

        ####
        count = 1
        display_text(display, 'Выберите действие', colors['black'], 30, width / 2, height / 6 * count)
        ####

        mouse = pygame.mouse.get_pos()
        ####
        count += 1
        btn_x_start, btn_y_start = width / 10, height / 6 * count
        btn_width, btn_height = width / 6 * 5, height / 12
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'state_statistic',
                    mouse_click_down, 'Количество сейсмических активностей по штатам за период',
                    colors['white'], 20, btn_x_start + btn_width / 2, btn_y_start + btn_height / 2,
                    client=client, splot=splot)
        ####
        count += 1
        btn_y_start = height / 6 * 3
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'avg_mag',
                    mouse_click_down, 'Средняя магнитуда по США по дням за период',
                    colors['white'], 20, btn_x_start + btn_width / 2, btn_y_start + btn_height / 2,
                    client=client, splot=splot)
        ####
        count += 1
        btn_y_start = height / 6 * 4
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'ai_today_mag',
                    mouse_click_down, 'Средняя магнитуда по США на сегодняшний день (Машинное обучение)',
                    colors['white'], 20, btn_x_start + btn_width / 2, btn_y_start + btn_height / 2,
                    width=width, height=height, client=client)
        ####
        count += 1
        btn_y_start = height / 6 * 5
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'quit',
                    mouse_click_down, 'Завершить приложение', colors['white'], 20,
                    btn_x_start + btn_width / 2, btn_y_start + btn_height / 2)
        ####

        pygame.display.update()
        clock.tick(20)

    handle_quit()


def handler_btn(display, mouse, pos, color_before, color_during, action=None, mouse_click=False, **kwargs):
    click = pygame.mouse.get_pressed()

    action_dict = {
        'state_statistic': count_of_state,
        'avg_mag': avg_mag,
        'ai_today_mag': ai_today_mag,
        'return_to_main': start_app,
        'quit': handle_quit,
    }

    if pos[0] + pos[2] > mouse[0] > pos[0] and pos[1] + pos[3] > mouse[1] > pos[1]:
        pygame.draw.rect(display, color_during, pos)

        if mouse_click and click[0] == 1 and action in action_dict.keys():
            action_dict[action](**kwargs)
    else:
        pygame.draw.rect(display, color_before, pos)


def display_text(display, text, color, font_size, center_x, center_y):
    font_text = pygame.font.Font("freesansbold.ttf", font_size)
    text_surf, text_rect = text_objects(text, font_text, color)
    text_rect.center = (center_x, center_y)
    display.blit(text_surf, text_rect)


def ai_today_mag(client, **kwargs):
    data = client.get_avg_magnitude_today()

    width = kwargs['width']
    height = kwargs['height']

    display = pygame.display.set_mode((width, height))

    clock = pygame.time.Clock()

    active = True
    while active:
        events_type = [event.type for event in pygame.event.get()]

        quit_was_happen = pygame.QUIT in events_type
        if quit_was_happen:
            handle_quit()

        mouse_click_down = pygame.MOUSEBUTTONDOWN in events_type

        display.fill(colors['bisque'])

        data = round(data, 2)
        text = f'Сегодня {date.today().strftime("%d-%m-%Y")} средняя магнитуда будет составлять {str(data)}'
        display_text(display, text, colors['black'], 30, width / 2, height / 6)

        mouse = pygame.mouse.get_pos()

        btn_x_start, btn_y_start = width / 10, height / 6 * 3
        btn_width, btn_height = width / 6 * 5, height / 12
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'return_to_main',
                    mouse_click_down, 'Вернуться на начало', colors['white'], 20,
                    btn_x_start + btn_width / 2, btn_y_start + btn_height / 2, width=width, height=height)

        pygame.display.update()
        clock.tick(20)


def handle_quit():
    pygame.quit()
    quit()


def display_btn(display, mouse, pos, color_before, color_during, action, clicked, text, text_color, font_size,
                text_x_center, text_y_center, **kwargs):

    handler_btn(display, mouse, pos, color_before, color_during, action, clicked, **kwargs)
    display_text(display, text, text_color, font_size, text_x_center, text_y_center)
