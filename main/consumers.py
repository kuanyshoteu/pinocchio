import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from accounts.models import Profile, Notification
from django.utils import timezone

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connect yes ')
        user = self.scope['user']
        profile = self.get_profile(user)
        for school in profile.schools.all():
            school_room = "school_" + str(school.id)
            await self.channel_layer.group_add(
                school_room,
                self.channel_name
            )
        self.chat_room = "school_" + str(profile.schools.first().id)
        self.my_room = "school_" + str(profile.schools.first().id)
        await self.send({
            "type":"websocket.accept",
        })

    async def websocket_receive(self, event):
        user = self.scope['user']
        profile = self.get_profile(user)
        post_text = event.get('text', None)
        if post_text is not None:
            loaded_data = json.loads(post_text)
            text = loaded_data.get('text')
            image_url = ''
            if profile.image:
                image_url = profile.image.url
            my_response = {
                'message':text,
                'author':profile.first_name,
                'image_url':image_url,
                'time':timezone.now().strftime('%d %B %Yг. %H:%M'),
            }
            print('********')
            self.create_notification(profile, text, '')
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"chat_message",
                    "text":json.dumps(my_response),
                }
            )

    async def chat_message(self, event):
        await self.send({
            "type":"websocket.send",
            "text":event['text']
        })

    async def websocket_disconnect(self, event):
        print('disconnect')

    def get_profile(self, me):
        return Profile.objects.get(user=me)

    def create_notification(self, profile, text, url):
        for pr in profile.schools.first().people.all():
            if pr.skill:
                skill = pr.skill
                skill.notifications_number += 1
                skill.save()
        image_url = 'None'
        if profile.image:
            image_url = profile.image.url
        Notification.objects.create(
            text = text,
            author_profile = profile,
            school = profile.schools.first(),
            itstype = 'news',
            url = url,
            image_url = image_url
        )
