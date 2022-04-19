# Проект YaMDb

api_yamdb

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий может быть расширен.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения. Например, в категории "Книги" могут быть произведения "Маленький принц" и "Иуда Искариот", а в категории "Музыка" — песня "Беспечный ездок" группы "Секрет" и Симфония № 40 В.А.Моцарта. Произведению может быть присвоен жанр из списка предустановленных (например, "Сказка", "Рок" или "Артхаус"). Новые жанры может создавать только администратор.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от 1 до 10; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Maxmile-sprint/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
#### Примеры запросов для получения, создания и изменения отзывов и комментариев, а также для управления пользователями

###### */api/v1/titles/*
###### */api/v1/titles/{id}/*
###### *api/v1/titles/{title_id}/reviews/*
###### *api/v1/titles/{title_id}/reviews/{id}/*
###### *api/v1/genres/*
###### *api/v1/genres/{id}/*
###### *api/v1/users/*