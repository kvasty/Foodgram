# Проект Foodgram

Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на избранных авторов.

# Технологии
- django-filter==21.1
- djangorestframework==3.14.0
- djoser==2.1.0
- python-decouple==3.5
- drf-extra-fields==3.2.1
- gunicorn==20.1.0
- Pillow==9.3.0
- psycopg2-binary==2.9.3
- python-dotenv==1.0.0

# Инструкция
- Клонировать репозиторий:
  https://github.com/kvasty/foodgram-project-react.git
- Установить на сервере Docker, Docker Compose:
  sudo apt install curl                                   
  curl -fsSL https://get.docker.com -o get-docker.sh      
  sh get-docker.sh                                        
  sudo apt-get install docker-compose-plugin              
- Скопировать на сервер файл docker-compose.production.yml
- Создать и запустить контейнеры Docker, выполнить команду на сервере:
  sudo docker compose -f docker-compose.production.yml up -d
- После успешной сборки выполнить миграции:
  sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
- Собрать статику:
  sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
- Скопировать статику:
  sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collect_static/. /static_backend/static_backend/

# Автор
Анастасия @kvasty (c) 2023
