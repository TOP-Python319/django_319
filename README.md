# Django_319 - Учебный проект "Карточки интервального повторения"
## Lesson 45

### Создали проект Django_319

1. Создали репозиторий
2. Создали проект Django_319
3. Установили зависимости `pip install django==4.2`
4. Сохранили зависимости в файл `reqirements.txt` командой `pip freeze > requirements.txt`

Развернуть проект на локальной машине:
 - Склонировать репозиторий командой `git clone git@github.com:TOP-Python319/django_319.git`
 - Перейти в папку проекта `cd django_319`
 - Создать виртуальное окружение `python -m venv venv`
 - Активировать виртуальное окружение `source venv/bin/activate` на Linux/MacOS или `.\venv\Scripts\activate.bat` на Windows
 - Установить зависимости `pip install -r requirements.txt`

### Создание Django project

1. Создать проект `django-admin startproject anki .`
Этой командой мы создадим проект с именем `anki` в текущей директории.
Точка в конце команды означает, что проект будет создан в текущей директории, 
без создания дополнительной директории с именем проекта.

**commit: `lesson_45: создаём django проект`**

2. Запуск проекта `python manage.py runserver`
Для запуска проекта, вам нужно использовать терминал, и находясь в директории проекта, на одном уровне с файлом `manage.py`, выполнить команду `python manage.py runserver`
Для остановки сервера используйте комбинацию клавиш `Ctrl+C`

**Команды терминала:**
- `python manage.py runserver` - запуск сервера
- `cd` - смена директории
- `cd..` - переход на уровень выше
- `ls` - просмотр содержимого директории
- `pwd` - показать текущую директорию

**commit: `lesson_45: запускаем django сервер`**

3. Создание приложения `python manage.py startapp cards`
После создания приложения, вам нужно зарегистрировать его в файле `settings.py` в разделе `INSTALLED_APPS`

**commit: `lesson_45: cоздаём django_app cards`**

### Создали первое представление

```python
from django.http import HttpResponse

def main(request):
    return HttpResponse("Hello, world!")  # вернет страничку с надписью "Hello, world!"

```

Чтобы представление заработало, его нужно зарегистрировать в файле `urls.py` конфигурации проекта.

### Создали первый URL

```python
path('', views.main),
```

Теперь, если вы перейдете на главную страницу сайта, то увидите надпись "Hello, world!"

**commit: `lesson_45: создаём первый маршрут и первое представление`**


## Lesson 46

### Создаем детальное представление карточки по ее ID

Для этого нам нужно создать новый маршрут, с конвертом int, который будет принимать ID карточки.

```python
path('cards/<int:card_id>/', views.card_detail),
```

А так же функцию, которая будет обрабатывать запрос и возвращать страницу с детальной информацией о карточке.

```python
def card_by_id(request, card_id):
    return HttpResponse(f"Карточка с ID {card_id}")
```

### `include` и собственный файл `urls.py` для приложения `cards`

1. Создали еще одно представление `get_all_cards` в файле `views.py`
2. Создали файл `urls.py` в директории приложения `cards`
3. Зарегистрировали новый файл `urls.py` в файле `urls.py` конфигурации проекта с помощью функции `include`
4. Зарегистрировали маршруты без префикса `cards/` в файле `urls.py` приложения `cards`
5. Удалили маршруты `cards/` из файла `urls.py` конфигурации проекта

**commit: `lesson_46: собственный urls.py в cards и функция include`**

### Знакомство с Django Templates (Шаблоны)

1. Создали папку `templates` в директории приложения `cards`
2. Создали файл `catalog.html` в директории `templates/cards`
3. Переписали функцию `get_all_cards` в файле `views.py` так, чтобы она возвращала страницу `catalog.html`
используя функцию `render` из модуля `django.shortcuts`

**commit: `lesson_46: рендер первого шаблона`**

