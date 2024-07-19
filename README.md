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