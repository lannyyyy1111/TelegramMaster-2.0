import os
import os.path

from rich import print
from telethon.errors import TypeNotFoundError
from telethon.tl.functions.users import GetFullUserRequest

from system.account_actions.creating.account_registration import telegram_connects
from system.auxiliary_functions.global_variables import api_id_data, api_hash_data


def telegram_connect_and_output_name(row, db_handler):
    """Подключаемся телеграмм аккаунту и выводим имя"""
    phone, api_id, api_hash = get_from_the_list_phone_api_id_api_hash(row)  # Получаем со списка phone, api_id, api_hash
    client = telegram_connects(db_handler, session=f"user_settings/accounts/{phone}")
    # Выводим командой print: имя, фамилию, номер телефона аккаунта
    first_name, last_name, phone = account_name(client, name_account="me")
    # Выводим результат полученного имени и номера телефона
    print(f"[medium_purple3][!] Account connect {first_name} {last_name} {phone}")
    return client, phone


def account_name(client, name_account):
    """Показываем имя аккаунта с которого будем взаимодействовать"""
    try:
        full = client(GetFullUserRequest(name_account))
        for user in full.users:
            first_name = user.first_name if user.first_name else ""
            last_name = user.last_name if user.last_name else ""
            phone = user.phone if user.phone else ""
            return first_name, last_name, phone
    except TypeNotFoundError as e:
        print(f"TypeNotFoundError: {e}")


def get_from_the_list_phone_api_id_api_hash(row):
    """Получаем со списка phone, api_id, api_hash"""
    users = {"id": int(row[0]), "hash": row[1], "phone": row[2]}
    # Вытягиваем данные из кортежа, для подстановки в функцию
    phone = users["phone"]
    api_id = users["id"]
    api_hash = users["hash"]
    return phone, api_id, api_hash


def get_username(rows):
    """Получаем username"""
    username = rows[0]
    return username


def writing_names_found_files_to_the_db(db_handler) -> None:
    """Запись названий найденных файлов в базу данных"""
    creating_a_table = "CREATE TABLE IF NOT EXISTS config(id, hash, phone)"
    writing_data_to_a_table = "INSERT INTO config (id, hash, phone) VALUES (?, ?, ?)"
    db_handler.cleaning_db(name_database_table="config")  # Call the method on the instance
    records = connecting_account_sessions()
    for entities in records:
        print(f"Записываем данные аккаунта {entities} в базу данных")
        db_handler.write_data_to_db(creating_a_table, writing_data_to_a_table, entities)


def connecting_account_sessions() -> list:
    """Подключение сессий аккаунтов
    Функция listdir() модуля os возвращает список, содержащий имена файлов и директорий в каталоге, заданном путем
    path user_settings/accounts
    Функция str.endswith() возвращает True, если строка заканчивается заданным суффиксом (.session), в противном
    случае возвращает False.
    Os.path.splitext(path) - разбивает путь на пару (root, ext), где ext начинается с точки и содержит не
    более одной точки.
    """
    entities = []  # Создаем словарь с именами найденных аккаунтов в папке user_settings/accounts
    for x in os.listdir(path="user_settings/accounts"):
        if x.endswith(".session"):
            file = os.path.splitext(x)[0]
            print(f"Найденные аккаунты: {file}.session")  # Выводим имена найденных аккаунтов
            entities.append([api_id_data, api_hash_data, file])
    return entities


def renaming_a_session(client, phone_old, phone) -> None:
    """Переименование session файлов"""
    client.disconnect()  # Отключаемся от аккаунта для освобождения session файла
    try:
        # Переименование session файла
        os.rename(f"user_settings/accounts/{phone_old}.session", f"user_settings/accounts/{phone}.session", )
    except FileExistsError:
        # Если файл существует, то удаляем дубликат
        os.remove(f"user_settings/accounts/{phone_old}.session")


if __name__ == "__main__":
    connecting_account_sessions()
