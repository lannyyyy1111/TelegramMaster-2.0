# -*- coding: utf-8 -*-
import time
import webbrowser
from multiprocessing import Process

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger
from fastapi.staticfiles import StaticFiles
# Импорт необходимых переменных и функций
from system.auxiliary_functions.config import program_name, program_version, date_of_program_change
from system.localization.localization import (parse_selected_user_subscribed_group, parse_single_or_multiple_groups,
                                              parse_active_group_members, clear_previously_parsed_data_list,
                                              parse_account_subscribed_groups_channels, inviting,
                                              invitation_1_time_per_hour, invitation_at_a_certain_time,
                                              inviting_every_day, importing_a_list_of_parsed_data, setting_reactions,
                                              we_are_winding_up_post_views, automatic_setting_of_reactions,
                                              sending_messages_via_chats,
                                              sending_messages_via_chats_with_answering_machine,
                                              sending_files_via_chats, sending_messages_files_via_chats,
                                              sending_personal_messages_with_limits,
                                              sending_files_to_personal_account_with_limits, choice_of_reactions,
                                              proxy_entry, changing_accounts, recording_api_id_api_hash,
                                              time_between_subscriptions, message_recording, link_entry, account_limits,
                                              message_limits, time_between_subscriptionss, creating_username_list,
                                              recording_the_time_between_messages,
                                              time_between_invites_sending_messages, recording_reaction_link,
                                              forming_list_of_chats_channels)

app = FastAPI()

