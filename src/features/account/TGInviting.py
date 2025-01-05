# -*- coding: utf-8 -*-
import asyncio
import datetime

import aioschedule
import flet as ft  # Импортируем библиотеку flet
from loguru import logger
from telethon.errors import (AuthKeyDuplicatedError, PeerFloodError, FloodWaitError, UserPrivacyRestrictedError,
                             UserChannelsTooMuchError, BotGroupsBlockedError, ChatWriteForbiddenError,
                             UserBannedInChannelError, UserNotMutualContactError, ChatAdminRequiredError,
                             UserKickedError, ChannelPrivateError, UserIdInvalidError, UsernameNotOccupiedError,
                             UsernameInvalidError, InviteRequestSentError, TypeNotFoundError, SessionRevokedError,
                             UserDeactivatedBanError)
from telethon.tl.functions.channels import InviteToChannelRequest

from src.core.configs import ConfigReader, path_inviting_folder, line_width_button, height_button
from src.core.localization import back_button, start_inviting_button
from src.core.sqlite_working_tools import DatabaseHandler
from src.core.utils import record_and_interrupt, record_inviting_results, find_filess
from src.features.account.TGChek import TGChek
from src.features.account.TGConnect import TGConnect
from src.features.account.TGLimits import SettingLimits
from src.features.account.TGSubUnsub import SubscribeUnsubscribeTelegram
from src.gui.menu import log_and_display, show_notification


