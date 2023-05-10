# -*- coding: utf-8 -*-
import random
import time
from tkinter import *

from rich import print
from rich.progress import track
from telethon.errors import *
from telethon.tl.functions.channels import JoinChannelRequest

from system.auxiliary_functions.auxiliary_functions import creating_and_writing_to_a_temporary_file, \
    record_and_interrupt
from system.auxiliary_functions.auxiliary_functions import deleting_files_if_available
from system.auxiliary_functions.global_variables import time_subscription_1
from system.auxiliary_functions.global_variables import time_subscription_2
from system.error.telegram_errors import record_account_actions
from system.menu.baner import program_version, date_of_program_change
from system.notification.notification import app_notifications
from system.sqlite_working_tools.sqlite_working_tools import open_the_db_and_read_the_data
from system.sqlite_working_tools.sqlite_working_tools import write_data_to_db
from system.telegram_actions.telegram_actions import connect_to_telegram_account_and_output_name

creating_a_table = """SELECT * from writing_group_links"""
writing_data_to_a_table = """DELETE from writing_group_links where writing_group_links = ?"""


def writing_group_links_to_file() -> None:
    """Запускаем окно программы (большого поля ввода)"""
    print("[bold red][+] Введите ссылки чатов на которые нужно подписаться, для вставки в графическое окно "
          "используйте комбинацию клавиш Ctrl + V, обратите внимание что при использование комбинации язык должен "
          "быть переключен на английский")
    root = Tk()  # Создаем программу
    root.title(f"Telegram_BOT_SMM: {program_version} от {date_of_program_change}")
    # Создаем окно ввода текста, width=50, height=25 выбираем размер программы
    text = Text(width=50, height=25)
    text.pack()  # Создаем поле ввода

    def output_values_from_the_input_field() -> None:
        """Выводим значения с поля ввода (то что ввел пользователь)"""
        message_text = text.get("1.0", 'end-1c')
        closing_the_input_field()
        folder_name, files = "setting_user", "members_group.csv"
        creating_and_writing_to_a_temporary_file(folder_name, files, message_text)
        deleting_files_if_available(folder_name, files)  # Удаляем файл после работы

    def closing_the_input_field() -> None:
        """Закрываем программу"""
        root.destroy()

    # Создаем кнопку по нажатии которой выведется поле ввода. После ввода чатов данные запишутся во временный файл
    but = Button(root, text="Готово", command=output_values_from_the_input_field)
    but.pack()
    root.mainloop()  # Запускаем программу


def subscription_all() -> None:
    """Подписываемся на каналы и группы, работаем по базе данных"""
    # Открываем базу данных для работы с аккаунтами setting_user/software_database.db
    records: list = open_the_db_and_read_the_data(name_database_table="config")
    print(f"[bold red]Всего accounts: {len(records)}")
    for row in track(records, description='[bold red]Прогресс выполнения работы\n'):
        # Подключение к Telegram и вывод имя аккаунта в консоль / терминал
        client, phone = connect_to_telegram_account_and_output_name(row)
        # Открываем базу данных
        records: list = open_the_db_and_read_the_data(name_database_table="writing_group_links")
        print(f"[bold red]Всего групп: {len(records)}")
        for groups in records:  # Поочередно выводим записанные группы
            try:
                groups_wr = subscribe_to_the_group_and_send_the_link(client, groups, phone)
                print(f"[bold red][+] Присоединился к группе или чату {groups_wr}")
                print(f"[bold green][+] Подождите {time_subscription_1}-{time_subscription_2} Секунд...")
                time.sleep(random.randrange(int(time_subscription_1), int(time_subscription_2)))
            # Переносим FloodWaitError в функцию подписки для избежания срабатывания в других функциях программы
            except FloodWaitError as e:
                print(f'Flood! wait for {e.seconds} seconds')
                print(f'Спим {e.seconds} секунд')
                time.sleep(e.seconds)
        client.disconnect()  # Разрываем соединение Telegram
    # Выводим уведомление, если операционная система windows 7, то выводим уведомление в консоль
    app_notifications(notification_text="На группы подписались!")


def subscribe_to_group_or_channel(client, groups_wr, phone) -> None:
    """Подписываемся на группу или канал"""
    actions: str = "Подписался на группу или чат, если ранее не был подписан"
    event: str = f"Subscription: {groups_wr}"
    description_action = f"channel / group: {groups_wr}"
    # цикл for нужен для того, что бы сработала команда brake
    # команда break в Python используется только для выхода из цикла, а не выхода из программы в целом.
    groups_wra = [groups_wr]
    for groups_wrs in groups_wra:
        try:
            client(JoinChannelRequest(groups_wrs))
            print(f"[green] Аккаунт подписался на группу: {groups_wrs}")
            # Записываем данные о действии аккаунта в базу данных
            record_account_actions(phone, description_action, event, actions)
        except ChannelsTooMuchError:
            """Если аккаунт подписан на множество групп и каналов, то отписываемся от них"""
            for dialog in client.iter_dialogs():
                print(f"[green]{dialog.name}, {dialog.id}")
                client.delete_dialog(dialog)
                client.disconnect()
            print('[green][+] Список почистили, и в файл записали.')
        except ChannelPrivateError:
            actions: str = "Указанный канал является приватным, или вам запретили подписываться."
            record_account_actions(phone, description_action, event, actions)
        except (UsernameInvalidError, ValueError, TypeError):
            actions: str = f"Не верное имя или cсылка {groups_wrs} не является группой / каналом: {groups_wrs}"
            record_account_actions(phone, description_action, event, actions)
            write_data_to_db(creating_a_table, writing_data_to_a_table, groups_wrs)
        except PeerFloodError:
            actions: str = "Предупреждение о Flood от Telegram."
            record_account_actions(phone, description_action, event, actions)
            time.sleep(random.randrange(50, 60))
        except FloodWaitError as e:
            actions: str = f'Flood! wait for {e.seconds} seconds'
            print(f"[red][!] {actions}")
            record_and_interrupt(actions, phone, description_action, event)
            break  # Прерываем работу и меняем аккаунт
        except InviteRequestSentError:
            actions: str = "Действия будут доступны после одобрения администратором на вступление в группу"
            record_account_actions(phone, description_action, event, actions)


def subscribe_to_the_group_and_send_the_link(client, groups, phone):
    """Подписываемся на группу и передаем ссылку"""
    group = {'writing_group_links': groups[0]}
    # Вытягиваем данные из кортежа, для подстановки
    groups_wr = group['writing_group_links']
    subscribe_to_group_or_channel(client, groups_wr, phone)
    return groups_wr


if __name__ == "__main__":
    subscription_all()
    writing_group_links_to_file()