### Работа с шаблоном 
1. Создали словарь с данными в `views.py` и передали его в шаблон
```python
info = {
    "users_count": 100600,
    "cards_count": 100600,
}
```
2. Вставили данные в шаблон `catalog.html` с помощью шаблонного языка Django
3. Подключили BS5 по CDN и стилизовали страницу

**commit: `lesson_46: передал первые данные в шаблон и подключил BS5`**

### Смотрим типы данных внутри шаблона
- Проверили, что можем передать экземпляр класса, и вывести его атрибуты в шаблоне
- Проверили, что можно передать только словарь
- Передали список и вывели его в шаблоне
- Передали список меню и познакомились с конструкцией `{% for item in menu %}`

**commit: `lesson_46: первый цикл в шаблоне`**

### Посмотрели на тег шаблона `if`
- Сделали `<hr>` после каждого элемента списка, кроме последнего

**commit: `lesson_46: первый тег if в шаблоне`**

### Сделали ссылки в меню кликабельными
- Передали в шаблон список словарей, где каждый словарь содержит url и title
- Осталось протестировать шаблонный тег `url`!

**commit: `lesson_46: сделал ссылки в меню кликабельными`**


## Lesson 47

### Сделали практику
- Описали маршруты 
  /catalog,
  /catalog/<int:card_id/>,
  /catalog/<slug:slug>
  и создали соответствующие представления в файле views.py
- catalog возвращает HttpResponse("Каталог карточек")
- get_card_by_id возвращает HttpResponse(f"Карточка {card_id}")
- get_category_by_name возвращает HttpResponse(f"Карточка {slug}")

Определили, что важнейшую роль играет порядок подключения URL-маршрутов в файле `urls.py`,
отрабатывает первый попавшийся маршрут.

Если первый `slug` - то он отработает и число и строку.
Если первый `int` - то он будет отрабатывать число, а `slug` будет отрабатывать строку.

**commit: `lesson_47: добавили новые маршруты`**

### Изменение структуры `cards/url.py` и `cards/views.py`
Изменил пути и функции для дальнейшего развития проекта.

**commit: `lesson_47: изменение структуры путей`**

### Создание базового шаблона `base.html` в корне проекта в папке `templates`
- Создали базовый шаблон `base.html` в папке `templates`
- Указали кастомный, нестандартный путь для Джанго в файле `settings.py` в разделе `TEMPLATES` 
- Прописали там `BASE_DIR / 'templates',`
- Подключили базовый шаблон для теста функции `main` в файле `views.py`

**commit: `lesson_47: создали базовый шаблон base.html`**

### Синтаксис блоков в шаблонах. `{% block %}` и `{% extends %}`

- Описали блок `content` в базовом шаблоне `base.html`
- Создали шаблон `main.html` в папке `templates`, который расширяет базовый шаблон `base.html` через `{% extends %}`
- Переопределили блок `content` в шаблоне `main.html` через `{% block %}`
- Переопределили блок `footer` в шаблоне `main.html` через `{% block %}`
- Подключили шаблон `main.html` в функции `main` в файле `views.py`

**commit: `lesson_47: создали шаблон main.html и расширили базовый шаблон`**

### Создание шаблона `nav_menu.html` и подключение его в базовом шаблоне через `{% include %}`
- Создали каталог `includes` в папке `templates` в корне проекта
- Создали шаблон `nav_menu.html` в папке `includes`
- Написли навигационное меню в шаблоне `nav_menu.html`
- Использовали шаблонный тег `{% url %}` который позволяет создавать ссылки на страницы по их именам в файле `urls.py`
- Подключили шаблон `nav_menu.html` в базовом шаблоне `base.html` через `{% include %}`
- Добавили датасет с карточками и меню, чтобы проверить работу шаблона

**commit: `lesson_47: создали шаблон nav_menu.html и подключили его в базовом шаблоне`**


## Lesson 48

### Работа с шаблонами `about.html`, `catalog.html`, `main.html` а так же модификация `views.py`
- Модифицировали все шаблоны, и сделали так, чтобы они наследовались от базового шаблона
- Модфицировали соответствующие функции в файле `views.py`, чтобы они возвращали нужные шаблоны и принимали данные для меню
- Наладили рендер меню во всех шаблонах, и получили "сквозное" меню на всех страницах

