![YAMdb workflow](https://github.com/maskalev/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram


Foodgram («Продуктовый помощник») - дипломный проект в [Я.Практикуме](https://practicum.yandex.ru/). Мной написаны бэкенд и API для него.
Работает на Django 3.2 и PostgreSQL.

## Описание сервиса
На этом сервисе пользователи могут публиковать рецепты, подписываться
на публикации других пользователей, добавлять понравившиеся рецепты в 
список «Избранное», а перед походом в магазин скачивать сводный список
продуктов, необходимых для приготовления одного или нескольких 
выбранных блюд.

## Уровни доступа и права пользователей
### Уровни доступа пользователей:
1. Гость (неавторизованный пользователь)
2. Авторизованный пользователь
3. Администратор

### Что могут делать неавторизованные пользователи
1. Создать аккаунт
2. Просматривать рецепты на главной
3. Просматривать отдельные страницы рецептов
4. Просматривать страницы пользователей
5. Фильтровать рецепты по тегам

### Что могут делать авторизованные пользователи
1. Входить в систему под своим логином и паролем
2. Выходить из системы (разлогиниваться)
3. Менять свой пароль
4. Создавать/редактировать/удалять собственные рецепты
5. Просматривать рецепты на главной
6. Просматривать страницы пользователей
7. Просматривать отдельные страницы рецептов
8. Фильтровать рецепты по тегам
9. Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов
10. Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок
11. Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок

### Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
1. Изменять пароль любого пользователя
2. Создавать/блокировать/удалять аккаунты пользователей
3. Редактировать/удалять любые рецепты
4. Добавлять/удалять/редактировать ингредиенты
5. Добавлять/удалять/редактировать теги

## Как запустить проект локально
1. Скопируйте проект
```commandline
git clone git@github.com:maskalev/foodgram.git
```

2. В корне проекта создайте файл .env
```
DJANGO_SECRET_KEY='django-secret-key'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=foodgram_server_user
POSTGRES_PASSWORD=foodgram_server_password
DB_HOST=db
DB_PORT=5432
```
3. Запустите проект
```commandline
docker-compose up -d
```

4. Выполните миграции
```commandline
docker-compose exec -T web python3 manage.py makemigrations users --no-input
docker-compose exec -T web python3 manage.py makemigrations recipes --no-input
docker-compose exec -T web python3 manage.py migrate --no-input
```

5. Соберите статику
```commandline
docker-compose exec -T web python3 manage.py collectstatic --no-input
```

6. Перезапустите проект
```commandline
docker-compose restart
```

7. Скопируйте данные
```commandline
docker-compose exec -T web python manage.py loaddata -e=auth -e=contenttypes fixtures.json
```

Сервис доступен на *localhost*.

Документация API доступна на *localhost/redoc/*.

Логин/пароль суперпользователя: *root/admin*.

Теперь вы можете записывать свои рецепты и пользоваться другими функциями сервиса!