class InvitingToAGroup:

    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.sub_unsub_tg = SubscribeUnsubscribeTelegram()
        self.limits_class = SettingLimits()
        self.tg_connect = TGConnect()
        self.config_reader = ConfigReader()
        self.time_inviting = self.config_reader.get_time_inviting()
        self.hour, self.minutes = self.config_reader.get_hour_minutes_every_day()

    async def getting_an_invitation_link_from_the_database(self):
        """"
        Получение ссылки для инвайтинга
        """
        try:
            links_inviting: list = await self.db_handler.open_and_read_data("links_inviting")  # Открываем базу данных
            logger.info(f"Ссылка для инвайтинга:  {links_inviting}")
            return links_inviting
        except Exception as error:
            logger.exception(f"Ошибка: {error}")

    @staticmethod
    async def log_and_display(message: str, lv, page: ft.Page):
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

    async def inviting_without_limits(self, page: ft.Page, account_limits) -> None:
        """
        Инвайтинг без лимитов. Группа для инвайтинга выбирается из выпадающего списка. Информация о работе выводится
        в графический интерфейс и записывается в лог файл.

        Аргументы:
        :param account_limits: Таблица с лимитами
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """

        lv = ft.ListView(expand=10, spacing=1, padding=2, auto_scroll=True)
        page.controls.append(lv)  # добавляем ListView на страницу для отображения логов 📝
        page.update()  # обновляем страницу, чтобы сразу показать ListView 🔄

        links_inviting = await self.getting_an_invitation_link_from_the_database()  # Получение ссылки для инвайтинга

        async def add_items(_):
            """
            🚀 Запускает процесс инвайтинга групп и отображает статус в интерфейсе.
            """
            start = datetime.datetime.now()  # фиксируем время начала выполнения кода ⏱️
            # Индикация начала инвайтинга
            await log_and_display(f"▶️ Начало инвайтинга.\n🕒 Время старта: {str(start)}", lv, page)
            page.update()  # Обновите страницу, чтобы сразу показать сообщение 🔄
            try:
                for session_name in find_filess(directory_path=path_inviting_folder, extension='session'):
                    client = await self.tg_connect.get_telegram_client(page, session_name,
                                                                       account_directory=path_inviting_folder)
                    logger.info(f"{dropdown.value}")
                    # Подписка на группу для инвайтинга
                    await self.sub_unsub_tg.subscribe_to_group_or_channel(client, dropdown.value)
                    # Получение списка usernames
                    number_usernames = await self.limits_class.get_usernames_with_limits(table_name="members",
                                                                                         account_limits=account_limits)
                    if len(number_usernames) == 0:
                        await log_and_display(f"В таблице members нет пользователей для инвайтинга", lv, page)
                        await self.sub_unsub_tg.unsubscribe_from_the_group(client, dropdown.value)
                        break  # Прерываем работу и меняем аккаунт
                    for username in number_usernames:
                        await log_and_display(f"Пользователь username:{username[0]}", lv, page)
                        # Инвайтинг в группу по полученному списку

                        try:
                            await log_and_display(f"Попытка приглашения {username[0]} в группу {dropdown.value}.", lv,
                                                  page)
                            await client(InviteToChannelRequest(dropdown.value, [username[0]]))
                            await log_and_display(f"Удачно! Спим 5 секунд", lv, page)
                            await asyncio.sleep(5)
                        # Ошибка инвайтинга продолжаем работу
                        except UserChannelsTooMuchError:
                            await log_and_display(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. Превышен лимит у user каналов / супергрупп.",
                                lv, page)
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                        except UserNotMutualContactError:
                            await log_and_display(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. User не является взаимным контактом.",
                                lv, page)
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                        except (UserKickedError, UserDeactivatedBanError):
                            await log_and_display(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. Пользователь был удален ранее из супергруппы или забанен.",
                                lv, page)
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                        except (UserIdInvalidError, UsernameNotOccupiedError, ValueError, UsernameInvalidError):
                            logger.error(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. Не корректное имя {username}")
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                        except ChatAdminRequiredError:
                            logger.error(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. Требуются права администратора.")
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                        except UserPrivacyRestrictedError:
                            logger.error(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. Настройки конфиденциальности {username} не позволяют вам inviting")
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                        except BotGroupsBlockedError:
                            logger.error(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. Вы не можете добавить бота в группу.")
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                        except (TypeError, UnboundLocalError):
                            logger.error(f"❌ Попытка приглашения {username} в группу {dropdown.value}")
                        # Ошибка инвайтинга прерываем работу
                        except ChatWriteForbiddenError:
                            logger.error(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. Настройки в чате не дают добавлять людей в чат, возможно стоит бот админ и нужно подписаться на другие проекты")
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                            break  # Прерываем работу и меняем аккаунт
                        except InviteRequestSentError:
                            logger.error(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. Доступ к функциям группы станет возможен после утверждения заявки администратором на {dropdown.value}")
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                            break  # Прерываем работу и меняем аккаунт
                        except (ChannelPrivateError, TypeNotFoundError, AuthKeyDuplicatedError,
                                UserBannedInChannelError, SessionRevokedError):
                            await record_and_interrupt(self.time_inviting[0], self.time_inviting[1])
                            break  # Прерываем работу и меняем аккаунт
                        except FloodWaitError as error:
                            logger.error(f'{error}')
                            await record_and_interrupt(self.time_inviting[0], self.time_inviting[1])
                            break  # Прерываем работу и меняем аккаунт
                        except PeerFloodError:
                            logger.error(
                                f"❌ Попытка приглашения {username} в группу {dropdown.value}. Настройки конфиденциальности {username} не позволяют вам inviting")
                            await record_and_interrupt(self.time_inviting[0], self.time_inviting[1])
                            break  # Прерываем работу и меняем аккаунт
                        except KeyboardInterrupt:  # Закрытие окна программы
                            client.disconnect()  # Разрываем соединение telegram
                            await log_and_display(f"[!] Скрипт остановлен!", lv, page)
                        except Exception as error:
                            logger.exception(f"❌ Ошибка: {error}")
                        else:
                            logger.info(f"[+] Участник {username} добавлен, если не состоит в чате {dropdown.value}")
                            await record_inviting_results(self.time_inviting[0], self.time_inviting[1], username)
                    await self.sub_unsub_tg.unsubscribe_from_the_group(client, dropdown.value)
                logger.info("[!] Инвайтинг окончен!")
            except Exception as error:
                logger.exception(f"❌ Ошибка: {error}")
            finish = datetime.datetime.now()  # фиксируем время окончания парсинга ⏰
            await log_and_display(
                f"🔚 Конец инвайтинга.\n🕒 Время окончания: {finish}.\n⏳ Время работы: {finish - start}", lv, page)
            await show_notification(page, "🔚 Конец инвайтинга")  # Выводим уведомление пользователю
            page.go("/inviting")  # переходим к основному меню инвайтинга 🏠

        async def back_button_clicked(_):
            """
            ⬅️ Обрабатывает нажатие кнопки "Назад", возвращая в меню инвайтинга.
            """
            page.go("/inviting")  # переходим к основному меню инвайтинга 🏠

        # Создаем выпадающий список с названиями групп
        dropdown = ft.Dropdown(width=line_width_button,
                               options=[ft.dropdown.Option(link[0]) for link in links_inviting],
                               autofocus=True)

        result_text = ft.Text(value="📂 Выберите группу для инвайтинга")

        # Добавляем кнопки и другие элементы управления на страницу
        page.views.append(
            ft.View(
                "/inviting",
                [
                    lv,  # Отображение логов 📝
                    result_text,  # Выбор группы для инвайтинга
                    dropdown,  # Выпадающий список с названиями групп
                    ft.Column(),  # Резерв для приветствия или других элементов интерфейса
                    ft.ElevatedButton(width=line_width_button, height=height_button, text=start_inviting_button,
                                      on_click=add_items),  # Кнопка "🚀 Начать инвайтинг"
                    ft.ElevatedButton(width=line_width_button, height=height_button, text=back_button,
                                      on_click=back_button_clicked)  # Кнопка "⬅️ Назад"
                ],
            )
        )

        page.update()  # обновляем страницу после добавления элементов управления 🔄

    @staticmethod
    async def run_scheduler():
        """
        Функция для запуска планировщика задач в бесконечном цикле.

        Планировщик проверяет наличие задач для выполнения и запускает их по расписанию.
        """
        while True:
            await aioschedule.run_pending()  # Выполнение всех задач, которые должны запуститься в текущее время
            await asyncio.sleep(1)  # Пауза для предотвращения избыточного использования ресурсов

    async def schedule_member_invitation(self, page: ft.Page) -> None:
        """
        Запуск приглашения участников в группу.

        Аргументы:
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        try:
            # Проверка валидности учетной записи Telegram
            await TGChek().validation_check(page=page)
            # Запуск приглашения участников без ограничений
            await self.inviting_without_limits(page=page, account_limits=ConfigReader().get_limits())
        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")

    async def launching_invite_every_day_certain_time(self, page: ft.Page) -> None:
        """
        Запуск приглашения участников каждый день в определенное время, выбранное пользователем.

        Аргументы:
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        try:
            # Настройка ежедневного выполнения задачи в указанное время
            aioschedule.every().day.at(f"{int(self.hour):02d}:{int(self.minutes):02d}").do(
                self.schedule_member_invitation,
                page=page)
            # Запуск планировщика задач
            await self.run_scheduler()
        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")

    async def launching_an_invite_once_an_hour(self, page: ft.Page) -> None:
        """
        Запуск приглашения участников 1 раз в час.

        Аргументы:
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        try:
            logger.info("Запуск программы в 00 минут каждого часа")
            # Настройка выполнения задачи каждый час на 00 минут
            aioschedule.every().hour.at(":00").do(self.schedule_member_invitation, page=page)
            # Запуск планировщика задач
            await self.run_scheduler()
        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")

    async def schedule_invite(self, page: ft.Page) -> None:
        """
        Запуск автоматической отправки приглашений участникам каждый день в определенное время.

        Аргументы:
        :param page: Страница интерфейса Flet для отображения элементов управления.
        """
        try:
            logger.info(f"Скрипт будет запускаться каждый день в {self.hour}:{self.minutes}")
            # Запускаем автоматизацию
            aioschedule.every().day.at(f"{self.hour}:{self.minutes}").do(self.schedule_member_invitation, page=page)
            await self.run_scheduler()  # Здесь мы блокируем выполнение, ожидая задач.
        except Exception as error:
            logger.exception(f"❌ Ошибка: {error}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_forever()
