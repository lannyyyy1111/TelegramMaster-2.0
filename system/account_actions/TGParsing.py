# -*- coding: utf-8 -*-
import datetime
import time

import flet as ft  # Импортируем библиотеку flet
from loguru import logger
from telethon import functions
from telethon import types
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import (ChannelParticipantsSearch, InputPeerEmpty, UserStatusEmpty, UserStatusLastMonth,
                               UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently)

from system.account_actions.TGConnect import TGConnect
from system.account_actions.TGSubUnsub import SubscribeUnsubscribeTelegram
from system.auxiliary_functions.auxiliary_functions import find_filess
from system.auxiliary_functions.config import (path_parsing_folder, line_width_button, height_button,
                                               time_activity_user_2)
from system.sqlite_working_tools.sqlite_working_tools import DatabaseHandler


class ParsingGroupMembers:
    """Парсинг групп"""

    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.tg_connect = TGConnect()
        self.sub_unsub_tg = SubscribeUnsubscribeTelegram()

    async def clean_parsing_list_and_remove_duplicates(self):
        """Очищает список парсинга от записей без имени пользователя и удаляет дубликаты по идентификатору."""
        # Очистка списка парсинга от записей без имени пользователя
        await self.db_handler.remove_records_without_username()
        # Удаление дублирующихся записей по идентификатору
        await self.db_handler.remove_duplicate_ids(table_name="members", column_name="id")

    async def log_and_display(self, message: str, lv, page):
        """
        Выводит сообщение в GUI и записывает лог.

        Аргументы:
        :param message: Текст сообщения для отображения и записи в лог.
        :param lv: ListView для отображения сообщений.
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        logger.info(message)  # записываем сообщение в лог
        lv.controls.append(ft.Text(message))  # отображаем сообщение в ListView
        page.update()  # обновляем страницу для отображения нового сообщения

    async def parse_groups(self, page: ft.Page) -> None:
        """
        Запускает процесс парсинга групп Telegram и отображает статус процесса в GUI.

        Аргументы:
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        start = datetime.datetime.now()  # фиксируем время начала выполнения кода
        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)  # добавляем ListView на страницу для отображения логов
        page.update()  # обновляем страницу, чтобы сразу показать ListView

        async def add_items(e):
            """
            Запускает процесс парсинга групп и отображает статус в интерфейсе.
            """
            # Индикация начала парсинга
            await self.log_and_display(f"▶️ Начало парсинга.\nВремя старта: {str(start)}", lv, page)
            page.update()  # Обновите страницу, чтобы сразу показать сообщение

            try:
                # Обрабатываем все файлы сессий по очереди
                for session_name in find_filess(directory_path=path_parsing_folder, extension='session'):
                    client = await self.tg_connect.get_telegram_client(session_name,
                                                                       account_directory=path_parsing_folder)
                    # Получаем список групп для парсинга из базы данных
                    for groups in await self.db_handler.open_and_read_data("writing_group_links"):
                        await self.log_and_display(f'[+] Парсинг группы: {groups[0]}', lv, page)
                        await self.sub_unsub_tg.subscribe_to_group_or_channel(client,
                                                                              groups[0])  # подписываемся на группу
                        await self.parse_group(client, groups[0], lv, page)  # выполняем парсинг группы
                        # Удаляем группу из списка после завершения парсинга
                        await self.db_handler.delete_row_db(table="writing_group_links", column="writing_group_links",
                                                            value=groups)
                    # Очищаем список и удаляем дубликаты после завершения обработки всех групп
                    await self.clean_parsing_list_and_remove_duplicates()
                    # Завершаем работу клиента после завершения парсинга
                    await client.disconnect()
            except Exception as e:
                logger.exception(f"Ошибка: {e}")  # логируем исключения

            finish = datetime.datetime.now()  # фиксируем время окончания парсинга
            # Логируем и отображаем время окончания работы
            await self.log_and_display(f"🔚 Конец парсинга.\nВремя окончания: {finish}.\nВремя работы: {finish - start}", lv, page)
            # page.update()  # Обновите страницу, чтобы сразу показать сообщение

        async def back_button_clicked(e):
            """
            Обрабатывает нажатие кнопки "Назад", возвращая в меню парсинга.
            """
            page.go("/parsing")  # переходим к основному меню парсинга

        # Добавляем кнопки и другие элементы управления на страницу
        page.views.append(
            ft.View(
                "/parsing",
                [
                    lv,  # отображение логов
                    ft.Column(),  # резерв для приветствия или других элементов интерфейса
                    ft.ElevatedButton(width=line_width_button, height=height_button, text="Начать парсинг",
                                      on_click=add_items),  # Кнопка "Начать парсинг"
                    ft.ElevatedButton(width=line_width_button, height=height_button, text="Назад",
                                      on_click=back_button_clicked)  # Кнопка "Назад"
                ],
            )
        )

        page.update()  # обновляем страницу после добавления элементов управления

    async def parse_group(self, client, groups_wr, lv, page) -> None:
        """
        Эта функция выполняет парсинг групп, на которые пользователь подписался. Аргумент phone используется декоратором
        @handle_exceptions для отлавливания ошибок и записи их в базу данных user_settings/software_database.db.
        :param client: Клиент Telegram
        :param groups_wr: ссылка на группу
        :param lv: ListView
        :param page: страница
        """
        try:
            logger.info(f"[+] Спарсили данные с группы {groups_wr}")
            lv.controls.append(ft.Text(f"[+] Спарсили данные с группы {groups_wr}"))
            page.update()  # Обновление страницы для каждого элемента данных
            # Записываем parsing данные в файл user_settings/software_database.db
            entities: list = await self.get_all_participants(await self.parse_users(client, groups_wr, lv, page), lv,
                                                             page)
            await self.db_handler.write_parsed_chat_participants_to_db(entities)
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def parse_active_users(self, chat_input, limit_active_user) -> None:
        """
        Parsing участников, которые пишут в чат (активных участников)
        :param chat_input: ссылка на чат
        :param limit_active_user: лимит активных участников
        """
        try:
            for session_name in find_filess(directory_path=path_parsing_folder, extension='session'):
                client = await self.tg_connect.get_telegram_client(session_name,
                                                                   account_directory=path_parsing_folder)
                await self.sub_unsub_tg.subscribe_to_group_or_channel(client, chat_input)
                time.sleep(int(time_activity_user_2))
                await self.get_active_users(client, chat_input, limit_active_user)
                await client.disconnect()  # Разрываем соединение telegram
            await self.clean_parsing_list_and_remove_duplicates()
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def parse_subscribed_groups(self) -> None:
        """Parsing групп / каналов на которые подписан аккаунт и сохраняем в файл user_settings/software_database.db"""
        try:
            # Открываем базу данных для работы с аккаунтами user_settings/software_database.db
            for session_name in find_filess(directory_path=path_parsing_folder, extension='session'):
                # Подключение к Telegram и вывод имя аккаунта в консоль / терминал
                client = await self.tg_connect.get_telegram_client(session_name,
                                                                   account_directory=path_parsing_folder)
                logger.info("Parsing групп / каналов на которые подписан аккаунт")
                await self.forming_a_list_of_groups(client)
                await client.disconnect()  # Разрываем соединение telegram
            await self.db_handler.remove_duplicate_ids(table_name="groups_and_channels",
                                                       column_name="id")  # Чистка дубликатов в базе данных
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def get_active_users(self, client, chat, limit_active_user) -> None:
        """
        Получаем данные участников группы которые писали сообщения
        :param client: клиент Telegram
        :param chat: ссылка на чат
        :param limit_active_user: лимит активных участников
        """
        try:
            async for message in client.iter_messages(chat, limit=int(limit_active_user)):
                if message.from_id is not None and hasattr(message.from_id, 'user_id'):
                    from_user = await client.get_entity(message.from_id.user_id)  # Получаем отправителя по ИД
                    entities = await self.get_active_user_data(from_user)
                    logger.info(entities)
                    await self.db_handler.write_parsed_chat_participants_to_db_active(entities)
                else:
                    logger.warning(f"Message {message.id} does not have a valid from_id.")
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def filtering_groups(self, chats):
        """
        Фильтруем группы
        :param chats: список групп
        """
        groups = []
        for chat in chats:
            try:
                if chat.megagroup:
                    groups.append(chat)
            except AttributeError:
                continue  # Игнорируем объекты без атрибута 'megagroup'
        return groups

    async def name_of_the_groups(self, groups):
        """Возвращаем список названий групп"""
        group_names = []  # Создаем новый список для названий групп
        for group in groups:
            logger.info(f"{group}")  # Логируем сам объект группы
            logger.info(f"{group.title}")  # Логируем название группы
            group_names.append(group.title)  # Добавляем название группы в список
        return group_names

    async def choose_and_parse_group(self, page: ft.Page) -> None:
        """
        Выбираем группу из подписанных и запускаем парсинг
        :param page: страница программы
        :return: None
        """
        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)
        try:
            for session_name in find_filess(directory_path=path_parsing_folder, extension='session'):
                client = await self.tg_connect.get_telegram_client(session_name, account_directory=path_parsing_folder)
                chats = []
                last_date = None
                result = await client(
                    GetDialogsRequest(offset_date=last_date, offset_id=0, offset_peer=InputPeerEmpty(), limit=200,
                                      hash=0))
                chats.extend(result.chats)
                groups = await self.filtering_groups(chats)  # Получаем отфильтрованные группы
                group_titles = await self.name_of_the_groups(groups)  # Получаем названия групп
                logger.info(group_titles)
                # Создаем текст для отображения результата
                result_text = ft.Text(value="Выберите группу для парсинга")

                # Обработчик нажатия кнопки выбора группы
                async def handle_button_click(event) -> None:
                    lv.controls.append(ft.Text(f"Выбрана группа: {dropdown.value}"))
                    page.update()  # Обновление страницы для каждого элемента данных
                    await self.parse_group(client, dropdown.value, lv, page)  # Запускаем парсинг выбранной группы
                    await self.clean_parsing_list_and_remove_duplicates()
                    await client.disconnect()
                    # Переходим на экран парсинга только после завершения всех действий
                    page.go("/parsing")

                async def back_button_clicked(e):
                    """Кнопка возврата в меню настроек"""
                    page.go("/parsing")

                # Создаем выпадающий список с названиями групп
                dropdown = ft.Dropdown(width=line_width_button,
                                       options=[ft.dropdown.Option(title) for title in group_titles],
                                       autofocus=True)
                page.views.append(
                    ft.View(
                        "/parsing",
                        [
                            ft.Column(controls=[
                                dropdown,
                                ft.ElevatedButton(width=line_width_button, height=height_button, text="Выбрать группу",
                                                  on_click=handle_button_click),
                                ft.ElevatedButton(width=line_width_button, height=height_button, text="Назад",
                                                  on_click=back_button_clicked),
                                result_text, lv,
                            ])
                        ],
                    )  # Добавляем созданный вид на страницу
                )
                page.update()

        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def parse_users(self, client, target_group, lv, page) -> list:
        """
        Собираем данные user и записываем в файл user_settings/software_database.db (создание нового файла user_settings/software_database.db)
        :param client: клиент Telegram
        :param target_group: группа / канал
        :param lv: ListView
        :param page: страница программы
        :return: список пользователей
        """
        try:
            logger.info("[+] Ищем участников... Сохраняем в файл software_database.db...")
            lv.controls.append(ft.Text("[+] Ищем участников... Сохраняем в файл software_database.db..."))
            page.update()  # Обновление страницы для каждого элемента данных
            all_participants: list = []
            while_condition = True
            my_filter = ChannelParticipantsSearch("")
            offset = 0
            while while_condition:
                try:
                    participants = await client(
                        GetParticipantsRequest(channel=target_group, offset=offset, filter=my_filter,
                                               limit=200, hash=0))
                    all_participants.extend(participants.users)
                    offset += len(participants.users)
                    if len(participants.users) < 1:
                        while_condition = False
                except TypeError:
                    logger.info(
                        f'Ошибка parsing: не верное имя или 🔗 cсылка {target_group} не является группой / каналом: {target_group}')
                    time.sleep(2)
                    break
            return all_participants
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def get_all_participants(self, all_participants, lv, page) -> list:
        """
        Формируем список user_settings/software_database.db
        :param all_participants: список пользователей
        :return: список пользователей
        """
        try:
            entities: list = []  # Создаем словарь
            for user in all_participants:
                await self.get_user_data(user, entities, lv, page)
            return entities  # Возвращаем словарь пользователей
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def get_user_data(self, user, entities, lv, page) -> None:
        """
        Получаем данные пользователя
        :param user: пользователь
        :param entities: список пользователей
        """
        try:
            username, user_phone, first_name, last_name, photos_id, online_at, user_premium = await self.receiving_data(
                user)
            entities.append(
                [username, user.id, user.access_hash, first_name, last_name, user_phone, online_at, photos_id,
                 user_premium])
            lv.controls.append(ft.Text(
                f"{username}, {user.id}, {user.access_hash}, {first_name}, {last_name}, {user_phone}, {online_at}, {photos_id}, {user_premium}"))
            page.update()  # Обновление страницы для каждого элемента данных
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def receiving_data(self, user):
        """Получение парсинг данных"""
        username = user.username if user.username else "NONE"
        user_phone = user.phone if user.phone else "Номер телефона скрыт"
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        photos_id = (
            "Пользователь с фото" if isinstance(user.photo, types.UserProfilePhoto) else "Пользователь без фото")
        online_at = "Был(а) недавно"
        # Статусы пользователя https://core.telegram.org/type/UserStatus
        if isinstance(user.status, (
                UserStatusRecently, UserStatusOffline, UserStatusLastWeek, UserStatusLastMonth, UserStatusOnline,
                UserStatusEmpty)):
            if isinstance(user.status, UserStatusOffline):
                online_at = user.status.was_online
            if isinstance(user.status, UserStatusRecently):
                online_at = "Был(а) недавно"
            if isinstance(user.status, UserStatusLastWeek):
                online_at = "Был(а) на этой неделе"
            if isinstance(user.status, UserStatusLastMonth):
                online_at = "Был(а) в этом месяце"
            if isinstance(user.status, UserStatusOnline):
                online_at = user.status.expires
            if isinstance(user.status, UserStatusEmpty):
                online_at = "статус пользователя еще не определен"
        user_premium = "Пользователь с premium" if user.premium else ""

        return username, user_phone, first_name, last_name, photos_id, online_at, user_premium

    async def get_active_user_data(self, user):
        """
        Получаем данные активного пользователя
        :param user: пользователь
        """
        try:
            username, user_phone, first_name, last_name, photos_id, online_at, user_premium = await self.receiving_data(
                user)
            entity = (
                username, user.id, user.access_hash, first_name, last_name, user_phone, online_at, photos_id,
                user_premium)
            return entity
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def forming_a_list_of_groups(self, client) -> None:
        """
        Формируем список групп
        :param client: клиент
        """
        try:
            async for dialog in client.iter_dialogs():
                try:
                    ch = await client.get_entity(dialog.id)
                    result = await client(functions.channels.GetFullChannelRequest(channel=ch))
                    chs = await client.get_entity(result.full_chat)
                    # Получение количества участников в группе или канале
                    if hasattr(result.full_chat, "participants_count"):
                        members_count = result.full_chat.participants_count
                    else:
                        members_count = 0
                    # Время синтаксического анализа
                    parsing_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    logger.info(
                        f"{dialog.id}, {chs.title}, {result.full_chat.about}, https://t.me/{chs.username}, {members_count}, {parsing_time}")
                    entities = [dialog.id, chs.title, result.full_chat.about, f"https://t.me/{chs.username}",
                                members_count,
                                parsing_time]
                    await self.db_handler.write_data_to_db(
                        creating_a_table="CREATE TABLE IF NOT EXISTS groups_and_channels(id, title, about, link, members_count, parsing_time)",
                        writing_data_to_a_table="INSERT INTO groups_and_channels (id, title, about, link, members_count, parsing_time) VALUES (?, ?, ?, ?, ?, ?)",
                        entities=entities)
                except TypeError:
                    continue  # Записываем ошибку в software_database.db и продолжаем работу
        except Exception as e:
            logger.exception(f"Ошибка: {e}")

    async def entering_data_for_parsing_active(self, page: ft.Page) -> None:
        """
        Функция для ввода данных для парсинга активных пользователей.
        Создает интерфейс с полем ввода для ссылки на чат и количеством сообщений.
        """
        try:
            # Поле для ввода ссылки на чат
            chat_input = ft.TextField(label="Введите ссылку на чат, с которого будем собирать активных:",
                                      multiline=False,
                                      max_lines=1)
            # Поле для ввода количества сообщений
            limit_active_user = ft.TextField(label="Введите количество сообщений, которые будем парсить:",
                                             multiline=False,
                                             max_lines=1)

            async def btn_click(e) -> None:
                """Функция-обработчик для кнопки "Готово"""
                # Логирование введенных данных
                logger.info(f"Ссылка на чат: {chat_input.value}. Количество сообщений: {limit_active_user.value}")
                # Вызов функции для парсинга активных пользователей (функция должна быть реализована)
                await self.parse_active_users(chat_input.value, int(limit_active_user.value))
                # Изменение маршрута на новый (если необходимо)
                page.go("/parsing")
                page.update()  # Обновление страницы для отображения изменений

            async def back_button_clicked(e):
                """Кнопка возврата в меню настроек"""
                page.go("/parsing")

            # Добавление представления на страницу
            page.views.append(
                ft.View(
                    "/parsing",  # Маршрут для этого представления
                    [
                        chat_input,  # Поле ввода ссылки на чат
                        limit_active_user,  # Поле ввода количества сообщений
                        ft.Column(),  # Колонка для размещения других элементов (при необходимости)
                        ft.ElevatedButton(width=line_width_button, height=height_button, text="Готово",
                                          on_click=btn_click),  # Кнопка "Готово"
                        ft.ElevatedButton(width=line_width_button, height=height_button, text="Назад",
                                          on_click=back_button_clicked)  # Кнопка "Назад"
                    ]
                )
            )
        except Exception as e:
            logger.exception(f"Ошибка: {e}")
# TODO сократить не используемый код или повторяющийся 463 - строк