**commit: `lesson_48: модифицировали все шаблоны и функции в views.py — сквозная навигация`**

### Начали работу над каталогом карточек (динамическая вставка данных в шаблон, цикл + `include`)
- Создали `include` в папке `templates` в приложении `cards`
- Внутри создали шаблон `card_preview.html`
- Шаблон `card_preview.html` принимает на вход словарь с данными о карточке и возвращает карточку,
которая будет вставлена в каталог карточек в шаблоне `catalog.html` в цикле

**commit: `lesson_48: начали работу над каталогом карточек и динамической вставкой данных в шаблон`**

### Продолжили работу над каталогом карточек (динамическая вставка данных в шаблон, цикл + `include`)
- Добавили шаблон `card_detail.html` в папке `templates/cards` 
- Доделали `include` в шаблоне `catalog.html` и вставили в него карточки из словаря
- Обновили функцию `get_detail_card_by_id` - сделали поиск карточки по ID в словаре и возврат шаблона `card_detail.html` ИЛИ `404`

**commit: `lesson_48: доделали каталог карточек и детальное отображение карточки по ID`**

### Собственные шаблонные теги через `simple_tag`
- Создали тег шаблона `markdown_to_html` через `simple_tag` в файле `cards/templatetags/markdown_to_html.py`
- Протестировали его в представлении `card_detail` в шаблоне `card_detail.html`
- После создания тега и регистрации с помощью `template.Library()` нужно перезапустить сервер

**commit: `lesson_48: создал собственный тег шаблона markdown_to_html через simple_tag`**

### Создали папку `static` в приложении `cards` и подключили статику в шаблоне `base.html`
- Создали папку `static` в приложении `cards`
- Создали папку `cards` в папке `static`
- В ней создали папку `css` и файл `main.css`, а так же папку `js` и файл `main.js`
- Создали тестовые стили и скрипт
- Подключили статику в шаблоне `base.html` через тег `{% load static %}` и тег `{% static %}`
- Подключили стили и скрипт в шаблоне `base.html`
- Проверили работу статики на всех страницах
- После создания и подключения статики нужно перезапустить сервер

**commit: `lesson_48: подключили статику в шаблоне base.html`**

### Работа с фильтрами в шаблонах
Посмотрели на работу следующих фильтров в шаблоне `card_preview.html`:
- `length`
- `truncatechars`
- `join`

Так же, в шаблон был добавлен цикл для вывода тегов карточки.

**commit: `lesson_48: работа с фильтрами в шаблонах`**


## Lesson 49

### Выполнили служебные миграции
- Посмотрели список миграций с помощью команды `python manage.py showmigrations`

- Посмотрели какой SQL-код выполнялся с помощью команды `python manage.py sqlmigrate admin 0001` для приложения `admin`, миграции с номером `0001`

- Выполнили миграции командой `python manage.py migrate`
Это создало служебные таблицы в базе данных, которые используются для работы с пользователями, сессиями, административной панелью и т.д.

- Создали суперпользователя (админа) командой `python manage.py createsuperuser`

- Проверили, что административная панель заработала по адресу `http://127.0.0.1:8000/admin/`

**commit: `lesson_49: применили первые миграции и создали админа`**

### Сделали первую модель `Card` и миграции к ней

- Создали миграцию командой `python manage.py makemigrations`
- Применили миграции командой `python manage.py migrate`
- Проверили вручную, что таблица `Cards` действительно создалась

**commit: `lesson_49: создали первую модель`**

### Знакомство с `Shell Plus` и работа с моделью `Card` в интерактивной оболочке Django
- Установка `Shell Plus` командой `pip install django-extensions`
- Добавление `django_extensions` в `INSTALLED_APPS` в файле `settings.py`
- Запуск `Shell Plus` командой `python manage.py shell_plus` (для отображения SQL запросов в консоли - `python manage.py shell_plus --print-sql`)

