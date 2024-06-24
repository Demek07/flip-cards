import asyncio
from django.db.models.signals import post_save
from django.dispatch import receiver
from flip_cards.settings import TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID
from flip_cards_app.models import Word
from .telegram_bot import send_telegram_message


# @receiver(post_save, sender=Word)
# def send_telegram_notification(sender, instance, created, **kwargs):
# if created:
# message = f"""*Новая карточка!* *Вопрос:* *Ответ:**Категория:**Автор:* {instance.en_word}"""

# asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message, parse_mode="HTML"))