# Указываем путь к статическим файлам
app.mount("/static", StaticFiles(directory="docs/static"), name="static")
templates = Jinja2Templates(directory="docs/templates")  # Указываем директорию с шаблонами.


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница документации"""
    logger.info("Запущена главная страница документации")
    try:
        return templates.TemplateResponse("index.html", {"request": request, "program_name": program_name})
    except Exception as e:
        logger.exception(f"Error rendering the template: {e}")
        return {"error": "Failed to render template"}


@app.get("/menu", response_class=HTMLResponse)
async def menu(request: Request):
    """Меню программы"""
    logger.info("Запущено меню программы")
    return templates.TemplateResponse("menu.html", {"request": request, "program_version": program_version,
                                                    "update_date": date_of_program_change})


@app.get("/inviting", response_class=HTMLResponse)
async def inviting_page(request: Request):
    """🚀 Инвайтинг"""
    logger.info("Запущена страница инвайтинга")
    return templates.TemplateResponse("inviting.html", {"request": request, "program_name": program_name,
                                                        "inviting": inviting,
                                                        "invitation_1_time_per_hour": invitation_1_time_per_hour,
                                                        "invitation_at_a_certain_time": invitation_at_a_certain_time,
                                                        "inviting_every_day": inviting_every_day})


@app.get('/sending_messages', response_class=HTMLResponse)
async def sending_messages(request: Request):
    """💬 Рассылка сообщений"""
    logger.info("Запущено страница рассылки сообщений")
    return templates.TemplateResponse('sending_messages.html', {"request": request, "program_name": program_name,
                                                                "sending_messages_via_chats": sending_messages_via_chats,
                                                                "sending_messages_via_chats_with_answering_machine": sending_messages_via_chats_with_answering_machine,
                                                                "sending_files_via_chats": sending_files_via_chats,
                                                                "sending_messages_files_via_chats": sending_messages_files_via_chats,
                                                                "sending_personal_messages_with_limits": sending_personal_messages_with_limits,
                                                                "sending_files_to_personal_account_with_limits": sending_files_to_personal_account_with_limits})


@app.get('/editing_bio', response_class=HTMLResponse)
async def editing_bio(request: Request):
    """Редактирование БИЛ"""
    logger.info("Запущена страница редактирования БИО")
    return templates.TemplateResponse('editing_bio.html', {"request": request, "program_name": program_name})


@app.get('/working_with_contacts', response_class=HTMLResponse)
async def working_with_contacts(request: Request):
    """Работа с контактами"""
    logger.info("Запущена страница работы с контактами")
    return templates.TemplateResponse('working_with_contacts.html', {"request": request, "program_name": program_name})


@app.get('/settings', response_class=HTMLResponse)
async def settings(request: Request):
    """⚙️ Настройки"""
    logger.info("Запущена страница настроек")
    return templates.TemplateResponse('settings.html', {"request": request, "program_name": program_name,
                                                        "choice_of_reactions": choice_of_reactions,
                                                        "proxy_entry": proxy_entry,
                                                        "changing_accounts": changing_accounts,
                                                        "recording_api_id_api_hash": recording_api_id_api_hash,
                                                        "time_between_subscriptions": time_between_subscriptions,
                                                        "message_recording": message_recording,
                                                        "link_entry": link_entry,
                                                        "account_limits": account_limits,
                                                        "message_limits": message_limits,
                                                        "time_between_subscriptionss": time_between_subscriptionss,
                                                        "creating_username_list": creating_username_list,
                                                        "recording_the_time_between_messages": recording_the_time_between_messages,
                                                        "time_between_invites_sending_messages": time_between_invites_sending_messages,
                                                        "recording_reaction_link": recording_reaction_link,
                                                        "forming_list_of_chats_channels": forming_list_of_chats_channels,
                                                        })


@app.get('/working_with_reactions', response_class=HTMLResponse)
async def working_with_reactions(request: Request):
    """👍 Работа с реакциями"""
    logger.info("Запущена страница работы с реакциями")
    return templates.TemplateResponse('working_with_reactions.html',
                                      {"request": request, "program_name": program_name,
                                       "setting_reactions": setting_reactions,
                                       "we_are_winding_up_post_views": we_are_winding_up_post_views,
                                       "automatic_setting_of_reactions": automatic_setting_of_reactions})


@app.get('/parsing', response_class=HTMLResponse)
async def parsing(request: Request):
    """🔍 Парсинг"""
    logger.info("Запущена страница парсинга")
    return templates.TemplateResponse('parsing.html', {"request": request, "program_name": program_name,
                                                       "parse_single_or_multiple_groups": parse_single_or_multiple_groups,
                                                       "parse_selected_user_subscribed_group": parse_selected_user_subscribed_group,
                                                       "parse_active_group_members": parse_active_group_members,
                                                       "parse_account_subscribed_groups_channels": parse_account_subscribed_groups_channels,
                                                       "clear_previously_parsed_data_list": clear_previously_parsed_data_list,
                                                       "importing_a_list_of_parsed_data": importing_a_list_of_parsed_data})


@app.get('/subscribe_unsubscribe', response_class=HTMLResponse)
async def subscribe_unsubscribe(request: Request):
    """Подписка, отписка"""
    logger.info("Запущена страница подписки, отписки")
    return templates.TemplateResponse('subscribe_unsubscribe.html',
                                      {"request": request, "program_name": program_name})


@app.get('/connect_accounts', response_class=HTMLResponse)
async def connect_accounts(request: Request):
    """Подключение аккаунтов"""
    logger.info("Запущена страница подключения аккаунтов")
    return templates.TemplateResponse('connect_accounts.html',
                                      {"request": request, "program_name": program_name})


@app.get('/account_verification', response_class=HTMLResponse)
async def account_verification(request: Request):
    """Проверка аккаунтов"""
    logger.info("Запущена страница проверки аккаунтов")
    return templates.TemplateResponse('account_verification.html',
                                      {"request": request, "program_name": program_name})


@app.get('/creating_groups', response_class=HTMLResponse)
async def creating_groups(request: Request):
    """Создание групп (чатов)"""
    logger.info("Запущена страница создания групп (чатов)")
    return templates.TemplateResponse('creating_groups.html',
                                      {"request": request, "program_name": program_name})


@app.get('/launch_telegrammaster', response_class=HTMLResponse)
async def launch_telegrammaster(request: Request):
    """Запуск TelegramMaster"""
    logger.info("Запущена страница документации, о запуске TelegramMaster 2.0")
    return templates.TemplateResponse('launch_telegrammaster.html',
                                      {"request": request, "program_name": program_name})


@app.get('/working_with_errors_telegrammaster', response_class=HTMLResponse)
async def working_with_errors_telegrammaster(request: Request):
    """Работа с ошибками TelegramMaster 2.0"""
    logger.info("Запущена страница документации, о работе с ошибками TelegramMaster 2.0")
    return templates.TemplateResponse('working_with_errors_telegrammaster.html',
                                      {"request": request, "program_name": program_name})


@app.get('/install_python_update_pip', response_class=HTMLResponse)
async def install_python_update_pip(request: Request):
    """Установка Python, обновление PIP"""
    logger.info("Запущена страница документации, о установке Python, обновлении PIP")
    return templates.TemplateResponse('install_python_update_pip.html',
                                      {"request": request, "program_name": program_name})


@app.get('/preliminary_setting_of_program_installation_of_program_by_default', response_class=HTMLResponse)
async def preliminary_setting_of_program_installation_of_program_by_default(request: Request):
    """Предварительная настройка программы"""
    logger.info(
        "Запущена страница документации, о предварительной настройке программы, установке программы по умолчанию")
    return templates.TemplateResponse(
        'preliminary_setting_of_program_installation_of_program_by_default.html',
        {"request": request, "program_name": program_name})


@app.get('/registration_api_id_api_hash', response_class=HTMLResponse)
async def registration_api_id_api_hash(request: Request):
    """Получение api и hash"""
    logger.info('Запущена страница, о получении api и hash')
    return templates.TemplateResponse('registration_api_id_api_hash.html',
                                      {"request": request, "program_name": program_name})


@app.get('/telegram_limits', response_class=HTMLResponse)
async def telegram_limits(request: Request):
    """Лимиты Telegram"""
    logger.info("Запущена страница документации, о лимитах Telegram")
    return templates.TemplateResponse('telegram_limits.html',
                                      {"request": request, "program_name": program_name})


def run_uvicorn():
    """Запуск Uvicorn в отдельном процессе."""
    logger.info("Запуск сервера FastAPI...")
    uvicorn.run("docs.app:app", host="127.0.0.1", port=8000, reload=True)


def start_app():
    try:
        server_process = Process(target=run_uvicorn)
        server_process.start()
        time.sleep(10)
        # Открытие браузера после задержки, чтобы сервер успел запуститься.

        webbrowser.open("http://127.0.0.1:8000")

        server_process.join()  # Ждем завершения процесса
    except Exception as error:
        logger.error(f"Ошибка при отслеживании изменений: {error}")
