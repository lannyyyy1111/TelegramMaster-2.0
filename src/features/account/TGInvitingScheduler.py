# -*- coding: utf-8 -*-
import asyncio

import aioschedule
from loguru import logger

from src.features.account.TGChek import TGChek
from src.features.account.TGInviting import InvitingToAGroup
from src.core.configs import ConfigReader

hour, minutes = ConfigReader().get_hour_minutes_every_day()


async def run_scheduler():
    """
    Функция для запуска планировщика.
    """
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def schedule_member_invitation(page) -> None:
    """
    Запуск inviting

    Аргументы:
    :param page: Страница интерфейса Flet для отображения элементов управления.
    """
    try:
        await TGChek().validation_check(page=page)
        await InvitingToAGroup().inviting_without_limits(page=page, account_limits=ConfigReader().get_limits())
    except Exception as error:
        logger.exception(f"❌ Ошибка: {error}")


async def launching_invite_every_day_certain_time(page) -> None:
    """
    Запуск inviting каждый день в определенное время выбранное пользователем

    Аргументы:
    :param page: Страница интерфейса Flet для отображения элементов управления.
    """
    try:
        aioschedule.every().day.at(f"{int(hour):02d}:{int(minutes):02d}").do(schedule_member_invitation, page=page)
        await run_scheduler()  # Здесь мы блокируем выполнение, ожидая задач.
    except Exception as error:
        logger.exception(f"❌ Ошибка: {error}")


async def launching_an_invite_once_an_hour(page) -> None:
    """
    Запуск inviting 1 раз в час

    Аргументы:
    :param page: Страница интерфейса Flet для отображения элементов управления.
    """
    try:
        logger.info("Запуск программы в 00 минут")
        aioschedule.every().hour.at(":00").do(schedule_member_invitation, page=page)
        await run_scheduler()  # Здесь мы блокируем выполнение, ожидая задач.
    except Exception as error:
        logger.exception(f"❌ Ошибка: {error}")


async def schedule_invite(page) -> None:
    """
    Запуск автоматической отправки приглашений участникам

    Аргументы:
    :param page: Страница интерфейса Flet для отображения элементов управления.
    """
    try:
        logger.info(f"Скрипт будет запускаться каждый день в {hour}:{minutes}")
        # Запускаем автоматизацию
        aioschedule.every().day.at(f"{hour}:{minutes}").do(schedule_member_invitation, page=page)
        await run_scheduler()  # Здесь мы блокируем выполнение, ожидая задач.
    except Exception as error:
        logger.exception(f"❌ Ошибка: {error}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_forever()
