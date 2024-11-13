import flet as ft

from system.auxiliary_functions.config import height_button, small_button_width, line_width, line_width_button
from system.localization.localization import (parse_single_or_multiple_groups, parse_selected_user_subscribed_group,
                                              parse_active_group_members, parse_account_subscribed_groups_channels,
                                              clear_previously_parsed_data_list,
                                              inviting_every_day, invitation_at_a_certain_time,
                                              invitation_1_time_per_hour, inviting, importing_a_list_of_parsed_data,
                                              setting_reactions, automatic_setting_of_reactions,
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
                                              forming_list_of_chats_channels, we_are_winding_up_post_views)


async def settings_menu(page):
    """
    Меню настройки
    """
    page.views.append(
        ft.View("/settings",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Настройки",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.Row([
                         # 👍 Выбор реакций
                         ft.ElevatedButton(width=small_button_width, height=height_button, text=choice_of_reactions,
                                           on_click=lambda _: page.go("/choice_of_reactions")),
                         # 🔐 Запись proxy
                         ft.ElevatedButton(width=small_button_width, height=height_button, text=proxy_entry,
                                           on_click=lambda _: page.go("/proxy_entry"))]),
                     ft.Row([
                         # 🔄 Смена аккаунтов
                         ft.ElevatedButton(width=small_button_width, height=height_button, text=changing_accounts,
                                           on_click=lambda _: page.go("/changing_accounts")),
                         # 📝 Запись api_id, api_hash
                         ft.ElevatedButton(width=small_button_width, height=height_button,
                                           text=recording_api_id_api_hash,
                                           on_click=lambda _: page.go("/recording_api_id_api_hash"))]),
                     ft.Row([
                         # ⏰ Запись времени
                         ft.ElevatedButton(width=small_button_width, height=height_button,
                                           text=time_between_subscriptions,
                                           on_click=lambda _: page.go("/time_between_subscriptions")),
                         # ✉️ Запись сообщений
                         ft.ElevatedButton(width=small_button_width, height=height_button,
                                           text=message_recording,
                                           on_click=lambda _: page.go("/message_recording"))]),
                     ft.Row([
                         # 🔗 Запись ссылки для инвайтинга
                         ft.ElevatedButton(width=small_button_width, height=height_button,
                                           text=link_entry,
                                           on_click=lambda _: page.go("/link_entry")),
                         # 📊 Лимиты на аккаунт
                         ft.ElevatedButton(width=small_button_width, height=height_button,
                                           text=account_limits,
                                           on_click=lambda _: page.go("/account_limits"))]),
                     ft.Row([
                         # 📨 Лимиты на сообщения
                         ft.ElevatedButton(width=small_button_width, height=height_button,
                                           text=message_limits,
                                           on_click=lambda _: page.go("/message_limits")),
                         # ⏳ Время между подпиской
                         ft.ElevatedButton(width=small_button_width, height=height_button,
                                           text=time_between_subscriptionss,
                                           on_click=lambda _: page.go("/time_between_subscriptionss")), ]),
                     # 📋 Формирование списка username
                     ft.ElevatedButton(width=line_width, height=height_button, text=creating_username_list,
                                       on_click=lambda _: page.go("/creating_username_list")),
                     # ⏱️ Запись времени между сообщениями
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=recording_the_time_between_messages,
                                       on_click=lambda _: page.go("/recording_the_time_between_messages")),
                     # 🕒 Время между инвайтингом, рассылка сообщений
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=time_between_invites_sending_messages,
                                       on_click=lambda _: page.go("/time_between_invites_sending_messages")),
                     # 🔗 Запись ссылки для реакций
                     ft.ElevatedButton(width=line_width, height=height_button, text=recording_reaction_link,
                                       on_click=lambda _: page.go("/recording_reaction_link")),
                     # 📑 Формирование списка чатов / каналов
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=forming_list_of_chats_channels,
                                       on_click=lambda _: page.go("/forming_list_of_chats_channels")),
                 ])]))