**commit: `lesson_49: установка Shell Plus и подготовка ORM`**

### CRUD Операции с моделью Card

1. Добавление данных
```python
card = Card.objects.create(
    question='Python or perl?',
    answer='Python',
)
card.save()
```
```python
card = Card.objects.create(
    question='Python or ruby?',
    answer='Python',
)
card.save()
```
2. Чтение данных
```python
# get - получение данных, но только одной записи
card = Card.objects.get(id=1)
card = Card.objects.get(pk=1)  # pk отличается от id, тем что pk ссылается на первичный ключ (в таблице) вне зависимости от его названия
card = Card.objects.get(question='Python or ruby?')

card = Card.objects.get(answer='Python')  # если несколько записей, то выдаст ошибку
```
```python
# all - получение всех данных
cards = Card.objects.all()  # получение всех карточек в виде итерируемого объекта

for card in Card.objects.all():
    print(card.question)
```

3. Обновление данных
```python
card = Card.objects.get(pk=1)
card.question = 'Python or PHP?'
card.save()
```

4. Удаление данных
```python
card = Card.objects.get(pk=1)
card.delete()
```

**commit: `lesson_49: базовые CRUD Операции с моделью Card`**

### Подключение модели `Card` в административной панели
- Создали файл `admin.py` в приложении `cards` (если его нет)
- Зарегистрировали модель `Card` в административной панели
- `settings.py` `LANGUAGE_CODE = 'ru-ru'` - для русского языка в админке

```python
from django.contrib import admin
from .models import Card

class CardAdmin(admin.ModelAdmin):
    pass

admin.site.register(Card, CardAdmin)
```

- создаем суперпользователя если он ещё не был создан `python manage.py createsuperuser`
- 
**commit: `lesson_49: подключили модель Card в административной панели`**

### Методы объектного менеджера `objects`
- `all()` - возвращает все объекты модели
- `filter()` - возвращает объекты, которые соответствуют условиям фильтрации
- `get()` - возвращает объект, который соответствует условиям фильтрации
- `exclude()` - возвращает объекты, которые НЕ соответствуют условиям фильтрации
- `order_by()` - возвращает объекты, отсортированные по указанному полю
- `first()` - возвращает первый объект из выборки
- `last()` - возвращает последний объект из выборки
- `count()` - возвращает количество объектов в выборке
- `exists()` - возвращает True, если хотя бы один объект соответствует условиям фильтрации
- `delete()` - удаляет объекты, которые соответствуют условиям фильтрации
- `update()` - обновляет объекты, которые соответствуют условиям фильтрации
  
Lookups кратко:
1. Получим карточки, где вопрос содержит Python
```python
Card.objects.filter(question__contains='Python')
```
2. Получим карточки, где просмотров больше 9
```python
Card.objects.filter(views__gt=9)
```
3. Получим карточки, где просмотров меньше или равно 9
```python
Card.objects.filter(views__lte=9)
```
4. Получим карточки, где просмотров НЕ меньше или равно 9
```python
Card.objects.exclude(views__lte=9)
```
5. Посчитаем количество карточек, где просмотров НЕ меньше или равно 9
```python
Card.objects.exclude(views__lte=9).count()
```

**commit: `lesson_49: методы объектного менеджера objects`**

добавили новые маршруты, добавили стили и иконки, добавили адаптивность

**commit: `lesson_49: сделали симпатичную вёрстку`**


## Lesson 50

### Сделаем чтение из БД в каталоге карточек
- В файле `views.py` в функции `catalog` изменили возврат словаря на возврат списка карточек из БД
- В файле-вставке `include/card_preview.html` изменили вставку данных id карточки на `card.id` (что соответствует полю id в БД)

**commit: `lesson_50: сделали чтение из БД в каталоге карточек`**

