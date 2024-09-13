import os

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .forms import CardForm, UploadFileForm
from .models import Card


info = {
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
    """Класс-миксин для добавления меню в контекст шаблона и для кеширования cards_count, users_count и menu
    """

    timeout = 30

    def get_menu(self):
        menu = cache.get('menu')

        if not menu:
            menu = info['menu']
            cache.set('menu', menu, self.timeout)
        return menu

    def get_cards_count(self):
        cards_count = cache.get('cards_count')

        if not cards_count:
            cards_count = Card.objects.count()
            cache.set('cards_count', cards_count, self.timeout)
        return cards_count

    def get_users_count(self):
        users_count = cache.get('users_count')

        if not users_count:
            users_count = get_user_model().objects.count()
            cache.set('users_count', users_count, self.timeout)
        return users_count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.get_menu()
        context['users_count'] = self.get_users_count()
        context['cards_count'] = self.get_cards_count()
        return context


class IndexView(MenuMixin, TemplateView):
    template_name = 'main.html'


class AboutView(MenuMixin, TemplateView):
    template_name = 'about.html'


class CatalogView(MenuMixin, ListView):
    model = Card  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'cards/catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'cards'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 30  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        sort = self.request.GET.get('sort', 'upload_date')
        order = self.request.GET.get('order', 'desc')
        search_query = self.request.GET.get('search_query', '')

        # Определение направления сортировки
        if order == 'asc':
            order_by = sort
        else:
            order_by = f'-{sort}'

        # Фильтрация карточек по поисковому запросу и сортировка
        if search_query:
            queryset = Card.objects.filter(
                Q(question__iregex=search_query) |
                Q(answer__iregex=search_query) |
                Q(tags__name__iregex=search_query)
            ).prefetch_related('tags').select_related('category').order_by(order_by).distinct()
        else:
            queryset = Card.objects.prefetch_related('tags').select_related('category').order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        # Добавление дополнительных данных в контекст
        context['sort'] = self.request.GET.get('sort', 'upload_date')
        context['order'] = self.request.GET.get('order', 'desc')
        context['search_query'] = self.request.GET.get('search_query', '')

        return context


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


class CardDetailView(MenuMixin, DetailView):
    model = Card
    template_name = 'cards/card_detail.html'
    context_object_name = 'card'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        Card.objects.filter(pk=obj.pk).update(views=F('views') + 1)

        return obj


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


class AddCardCreateView(CreateView):
    model = Card
    form_class = CardForm
    template_name = 'cards/add_card.html'
    success_url = reverse_lazy('catalog')


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
