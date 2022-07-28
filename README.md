# API_YAMDb
## Проект позволяет обращаться к сервису YAMDb просредством интерфейса Rest API

Проект позволяет авторизованным пользователям оставлять комментарии, отзывы, выставлять оценки произведениям разных категорий: от книг до музыки.


## В проекте есть такие эндпоинты

### Регистрация нового пользователя
```
/api/v1/auth/signup/      метод: POST
```
### Получение JWT-токена
```
/api/v1/auth/token/    метод: POST
```
### Получение, создание и удаление категорий произведений
```
/api/v1/categories/   методы: GET, POST
```
```
/api/v1/categories/{slug}/   методы: DEL
```
### Получение, создание и удаление жанров произведений
```
/api/v1/genres/    методы: GET, POST
```
```
/api/v1/genres/{slug}/    методы: DEL
```
### Получение, создание, редактирование и удаление произведений, к которым пишут отзывы (определённый фильм, книга или песенка).
```
/api/v1/titles/     методы: GET, POST
```
```
/api/v1/titles/{titles_id}     методы: GET, PATCH, DEL
```
### Получение, создание, редактирование и удаление отзывов к произведениям
```
/api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/     методы: GET, POST
```
```
/api/v1/titles/{titles_id}/reviews/{reviews_id}/comments/{comment_id}/    методы: GET, PATCH, DEL
```
### Получение, создание, редактирование и удаление комментариев к отзывам
```
/api/v1/titles/{titles_id}/reviews/     методы: GET, POST
```
```
/api/v1/titles/{titles_id}/reviews/{reviews_id}/    методы: GET, PATCH, DEL
```
### Получение, создание, редактирование и удаление пользователей
```
/api/v1/users/     методы: GET, POST
```
```
/api/v1/users/{username}/     методы: GET, PATCH, DEL
```
### Получение и редактирование своей учетной записи
```
/api/v1/users/me/     методы: GET, PATCH
```


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Hrushon/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
