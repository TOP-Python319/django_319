import os

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .forms import CardForm, UploadFileForm
from .models import Card


info = {
    "users_count": 100500,
    "cards_count": 200600,
    # "menu": ['Главная', 'О проекте', 'Каталог']
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
        {"title": "Каталог",
         "url": "/cards/catalog/",
         "url_name": "catalog"},
    ],
}


class MenuMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = info['menu']
        return context


class IndexView(MenuMixin, TemplateView):
    template_name = 'main.html'


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = info['menu']
        return context


# @cache_page(60 * 15)
def catalog(request):
    """Функция для отображения страницы "Каталог"
    будет возвращать рендер шаблона /templates/cards/catalog.html
    - **`sort`** - ключ для указания типа сортировки с возможными значениями: `date`, `views`, `adds`.
    - **`order`** - опциональный ключ для указания направления сортировки с возможными значениями: `asc`, `desc`. По умолчанию `desc`.
    1. Сортировка по дате добавления в убывающем порядке (по умолчанию): `/cards/catalog/`
    2. Сортировка по количеству просмотров в убывающем порядке: `/cards/catalog/?sort=views`
    3. Сортировка по количеству добавлений в возрастающем порядке: `/cards/catalog/?sort=adds&order=asc`
    4. Сортировка по дате добавления в возрастающем порядке: `/cards/catalog/?sort=upload_date&order=asc`
    """

    # считаем параметры из GET-запроса
    sort = request.GET.get('sort', 'upload_date')  # по умолчанию сортируем по дате загрузки
    order = request.GET.get('order', 'desc')  # по умолчанию сортируем по убыванию
    search_query = request.GET.get('search_query', '')  # поиск по карточкам
    page_number = request.GET.get('page', 1)

    # Проверяем дали ли мы разрешение на сортировку по этому полю
    valid_sort_fields = {'upload_date', 'views', 'adds'}

    # Обрабатываем сортировку
    if sort not in valid_sort_fields:
        sort = 'upload_date'

    # Обрабатываем направление сортировки
    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    # Обрабатываем поиск
    if not search_query:
        # Получим ВСЕ карточки для представления в каталоге в ЖАДНОМ РЕЖИМЕ
        # `select_related` используется для оптимизации запросов,
        # когда необходимо получить связанные объекты через "один ко многим" или "один к одному" отношения.
        # Это уменьшает количество запросов к базе данных, выполняя более сложный запрос с JOIN'ами, но возвращая все необходимые данные за один запрос.
        # `prefetch_related` применяется в случаях, когда связи "многие ко многим" или обратные связи "один ко многим" присутствуют.
        # В отличие от `select_related`, `prefetch_related` выполняет отдельный запрос для каждой связи, но затем объединяет результаты в Python,
        # что может существенно сократить время выполнения запроса при работе с большими объемами данных.
        cards = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)
    else:
        # пробуем получить карточки по поиску в ЛЕНИВОМ РЕЖИМЕ
        # cards = Card.objects.filter(question__icontains=search_query).order_by(order_by)

        # возвращаем ЖАДНЫЙ РЕЖИМ
        # cards = Card.objects.\
        #     filter(question__icontains=search_query).\
        #     prefetch_related('tags').\
        #     select_related('category').\
        #     order_by(order_by)

        # добавляем поиск по ответам
        # cards = Card.objects.\
        #     filter(Q(question__icontains=search_query) | Q(answer__icontains=search_query)).\
        #     prefetch_related('tags').\
        #     select_related('category').\
        #     order_by(order_by)

        # добавляем поиск по тегам
        cards = Card.objects.\
            filter(
                Q(question__icontains=search_query) |
                Q(answer__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).\
            prefetch_related('tags').\
            select_related('category').\
            order_by(order_by).\
            distinct()

    # создаём объект пагинанатора и устанавалиавем кол-во элементов на странице
    paginator = Paginator(cards, 25)

    # получаем нужную страницу
    page_obj = paginator.get_page(page_number)

    # Подготовим контекст для шаблона
    context = {
        'cards': cards,
        'cards_count': len(cards),
        'menu': info['menu'],
        'page_obj': page_obj,
        'sort': sort,
        'order': order,
    }

    response = render(request, 'cards/catalog.html', context)

    # теперь браузер заново загружает страницу при нажатии кнопки НАЗАД в браузере
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate'  # кэш не используется
    response['Expires'] = 0  # перестраховка, кэш устаревает через 0 секунд

    return response


def get_categories(request):
    """
    Возвращает все категории для представления в каталоге
    """
    # Проверка работы базового шаблона
    return render(request, 'base.html', info)


def get_cards_by_category(request, slug):
    """
    Возвращает карточки по категории для представления в каталоге
    """
    return HttpResponse(f'Cards by category {slug}')


def get_cards_by_tag(request, tag_id):
    """
    Возвращает карточки по тегу для представления в каталоге
    """
    cards = Card.objects.filter(tags__id=tag_id)

    # Подготовим контекст для шаблона
    context = {
        'cards': cards,
        'menu': info['menu']
    }

    return render(request, 'cards/catalog.html', context=context)


def get_detail_card_by_id(request, card_id):
    """
    Возвращает детальную информацию по карточке для представления
    """
    # если в БД нет карточки с таким id, то возвращаем 404
    card = get_object_or_404(Card, id=card_id)

    # Обновляем счётчик просмотров по карточке
    card.views = F('views') + 1
    card.save()

    card.refresh_from_db()  # обновляем карточку в БД

    context = {
        'card': card,
        'menu': info['menu']
    }

    return render(request, 'cards/card_detail.html', context=context)


def preview_card_ajax(request):
    if request.method == "POST":
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        category = request.POST.get('category', '')

        # Генерация HTML для предварительного просмотра
        html_content = render_to_string('cards/card_detail.html', {
            'card': {
                'question': question,
                'answer': answer,
                'category': category,
                'tags': ['тест', 'тег'],

            }
        }
                                        )
        return JsonResponse({'html': html_content})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# def add_card(request):
#     if request.method == "POST":
#         form = CardForm(request.POST)
#         if form.is_valid():

#             # Сохраняем карточку в БД
#             card = form.save()

#             # Перенаправляем пользователя на страницу карточки
#             return redirect(card.get_absolute_url())
#     else:
#         form = CardForm()

#     context = {
#         'form': form,
#         'menu': info['menu']
#     }

#     return render(request, 'cards/add_card.html', context=context)

class AddCardView(View):

    """Обработка GET-запроса для добавления карточки
    """
    def get(self, request):
        form = CardForm()
        return render(request, 'cards/add_card.html', {'form': form})


    """Обработка POST-запроса для добавления карточки
    если форма валидна, то сохраняем карточку в БД
    иначе отображаем форму с ошибками
    """
    def post(self, request):
        form = CardForm(request.POST)
        if form.is_valid():
            # Сохраняем карточку в БД
            card = form.save()

            # Перенаправляем пользователя на страницу карточки
            return redirect(card.get_absolute_url())
        return render(request, 'cards/add_card.html', {'form': form})


def handle_uploaded_file(f):
    # Создаем путь к файлу в директории uploads, имя файла берем из объекта f
    file_path = f'uploads/{f.name}'

    # Создаем папку uploads, если ее нет
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


    # Открываем файл для записи в бинарном режиме (wb+)
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return file_path


def add_card_by_file(request):
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Записываем файл на диск
            file_path = handle_uploaded_file(request.FILES['file'])

            # Редирект на страницу каталога после успешного сохранения
            return redirect('catalog')
    else:
        form = UploadFileForm()
    return render(request, 'cards/add_file_card.html', {'form': form})
