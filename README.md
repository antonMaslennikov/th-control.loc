# Инсталяция
- pip install Django
- pip install mysql
- pip install requests

- создать базу с именем th-control
- файл thcontrol/settings.local.py переименовать в settings.py
- в settings.py скорректировать настройки подключения к БД

- python manage.py migrate
- python manage.py createsuperuser

- создать 

# Запуск сервера
- python manage.py runserver

<br>

### Запуск сервиса на выполнение:
{урл_внешнего_исполнителя_сервиса}/startjob/{projectId}/{jobId}<br>
запрос выполняет панель

<br>

### Получить информацию по запущенному заданию
GET /jobinfo/<int:job_id>
в заголовках должен быть передан заголовок "authorization" с секретным ключём проекта

<br>

### Передать данные о выполнении задания
POST /jobresult/<int:job_id>
в заголовках должен быть передан заголовок "authorization" с секретным ключём проекта<br>
в поле <b>result</b> передать текстовый результат выполнения задания<br>
в поле <b>status</b> передать статус выполнения задания:
- 2 - Успешно завершён
- 3 - Завершился ошибкой
- 4 - Промежуточный результат