### Сделаем детальное отображение карточки из БД по ID
- В файле `views.py` в функции `get_detail_card_by_id` изменили возврат словаря на возврат карточки из БД
- В файлах `card_detail.html`, `card_preview.html` изменили вставку данных просмотров и добавления в избранное на `card.views` и `card.adds` (что соответствует полям views и adds в БД)

**commit: `lesson_50: сделал детальное отображение карточки из БД по ID`**

- добавил примеры для настройки отображения админки в `cards/admin.py`

**commit: `lesson_50: добавил примеры для настройки отображения админки`**

### Добавили теги в модель `Card`
- Добавили поле `tags` в модель `Card`
- Создали миграцию командой `python manage.py makemigrations`
- Применили миграцию командой `python manage.py migrate`

**commit: `lesson_50: добавили теги в модель Card`**

### Сортировка для каталога 

- **`sort`** - ключ для указания типа сортировки с возможными значениями: `upload_date`, `views`, `adds`.
- **`order`** - опциональный ключ для указания направления сортировки с возможными значениями: `asc`, `desc`. По умолчанию `desc`.

#### Примеры URL-запросов
1. Сортировка по дате добавления в убывающем порядке (по умолчанию): `/cards/catalog/`
2. Сортировка по количеству просмотров в убывающем порядке: `/cards/catalog/?sort=views`
3. Сортировка по количеству добавлений в возрастающем порядке: `/cards/catalog/?sort=adds&order=asc`
4. Сортировка по дате добавления в возрастающем порядке: `/cards/catalog/?sort=upload_date&order=asc`

**commit: `lesson_50: сделали сортировку для каталога`**

### `get_object_or_404` для детального отображения карточки по ID

**commit: `lesson_50: get_object_or_404 для детального отображения карточки по ID`**

### В общих чертах разобрали `F` объекты
- Для `get_detail_card_by_id` сделали увеличение просмотров на + 1 через `F` объект

**commit: `lesson_50: F объект для увеличения просмотров карточки`**


## Lesson 51

### Подготовили базу данных anki_final.db
```sql
PRAGMA foreign_keys = 0;

--Создание временной таблицы без столбца UserID
CREATE TABLE sqlitestudio_temp_table AS SELECT CardID, Question, Answer, CategoryID, UploadDate, Views, Favorites FROM Cards;

--Удаление оригинальной таблицы Cards
DROP TABLE Cards;

--Создание новой таблицы Cards без столбца UserID
 CREATE TABLE Cards (
 CardID INTEGER PRIMARY KEY AUTOINCREMENT,
 Question TEXT NOT NULL,
 Answer TEXT NOT NULL,
 CategoryID INTEGER,
 UploadDate DATETIME DEFAULT (datetime('now')),
 Views INTEGER DEFAULT (0),
 Favorites INTEGER DEFAULT (0),
 FOREIGN KEY (CategoryID) REFERENCES Categories (CategoryID) ON DELETE SET NULL ON UPDATE CASCADE
);

--Копирование данных обратно в Cards из временной таблицы
INSERT INTO Cards (CardID, Question, Answer, CategoryID, UploadDate, Views, Favorites)
SELECT CardID, Question, Answer, CategoryID, UploadDate, Views, Favorites FROM sqlitestudio_temp_table;

--Удаление временной таблицы
DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;
```

### написали новые модели
- описали модель Tag
- описали модель CardTag
- описали модель Category

### сделали миграцию
- старые миграции удалены
- заново применены 18 базовых миграции
- сделана фейковая миграция `python manage.py migrate --fake` для того чтобы 
Django "думал", что он сам создал наши новые таблицы

**commit: `lesson_51: подключили базу данных anki_final.db`**

- переписали шаблоны под изменившуюся логику модели Tag

**commit: `lesson_51: поправили код шаблонов карточек для отображения из БД`**

- установили библиотеку `markdown`
- написали функцию конвертации `MarkDown` в `HTML`
- подключили шаблонный тэг `markdown_to_html` в детальное представление карточки
- подключили шаблонный тэг `markdown_to_html` в отображение каталога карточек
- подключили `Highlight.js` для подсветки синтаксиса

