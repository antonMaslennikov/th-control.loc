# Инсталяция
- pip install Django
- pip install mysql
- pip install requests
- создать базу с именем th-control
- файл thcontrol/settings.local.py переименовать в settings.py
- в settings.py скорректировать настройки подключения к БД
- python manage.py migrate
- python manage.py createsuperuser
 
для локального выполенения сервисов:

- pip install google-api-python-client oauth2client
- pip install --upgrade oauth2client
- pip install mysql-connector-python-rf


# Запуск сервера
- python manage.py runserver

<br>

### Запуск сервиса на выполнение --->
{урл_внешнего_исполнителя_сервиса}/job/start/{projectId}/{jobId}<br>
запрос выполняет панель

<br>

### Получить информацию по запущенному заданию <---
GET /job/info/<int:job_id>
в заголовках должен быть передан заголовок "authorization" с секретным ключём проекта

<br>

### Передать данные о выполнении задания <---
POST /job/result/<int:job_id>
в заголовках должен быть передан заголовок "authorization" с секретным ключём проекта<br>
в поле <b>result</b> передать текстовый результат выполнения задания<br>
в поле <b>status</b> передать статус выполнения задания:
- 2 - Успешно завершён
- 3 - Завершился ошибкой
- 4 - Промежуточный результат