from django.http import HttpResponse
from django.shortcuts import render


def main(request):
    return HttpResponse('Hello, world!')  # Вернёт страницу с надписью "Hello world!"


def info(request):
    return HttpResponse('info')


def get_all_cards(request):
    return render(request, 'cards/catalog.html')


def get_card_by_id(request, card_id):
    if card_id > 10:
        return HttpResponse('Такой карточки нет', status=404)
    return HttpResponse(f'Карточка {card_id}')  # Вернёт страницу с надписью "Вы открыли карточку {card_id}"