**commit: `lesson_51: добавили конвертацию MD в HTML и подсветку кода`**

- добавили маршрут `tags/<int:tag_id>/` для отображения карточек по конкретному тэгу
- написали представление `get_cards_by_tag`
- поменяли шаблоны `card_detail.html` и `card_preview.html` для добавления кликабельности тэгам

**commit: `lesson_51: добавили кликабельные тэги`**


## Lesson 52

- установили отладочную панель Django (`pip install django-debug-toolbar==4.0.0`) и настроили её
- убедились в том, что наше приложение генерирует слишком много запросов

**commit: `lesson_52: установили отладочную панель Django`**

- включили жадную загрузку и снизили количество запросов до 4

**commit: `lesson_52: включили жадную загрузку`**

- включили кэширование данных

**commit: `lesson_52: включили кэширование`**

### Примеры Django ORM Запросов

#### CREATE
```python
# создание карточки
card = Card.objects.create(
    question='Python or perl?',
    answer='Python',
)
card.save()

# проверка существования тега и создание нового тега если его не существует
tag, created = Tag.objects.get_or_create(name='IronPython')
# вернётся кортеж, в первом элементе которого будет объект тега, во втором - булевое значение создан ли тег

# создание новой категории
category = Category.objects.create(name='Random')

# добавление тега к карточке со связью многие ко многим
# ???????
```

#### READ
```python
# получение всех карточек
cards = Card.objects.all()

# получение карточки по идентификатору
card = Card.objects.get(id=337)
card = Card.objects.get(pk=337)

# получение всех тегов связанных с карточкой
tags = card.tags.all()

# получение карточек по тегу (два варианта)
cards = Card.objects.filter(tags__name='синтаксис')
cards = Tag.objects.get(name='синтаксис').cards.all()

# получение всех категорий
categories = Category.objects.all()
```

#### UPDATE
```python
# обновление карточки по id
card = Card.objects.get(pk=457)
card.question = 'Как выглядит "Hello, world!" на Python?'
card.save()

# изенение имени категории
category = Category.objects.get(name='JavaScript')
category.name = 'JS'
category.save()
```

#### DELETE
```python
# удаление карточки по id 457
card = Card.objects.get(pk=457)
card.delete()

# удаление категории по имени
category = Category.objects.get(name='JS')
category.delete()
```

#### Q объекты
```python
from django.db.models import Q

# получение карточек, которые содержат в вопросе слово "Java"
cards = Card.objects.filter(question__contains='Java')

# получение карточек, которые содержат слово "Java" в вопросе или ответе
cards = Card.objects.filter(Q(question__contains='Java') | Q(answer__contains='Java'))

# получение только тех карточек, которые содержат слова "Java" в вопросе и ответе
cards = Card.objects.filter(Q(question__contains='Java') & Q(answer__contains='Java'))
```

#### F объекты
```python
from django.db.models import F

# Увеличение количества просмотров на 1 для всех карточек
Card.objects.update(views=F("views") + 1)

# Установка количества добавлений в избранное равным количеству просмотров
Card.objects.update(adds=F("views"))

# Добавление 10 просмотров каждой карточке, ответ которой содержит слово SQL
Card.objects.filter(Q(answer__icontains="SQL")).update(views=F("views") + 10)
```

**commit: `lesson_52: посмотрели запросы Django ORM на CRUD`**


## Lesson 53

- добавили поля для отображения в админ. панели с помощью `list_display`
- пометили поля, которые будут ссылками с помощью `list_display_links`
- добавили поля по которым будет проводиться поиск с помощью `search_fields`
- добавили поля по которым будет проводиться фильтрация с помощью `list_filter`

**commit: `lesson_53: провели первоначальную настройку админ. панели`**


- добавили сортировку по категории по возрастанию  и по просмотрам по убыванию с помощью `ordering`
- изменили количество отображаемых карточек на странице админ. панели с помощью `list_per_page`
- задали поля, которые можно менять напрямую `list_editable`

