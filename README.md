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