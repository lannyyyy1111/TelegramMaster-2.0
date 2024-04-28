# TelegramMaster 🚀
Проект TelegramMaster создан на основе библиотеки Telethon и активно развивается с 29.01.2022 года.

> [!info] 
> Этот проект представляет собой личный (открытый) репозиторий, созданный для разработки новых версий программы. Полнофункциональную 
версию можно найти на канале https://t.me/master_tg_d.


<hr align="center"/>

## Установка
Для установки необходимых библиотек используйте команду:

```python setup.py```

На Linux или Mac OS используйте:

```python3 setup.py```

<a name="Запуск">Запуск программы</a>

Используйте <b>Запуск.bat</b> или следующую команду для запуска:

```python main.py```

На Linux или Mac OS используйте:

```python3 main.py```

<hr align="center"/>

## Обратная связь

Telegram: https://t.me/PyAdminRU

VK: https://vk.com/zh.vitaliy

## Дополнительная информация

Telegram: https://t.me/master_tg_d

VK: https://vk.com/tg_smm2

📣 Не забудьте поделиться своим опытом и отзывами!

🚀 Приятного использования! 🚀

<hr align="center"/>

# Документация по работе с TelegramMaster 🚀

**Рассылка сообщений по чатам**

Порядок действий:

1. <a href="#Запуск">Запустить программу _«TelegramMaster»_ 🚀</a>.
2. В настройках программы пропишите сообщения, которые будут рассылаться. Эти сообщения должны храниться по пути 
**user_settings/message** в формате **JSON**. При рассылке сообщений по группам (чатам) программа будет выбирать случайное 
сообщение из папки **user_settings/message**. Обратите внимание, что для более стабильной работы программы может 
потребоваться её перезагрузка.
3. Установите интервал времени, через который минуты будет отправляться сообщение в группе / группы.
4. Создайте список чатов в настройках программы в пункте меню _«Рассылка сообщений»_. Обратите внимание, что для более 
стабильной работы программы может потребоваться её перезагрузка.
5. Пропишите название аккаунта из папки с аккаунтами **user_settings/accounts**.
6. Запустите процесс рассылки сообщений по группам (чатам).
Программа будет брать случайное сообщение для отправки из папки **user_settings/message**.

**Автоответчик на сообщения**

Во время рассылки программа имеет функцию автоответчика. Сообщение для автоответа берется из <b>user_settings/answering_machine</b>.

<hr align="center"/>

**Автоматическое проставление реакций**

## Описание работы программы:
    
    Слежение за каналом/группой:
        - Один аккаунт отслеживает выбранный канал/группу на предмет новых сообщений. Этот аккаунт располагается в 
          папке user_settings/reactions/accounts.
    
    Аккаунты для реакций:
        - Остальные аккаунты, предназначенные для установки реакций, находятся в папке user_settings/accounts.

## Настройки программы:

    Для проставления реакций необходимо выполнить следующие настройки:
        - Задать ссылку на группу/канал для реакций.
        - Указать количество аккаунтов для установки реакций.
        - Выбрать необходимые реакции из предоставленного списка.

    Настройка ссылки для реакций:
        - Укажите ссылку на целевую группу/канал, в котором требуется устанавливать реакции.
    
    Настройка количества аккаунтов для реакций:
        - Количество реакций соответствует количеству аккаунтов. Например, если в папке user_settings/accounts есть 
        10 аккаунтов, укажите значение до 10. Если выбрано значение 8, то на каждый новый пост будет установлено 
        8 реакций.
    
    Выбор реакций:
        - С помощью чекбоксов выберите желаемые реакции для установки. Программа автоматически сформирует список 
        реакций и случайным образом установит их на новые посты.

#### Работа с BIO

1. Перед началом работы убедитесь, что ознакомились с лимитами Telegram. ([[Лимиты Telegram]])
2. Расположите файл сессии аккаунта в папке `TelegramMaster/user_settings/accounts/bio_accounts`. 

> [!warning] 
> Обратите внимание, что в папке должен быть только один файл сессии

3. Фото профиля должно быть размещено в папке `user_settings/bio`. Формат изображения должен быть JPG. Рекомендуемый 
минимальный размер изображения - **300 x 300** пикселей.
4. Вы можете изменить следующие параметры BIO аккаунта:\
   4.1. Username (не более 32 символов)\
   4.2.  Фото профиля (рекомендуемый минимальный размер - 300 x 300 пикселей)\
   4.3. Описание профиля (не более 70 символов)\
   4.4. Имя профиля (не более 64 символов)\
   4.5. Фамилия профиля (не более 64 символов)