**commit: `lesson_53: дополнительные настройки амдин. панели`**

- познакомились с методом `get_absolute_url`
В Django метод `get_absolute_url` используется в моделях для получения URL-адреса, который однозначно
идентифицирует объект модели.
Полезен для создания ссылок на конкретные модели, например в админ. панели Django или в шаблонах.

**commit: `lesson_53: get_absolute_url для создания URL-адреса`**

- поменяли надписи в шапке, заголовке и на экране приветствия админ. панели

**commit: `lesson_53: изменили заголовок, экран приветствия и шапку админ. панели`**

- поменяли заголовок, тайтл и приветствие в админ. панели в файле `anki\urls.py`
- перевели все поля в админ. панели на русский язык с помощью параметра `verbose_name` в каждом поле модели `Card`

**commit: `lesson_53: перевели все поля в админ. панели на русский язык`**

#### добавили поле `status` в модель `Card`
- тип `BooleanField` используется для хранения булевых значений (`True` или `False`).
- параметр `choices` используется для ограничения возможных значений поля и для удобного отображения этих значений в админке Django.
- В данном случае, `choices` задается с помощью `tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices))`.

_нам нужно было ограничить значения поля `status` только двумя возможными состояниями: `True` (Проверено) и `False` (Не проверено).
Для этого используется `BooleanField`, который по своей сути ограничивает значения до двух возможных вариантов._

- `Status.choices` возвращает кортеж кортежей вида `((0, 'Не проверено'), (1, 'Проверено'))`.
- С помощью `map(lambda x: (bool(x[0]), x[1]), Status.choices)` эти значения преобразуются в булевы значения: `((False, 'Не проверено'), (True, 'Проверено'))`.
- Это позволяет использовать `BooleanField` с человеко-читаемыми именами для значений.

**commit: `lesson_53: добавили поле status`**

- добавили в админ. панель поле указывающее на наличие кода в ответе карточки
- добавили в админ. панель дополнительные действия: пометить карточки как проверенные и как не проверенные

**commit: `lesson_53: добавили в админ. панель поле наличие кода и дополнительные действия`**

##### Класс `CardCodeFilter`
Наследуется от `SimpleListFilter`, который предоставляет базовую функциональность для создания простых фильтров в админке Django.

##### Атрибут `title`
Задает название фильтра, которое будет отображаться в админке. В данном случае, это "Наличие кода".

##### Атрибут `parameter_name`
Задает имя параметра, которое будет использоваться в URL для фильтрации. В данном случае, это `has_code`.

##### Метод `lookups`
Возвращает кортеж кортежей, где каждый внутренний кортеж состоит из двух элементов: значения параметра и человеко-читаемого названия.
В данном случае, возвращаются два варианта: `('yes', 'Да')` и `('no', 'Нет')`.

##### Метод `queryset`
Принимает запрос `request` и исходный набор данных `queryset`.
В зависимости от значения параметра `has_code` (которое можно получить с помощью `self.value()`), фильтрует набор данных.
Если значение параметра `has_code` равно `yes`, фильтрует набор данных, чтобы включить только те карточки, в которых поле `answer` содержит строку с тремя тиками.
Если значение параметра `has_code` равно `no`, фильтрует набор данных, чтобы исключить карточки, в которых поле `answer` содержит строку с тремя тиками.

**commit: `lesson_53: добавили кастомный фильтр по наличию кода в ответе карточки`**

- установили `django-jazzmin` и настроили его
- `pip install django-jazzmin`
- Добавил `jazzmin` в `INSTALLED_APPS` в файле `settings.py`

**commit: `lesson_53: установил и настроил django-jazzmin`**


## Lesson 54

- Сделал копию служебного шаблона `change_form.html` и вклинились в `{% block after_field_sets %}`
- Добавил в админке карточек кнопку "Создать карточку с тегами" `{% block object-tools-items %}`

**commit: `lesson_54: кастомизация шаблона change_form.html`**