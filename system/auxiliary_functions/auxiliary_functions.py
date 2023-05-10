# -*- coding: utf-8 -*-
import os
import os.path
import platform
import random  # Импортируем модуль random, чтобы генерировать случайное число
import time  # Импортируем модуль time, чтобы работать с временем
from sys import platform

from rich import print
from rich.progress import track

from system.auxiliary_functions.global_variables import time_inviting_1, time_changing_accounts_1, \
    time_changing_accounts_2, time_inviting_2
from system.error.telegram_errors import record_account_actions
from system.menu.baner import banner
from system.sqlite_working_tools.sqlite_working_tools import open_the_db_and_read_the_data, delete_row_db
from system.sqlite_working_tools.sqlite_working_tools import write_to_single_column_table


def display_progress_bar(time_range_1, time_range_2, message):
    """Отображаем время смены аккаунта или username в виде progress bar"""
    # Генерируем случайное число в указанном диапазоне времени
    selected_shift_time = random.randrange(time_range_1, time_range_2)
    for _ in track(range(selected_shift_time),
                   description=f"[red]{message} через {selected_shift_time} секунды/секунд..."):
        time.sleep(1)


def record_inviting_results(username, phone, description_action, event, actions) -> None:
    """Запись результатов inviting, отправка сообщений в базу данных"""
    record_account_actions(phone, description_action, event, actions)
    delete_row_db(table="members", column="id", value=username['id'])
    # Смена username через случайное количество секунд
    display_progress_bar(time_inviting_1, time_inviting_2, "Переход к новому username")


def record_and_interrupt(actions, phone, description_action, event):
    """Запись данных в базу данных и прерывание выполнения кода"""
    record_account_actions(phone, description_action, event, actions)
    # Смена аккаунта через случайное количество секунд
    display_progress_bar(time_changing_accounts_1, time_changing_accounts_2, "Ожидайте смены аккаунта")


def deleting_files_if_available(folder, file) -> None:
    """Удаление список groups_and_channels"""
    try:
        os.remove(f'{folder}/{file}')
    except FileNotFoundError:
        print(f"[green]Файл {file} был ранее удален")


def clearing_console_showing_banner() -> None:
    """Чистим консоль, выводим банер"""
    if platform == 'win32':
        os.system("cls")  # Чистим консоль (для windows cls)
    else:
        os.system("clear")  # Чистим консоль (для linux clear)
    banner()  # Ставим банер программы, для красивого визуального отображения


def creating_and_writing_to_a_temporary_file(folder_name, files, text) -> None:
    """Создание и запись во временный файл"""
    # Печатаем переменную в консоль
    with open(f'{folder_name}/{files}', "w") as res_as:
        res_as.write(text)
    with open(f'{folder_name}/{files}', 'r') as recorded_data:  # Записываем данные с файла в базу данных
        name_database = "writing_group_links"
        open_the_db_and_read_the_data(name_database)  # Запись ссылок в базу данных
        write_to_single_column_table(name_database, recorded_data)


def column_names(table) -> None:
    """Название столбцов, для меню программы"""
    table.add_column("[bold red]№ функции", justify="center", style="cyan")
    table.add_column("[bold red]Функция", justify="left", style="green")
    table.add_column("[bold red]Описание", justify="left", style="cyan")


if __name__ == "__main__":
    clearing_console_showing_banner()
