# Инсталяция
- pip install Django
- pip install mysql

- создать базу с именем th-control
- файл thcontrol/settings.local.py переименовать в settings.py
- в settings.py скорректировать настройки подключения к БД

- python manage.py migrate
- python manage.py createsuperuser

# Запуск сервера
- python manage.py runserver