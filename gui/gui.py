from datetime import date, datetime

import pygame
import pygame_gui
from dateutil.relativedelta import relativedelta

from colors_constant import web_colors as colors
from config import MONGO_DB_NAME, MONGO_DB_HOST, MONGO_DB_USER, MONGO_DB_PASSWORD, BASE_SEISMIC_COLLECTION
from db import DBClient
from gui.handlers import count_of_state, avg_mag, show_map
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
        division = 7
        display_text(display, 'Выберите действие', colors['black'], 30, width / 2, height / division * count)
        ####

        mouse = pygame.mouse.get_pos()
        ####
        count += 1
        btn_x_start, btn_y_start = width / 10, height / division * count
        btn_width, btn_height = width / 6 * 5, height / 12
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'state_statistic',
                    mouse_click_down, 'Количество сейсмических активностей по странам/штатам c 10-03-2020',
                    colors['white'], 20, btn_x_start + btn_width / 2, btn_y_start + btn_height / 2,
                    client=client, splot=splot)

        ####
        count += 1
        btn_y_start = height / division * count
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'show_map',
                    mouse_click_down, 'Отобразить на карте последние сейсмические активности', colors['white'],
                    20, btn_x_start + btn_width / 2, btn_y_start + btn_height / 2,
                    client=client, splot=splot)
        ####
        count += 1
        btn_y_start = height / division * count
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'avg_mag',
                    mouse_click_down, 'Средняя магнитуда по дням (за последние 50 дней) по странам/штатам',
                    colors['white'], 20, btn_x_start + btn_width / 2, btn_y_start + btn_height / 2,
                    client=client, splot=splot, width=width, height=height)
        ####
        count += 1
        btn_y_start = height / division * count
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'ai_today_mag',
                    mouse_click_down, 'Вероятная средняя магнитуда на сегодняшний день (Машинное обучение)',
                    colors['white'], 20, btn_x_start + btn_width / 2, btn_y_start + btn_height / 2,
                    width=width, height=height, client=client)
        ####
        count += 1
        btn_y_start = height / division * count
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'quit',
                    mouse_click_down, 'Завершить', colors['white'], 20,
                    btn_x_start + btn_width / 2, btn_y_start + btn_height / 2)
        ####

        pygame.display.update()
        clock.tick(20)

    handle_quit()


def handler_btn(display, mouse, pos, color_before, color_during, action=None, mouse_click=False, **kwargs):
    click = pygame.mouse.get_pressed()

    action_dict = {
        'state_statistic': count_of_state,
        # 'avg_mag': avg_mag,
        'avg_mag': select_country,
        'ai_today_mag': ai_today_mag,
        'return_to_main': start_app,
        'quit': handle_quit,
        'show_map': show_map,
        'country_avg': country_avg,
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
        text = [f'Сегодня {date.today().strftime("%d-%m-%Y")} средняя магнитуда', f'будет составлять {str(data)}']
        for num, elem in enumerate(text):
            display_text(display, elem, colors['black'], 30, width / 2, height / 6 + num * 50)

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


def select_country(client, splot, start=datetime(2020, 3, 10), end=datetime.today(), **kwargs):
    data = client.get_data_by_range_date(start, end, 'place', 'coord', 'time')

    width = kwargs['width']
    height = kwargs['height']

    display = pygame.display.set_mode((width, height))

    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((800, 600))

    all_countries = []
    for row in data:
        state = row['place'].split(', ')[-1]
        all_countries.append(state)
    all_countries = list(sorted(set(all_countries)))

    default_text = '---'
    drop_down_menu = pygame_gui.elements.UIDropDownMenu(
        all_countries, starting_option=default_text, manager=manager,
        relative_rect=pygame.Rect((width / 8 * 2, height / 6 * 2), (width / 2, height / 12))
    )

    active = True
    while active:
        time_delta = clock.tick(30) / 1000.0
        events = pygame.event.get()
        events_type = [event.type for event in events]

        quit_was_happen = pygame.QUIT in events_type
        if quit_was_happen:
            handle_quit()

        for event in events:
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == drop_down_menu:
                        default_text = event.text

            manager.process_events(event)

        manager.update(time_delta)

        mouse_click_down = pygame.MOUSEBUTTONDOWN in events_type

        display.fill(colors['bisque'])

        text = ['Выберите страну (или штат), чтобы отобразить', 'последние сейсмические активности в стране/штате']
        for num, elem in enumerate(text):
            display_text(display, elem, colors['black'], 30, width / 2, height / 6 + num * 50)

        mouse = pygame.mouse.get_pos()

        btn_x_start, btn_y_start = width / 10, height / 7 * 5
        btn_width, btn_height = width / 6 * 5, height / 12

        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'country_avg',
                    mouse_click_down, 'Отобразить средние значения магнитуды по дням', colors['white'], 20,
                    btn_x_start + btn_width / 2, btn_y_start + btn_height / 2,
                    client=client, splot=splot, country_name=default_text)

        btn_y_start = height / 7 * 6
        btn_position = (btn_x_start, btn_y_start, btn_width, btn_height)

        display_btn(display, mouse, btn_position, colors['blackmagic'], colors['knightsarmor'], 'return_to_main',
                    mouse_click_down, 'Вернуться на начало', colors['white'], 20,
                    btn_x_start + btn_width / 2, btn_y_start + btn_height / 2, width=width, height=height)

        manager.draw_ui(display)
        pygame.display.update()


def country_avg(client, splot, country_name):
    if country_name != '---':
        start = datetime.today() - relativedelta(days=50)
        end = datetime.today()
        data = client.get_data_by_range_date(start, end, 'time', 'mag', 'place')

        new_data = []
        for row in data:
            if row['place'].endswith(country_name):
                new_data.append(row)

        avg_mag(client, splot, data=new_data)
