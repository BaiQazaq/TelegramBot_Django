# Create your views here.
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from decouple import config

from .models import UserProfile, Message
from .utility_methods import send_message, TELEGRAM_API_URL, delete_prefix



class Tg_dj_View(APIView):
    authentication_classes = []  
    permission_classes = []

    def post(self, request, token):
        if token != config('SECRET_TOKEN'):
            return Response({"error": "Forbidden"}, status=403)

        message = request.data.get('message')
        if not message:
            return Response({"error": "No message"}, status=400)

        chat_id = message['chat']['id']
        text = message.get('text', '')
        first_name = message['from'].get('first_name')
        username = message['from'].get('username')

        user, _ = UserProfile.objects.get_or_create(
            telegram_chat_id=chat_id,
            defaults={'first_name': first_name, 'username': username}
        )
        user.first_name = first_name
        user.username = username
        user.save()

        if text.strip() == '/start':
            send_message(chat_id, f"Привет, {first_name or 'друг'}!")

        elif text.strip() == '/message':
            msg_text = f"Это сообщение будет удалено через 5 минут для пользователя {first_name}"
            telegram_message_id = send_message(chat_id, msg_text)

            Message.objects.create(
                user=user,
                text=msg_text,
                telegram_message_id=telegram_message_id,
                deleted=False,
                deleted_at=None
            )
        elif text.strip() == '/clear':
            time_limit = timezone.now() - timedelta(minutes=5)
            messages_to_delete = Message.objects.filter(user=user, deleted=False, created_at__gte=time_limit)

            deleted_count = 0
            for msg in messages_to_delete:
                payload = {
                    'chat_id': chat_id,
                    'message_id': msg.telegram_message_id
                }
                response = requests.post(TELEGRAM_API_URL+delete_prefix, data=payload)
                if response.ok:
                    msg.deleted = True
                    msg.deleted_at = timezone.now()
                    msg.save()
                    deleted_count += 1

            send_message(chat_id, f"Удалено сообщений: {deleted_count}")

        else:
            send_message(chat_id, "Набери /start, /message или /clear" )

        return Response({"ok": True})


