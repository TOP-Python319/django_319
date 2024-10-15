import asyncio

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from anki.settings import TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, DEBUG
from cards.models import Card
from .telegram_bot import send_telegram_message


MESSAGE_TEMPLATE = """
*Вопрос:* {instance.question}
*Ответ:* {instance.answer}
*Категория:* {instance.category}
*Автор:* {instance.author}
"""


@receiver(post_save, sender=Card)
def send_telegram_notification_on_save(sender, instance, created, **kwargs):

    if DEBUG:
        card_link = f'127.0.0.1:8000/cards/{instance.id}/detail/'
    else:
        card_link = f'cardslurm.ru/cards/{instance.id}/detail/'

    if created:
        message = f'*Новая карточка!*\n{card_link}\n' + MESSAGE_TEMPLATE.format(instance=instance)
    else:
        message = f'*Карточка обновлена!*\n{card_link}\n' + MESSAGE_TEMPLATE.format(instance=instance)

    asyncio.run(send_telegram_message(
        TELEGRAM_BOT_TOKEN,
        YOUR_PERSONAL_CHAT_ID,
        message
    ))


@receiver(post_delete, sender=Card)
def send_telegram_notification_on_delete(sender, instance, **kwargs):
    asyncio.run(send_telegram_message(
        TELEGRAM_BOT_TOKEN,
        YOUR_PERSONAL_CHAT_ID,
        f'*Карточка {instance.id} удалена пользователем {instance.author}!*'
    ))
