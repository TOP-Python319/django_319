from django.http import HttpResponse


def main(request):
    return HttpResponse('Hello, world!')  # Вернёт страницу с надписью "Hello world!"


def info(request):
    return HttpResponse('info')


def get_all_cards(request):
    return HttpResponse('Все карточки')  # Вернёт страницу с надписью "Все карточки"


def get_card_by_id(request, card_id):
    if card_id > 10:
        return HttpResponse('Такой карточки нет', status=404)
    return HttpResponse(f'Карточка {card_id}')  # Вернёт страницу с надписью "Вы открыли карточку {card_id}"