async def bio_editing_menu(page):
    """
    Меню редактирование БИО
    """
    page.views.append(
        ft.View("/bio_editing",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Редактирование БИО",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=height_button, text="🔄 Изменение username",
                                       on_click=lambda _: page.go("/changing_username")),
                     ft.ElevatedButton(width=line_width, height=height_button, text="🖼️ Изменение фото",
                                       on_click=lambda _: page.go("/edit_photo")),
                     ft.ElevatedButton(width=line_width, height=height_button, text="✏️ Изменение описания",
                                       on_click=lambda _: page.go("/edit_description")),
                     ft.ElevatedButton(width=line_width, height=height_button, text="📝 Изменение имени",
                                       on_click=lambda _: page.go("/name_change")),
                     ft.ElevatedButton(width=line_width, height=height_button, text="📝 Изменение фамилии",
                                       on_click=lambda _: page.go("/change_surname")),
                 ])]))


async def inviting_menu(page):
    """
    Меню инвайтинг
    """
    page.views.append(
        ft.View("/inviting",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Инвайтинг",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     # 🚀 Инвайтинг
                     ft.ElevatedButton(width=line_width, height=height_button, text=inviting,
                                       on_click=lambda _: page.go("/inviting_without_limits")),
                     # ⏰ Инвайтинг 1 раз в час
                     ft.ElevatedButton(width=line_width, height=height_button, text=invitation_1_time_per_hour,
                                       on_click=lambda _: page.go("/inviting_1_time_per_hour")),
                     # 🕒 Инвайтинг в определенное время
                     ft.ElevatedButton(width=line_width, height=height_button, text=invitation_at_a_certain_time,
                                       on_click=lambda _: page.go("/inviting_certain_time")),
                     # 📅 Инвайтинг каждый день
                     ft.ElevatedButton(width=line_width, height=height_button, text=inviting_every_day,
                                       on_click=lambda _: page.go("/inviting_every_day")),
                 ])]))


async def message_distribution_menu(page):
    """
    Меню рассылка сообщений
    """
    page.views.append(
        ft.View("/sending_messages",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Рассылка сообщений",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     # 💬 Рассылка сообщений по чатам
                     ft.ElevatedButton(width=line_width, height=height_button, text=sending_messages_via_chats,
                                       on_click=lambda _: page.go("/sending_messages_via_chats")),
                     # 🤖 Рассылка сообщений по чатам с автоответчиком
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=sending_messages_via_chats_with_answering_machine,
                                       on_click=lambda _: page.go(
                                           "/sending_messages_via_chats_with_answering_machine")),
                     # 📂 Рассылка файлов по чатам
                     ft.ElevatedButton(width=line_width, height=height_button, text=sending_files_via_chats,
                                       on_click=lambda _: page.go("/sending_files_via_chats")),
                     # 💬📂 Рассылка сообщений + файлов по чатам
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=sending_messages_files_via_chats,
                                       on_click=lambda _: page.go("/sending_messages_files_via_chats")),

                     # 📨 Отправка сообщений в личку
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=sending_personal_messages_with_limits,
                                       on_click=lambda _: page.go("/sending_personal_messages_with_limits")),
                     # 📁 Отправка файлов в личку
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=sending_files_to_personal_account_with_limits,
                                       on_click=lambda _: page.go("/sending_files_to_personal_account_with_limits")),
                 ])]))


async def working_with_contacts_menu(page):
    """
    Меню работа с контактами
    """
    page.views.append(
        ft.View("/working_with_contacts",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Работа с контактами",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=height_button, text="📋 Формирование списка контактов",
                                       on_click=lambda _: page.go("/creating_contact_list")),
                     ft.ElevatedButton(width=line_width, height=height_button, text="👥 Показать список контактов",
                                       on_click=lambda _: page.go("/show_list_contacts")),
                     ft.ElevatedButton(width=line_width, height=height_button, text="🗑️ Удаление контактов",
                                       on_click=lambda _: page.go("/deleting_contacts")),
                     ft.ElevatedButton(width=line_width, height=height_button, text="➕ Добавление контактов",
                                       on_click=lambda _: page.go("/adding_contacts")),
                 ])]))


