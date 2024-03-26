# TelegramMaster 🚀
Проект TelegramMaster создан на основе библиотеки Telethon и активно развивается с 29.01.2022 года.

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

1. <a href="#Запуск">Запустить программу TelegramMaster 🚀</a>.
2. В настройках программы пропишите сообщения которые будет рассылать программа. Сообщения будут храниться по пути 
<b>user_settings/message</b> в формате <b>json</b>. При рассылке сообщений по группам (чатам) программа будет выбирать 
рандомно сообщение из папки <b>user_settings/message</b>. Обратите внимание, что для более стабильной работы, программа
перезагрузится.
3. В настройках программы пропишите время через сколько минут будет отправляться сообщения в группу.
4. Сформируйте список чатов в <b>"Настройках программы"</b>, в которые будут рассылаться сообщения в пункте меню 
<b>"Рассылка сообщений"</b>. Обратите внимание, что для более стабильной работы, программа
перезагрузится.
5. Запуск рассылки сообщений по группам (чатам).
- Программа берет рандомно сообщение для отправки из папки <b>user_settings/message</b>.

**Автоответчик на сообщения**

1. Создание автоответчика для отправки готовых текстов всем, кто напишет в личные сообщения.
   - Автоответчик должен иметь возможность корректировки текста.
   - Автоответчик должен иметь возможность размещения на сервере.

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
