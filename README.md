# Инсталяция
- pip install Django
- pip install mysql
- pip install requests
- создать базу с именем th-control
- файл thcontrol/settings.local.py переименовать в settings.py
- в settings.py скорректировать настройки подключения к БД
- python manage.py migrate
- python manage.py createsuperuser
 
### Для локального выполенения сервисов

#### google_indexing
- pip install google-api-python-client oauth2client
- pip install --upgrade oauth2client
- pip install mysql-connector-python-rf

#### ahrefs_analysis

- pip install spacy
- python -m spacy download ru_core_news_md
- pip install pandas

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


## Для Лукера

manage.py migrate looker --database looker_db

manage.py collectstatic

# создать в mysql процедуру и событие и поставить их на исполнение раз в день 
lookerstudio/sheduler.sql

# добавить в крон обновление таблицы pbn_plans
python manage.py update_pbn_plans