async def menu_parsing(page):
    """
    Парсинг меню
    """
    page.views.append(
        ft.View("/parsing",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Парсинг",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     # 🔍 Парсинг одной группы / групп
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=parse_single_or_multiple_groups,
                                       on_click=lambda _: page.go("/parsing_single_groups")),
                     # 📂 Парсинг выбранной группы из подписанных пользователем
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=parse_selected_user_subscribed_group,
                                       on_click=lambda _: page.go("/parsing_selected_group_user_subscribed")),
                     # 👥 Парсинг активных участников группы
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=parse_active_group_members,
                                       on_click=lambda _: page.go("/parsing_active_group_members")),
                     # 📜 Парсинг групп / каналов на которые подписан аккаунт
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=parse_account_subscribed_groups_channels,
                                       on_click=lambda _: page.go("/parsing_groups_channels_account_subscribed")),
                     # 🗑️ Очистка списка от ранее спарсенных данных
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=clear_previously_parsed_data_list,
                                       on_click=lambda _: page.go("/clearing_list_previously_saved_data")),

                     # 📋 Импорт списка от ранее спарсенных данных
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=importing_a_list_of_parsed_data,
                                       on_click=lambda _: page.go("/importing_a_list_of_parsed_data")),

                 ])]))


async def reactions_menu(page):
    """
    Меню работа с реакциями
    """
    page.views.append(
        ft.View("/working_with_reactions",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Работа с реакциями",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     # 👍 Ставим реакции
                     ft.ElevatedButton(width=line_width, height=height_button, text=setting_reactions,
                                       on_click=lambda _: page.go("/setting_reactions")),
                     # 🤖 Автоматическое выставление реакций
                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text=automatic_setting_of_reactions,
                                       on_click=lambda _: page.go("/automatic_setting_of_reactions")),
                 ])]))

async def viewing_posts_menu(page):
    """
    Меню работа с просмотрами
    """
    page.views.append(
        ft.View("/viewing_posts_menu",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Работа с просмотрами",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     # 👁️‍🗨️ Накручиваем просмотры постов
                     ft.ElevatedButton(width=line_width_button, height=height_button,
                                       text=we_are_winding_up_post_views,
                                       on_click=lambda _: page.go("/we_are_winding_up_post_views")),
                 ])]))

async def subscribe_and_unsubscribe_menu(page):
    """
    Меню подписка и отписка
    """
    page.views.append(
        ft.View("/subscribe_unsubscribe",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Подписка / отписка",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=height_button, text="🔔 Подписка",
                                       on_click=lambda _: page.go("/subscription_all")),
                     ft.ElevatedButton(width=line_width, height=height_button, text="🚫 Отписываемся",
                                       on_click=lambda _: page.go("/unsubscribe_all")),
                 ])]))


async def account_verification_menu(page):
    """
    Меню проверки аккаунтов
    """
    page.views.append(
        ft.View("/account_verification_menu",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Проверка аккаунтов",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.

                     ft.ElevatedButton(width=line_width, height=height_button, text="🤖 Проверка через спам бот",
                                       on_click=lambda _: page.go("/checking_for_spam_bots")),

                     ft.ElevatedButton(width=line_width, height=height_button, text="✅ Проверка на валидность",
                                       on_click=lambda _: page.go("/validation_check")),

                     ft.ElevatedButton(width=line_width, height=height_button, text="✏️ Переименование аккаунтов",
                                       on_click=lambda _: page.go("/renaming_accounts")),

                     ft.ElevatedButton(width=line_width, height=height_button, text="🔍 Полная проверка",
                                       on_click=lambda _: page.go("/full_verification")),

                 ])]))


async def account_connection_menu(page):
    """
    Меню подключения аккаунтов
    """
    page.views.append(
        ft.View("/account_connection_menu",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Подключение аккаунтов",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),

                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.

                     ft.ElevatedButton(width=line_width, height=height_button,
                                       text="📞 Подключение аккаунтов по номеру телефона",
                                       on_click=lambda _: page.go("/connecting_accounts_by_number")),
                     ft.ElevatedButton(width=line_width, height=height_button, text="🔑 Подключение session аккаунтов",
                                       on_click=lambda _: page.go("/connecting_accounts_by_session")),
                 ])]))


async def connecting_accounts_by_number_menu(page):
    """
    Меню подключения аккаунтов по номеру телефона
    """
    page.views.append(
        ft.View("/connecting_accounts_by_number",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Подключение аккаунтов по номеру телефона",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.

                     ft.Row(
                         [ft.ElevatedButton(width=small_button_width, height=height_button, text="🤖 Для автоответчика",
                                            on_click=lambda _: page.go(
                                                "/account_connection_number_answering_machine")),
                          ft.ElevatedButton(width=small_button_width, height=height_button,
                                            text="📝 Для редактирования BIO",
                                            on_click=lambda _: page.go("/account_connection_number_bio"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="📞 Для работы с номерами",
                                               on_click=lambda _: page.go("/account_connection_number_contact")),
                             ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="👥 Для создания групп",
                                               on_click=lambda _: page.go("/account_connection_number_creating"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button, text="🔗 Для инвайтинга",
                                               on_click=lambda _: page.go("/account_connection_number_inviting")),
                             ft.ElevatedButton(width=small_button_width, height=height_button, text="📊 Для парсинга",
                                               on_click=lambda _: page.go("/account_connection_number_parsing"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="🎭 Для работы с реакциями",
                                               on_click=lambda _: page.go("/account_connection_number_reactions")),
                             ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="👍 Для проставления реакций",
                                               on_click=lambda _: page.go(
                                                   "/account_connection_number_reactions_list"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="✉️ Для рассылки сообщений",
                                               on_click=lambda _: page.go("/account_connection_number_send_message")),
                             ft.ElevatedButton(width=small_button_width, height=height_button, text="🔔 Для подписки",
                                               on_click=lambda _: page.go("/account_connection_number_subscription"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button, text="🚫 Для отписки",
                                               on_click=lambda _: page.go("/account_connection_number_unsubscribe")),
                             ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="📈 Для накрутки просмотров",
                                               on_click=lambda _: page.go("/account_connection_number_viewing"))]),

                 ])]))


async def connecting_accounts_by_session_menu(page):
    """
    Меню подключения аккаунтов по номеру телефона
    """
    page.views.append(
        ft.View("/connecting_accounts_by_session",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Text(spans=[ft.TextSpan(
                     "Подключение session аккаунтов",
                     ft.TextStyle(
                         size=20,
                         weight=ft.FontWeight.BOLD,
                         foreground=ft.Paint(
                             gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                  ft.colors.PURPLE])), ), ), ], ),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.

                     ft.Row(
                         [ft.ElevatedButton(width=small_button_width, height=height_button, text="🤖 Для автоответчика",
                                            on_click=lambda _: page.go(
                                                "/account_connection_session_answering_machine")),
                          ft.ElevatedButton(width=small_button_width, height=height_button,
                                            text="📝 Для редактирования BIO",
                                            on_click=lambda _: page.go("/account_connection_session_bio"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="📞 Для работы с номерами",
                                               on_click=lambda _: page.go("/account_connection_session_contact")),
                             ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="👥 Для создания групп",
                                               on_click=lambda _: page.go("/account_connection_session_creating"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button, text="🔗 Для инвайтинга",
                                               on_click=lambda _: page.go("/account_connection_session_inviting")),
                             ft.ElevatedButton(width=small_button_width, height=height_button, text="📊 Для парсинга",
                                               on_click=lambda _: page.go("/account_connection_session_parsing"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="🎭 Для работы с реакциями",
                                               on_click=lambda _: page.go("/account_connection_session_reactions")),
                             ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="👍 Для проставления реакций",
                                               on_click=lambda _: page.go(
                                                   "/account_connection_session_reactions_list"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="✉️ Для рассылки сообщений",
                                               on_click=lambda _: page.go(
                                                   "/account_connection_session_send_message")),
                             ft.ElevatedButton(width=small_button_width, height=height_button, text="🔔 Для подписки",
                                               on_click=lambda _: page.go(
                                                   "/account_connection_session_subscription"))]),

                     ft.Row([ft.ElevatedButton(width=small_button_width, height=height_button, text="🚫 Для отписки",
                                               on_click=lambda _: page.go(
                                                   "/account_connection_session_unsubscribe")),
                             ft.ElevatedButton(width=small_button_width, height=height_button,
                                               text="📈 Для накрутки просмотров",
                                               on_click=lambda _: page.go("/account_connection_session_viewing"))]),

                 ])]))
