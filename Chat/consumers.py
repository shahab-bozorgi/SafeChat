# import json
#
# from channels.db import database_sync_to_async
# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from djangochannelsrestframework.observer import model_observer
# from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin, action
# from djangochannelsrestframework.mixins import CreateModelMixin
#
# from Accounts.models import User
# from Chat.api.serializers import RoomSerializer, MessageSerializer
# from Chat.models import Room, Message
#
#
# class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     lookup_field = "pk"
#
#     @action()
#     async def create(self, data: dict, request_id: str, **kwargs):
#         response, status = await super().create(data, **kwargs)
#         room_pk = response["pk"]
#         await self.subscribe_instance(request_id=request_id, pk=room_pk)
#         return response, status
#
#     @action()
#     async def join_room(self, pk, request_id, **kwargs):
#         room = await database_sync_to_async(self.get_object)(pk=pk)
#         await self.subscribe_instance(request_id=request_id, pk=room.pk)
#         await self.add_user_to_room(room)
#
#     @action()
#     async def leave_room(self, pk, **kwargs):
#         room = await database_sync_to_async(self.get_object)(pk=pk)
#         await self.remove_user_from_room(room)
#         await self.unsubscribe_instance(pk=room.pk)
#
#     @database_sync_to_async
#     def add_user_to_room(self, room: Room):
#         user: User = self.scope["user"]
#         room.current_users.add(user)
#
#     @database_sync_to_async
#     def remove_user_from_room(self, room: Room):
#         user: User = self.scope["user"]
#         room.current_users.remove(user)
#
#     @action()
#     async def create_message(self, message, room, **kwargs):
#         room: Room = await database_sync_to_async(self.get_object)(pk=room)
#         await database_sync_to_async(Message.objects.create)(
#             room=room,
#             user=self.scope["user"],
#             text=message
#         )
#
#     @model_observer(Message)
#     async def message_activity(
#             self,
#             message,
#             observer=None,
#             subscribing_request_ids=[],
#             **kwargs
#     ):
#         """
#         This is evaluated once for each subscribed consumer.
#         The result of `@message_activity.serializer` is provided here as the message.
#         """
#         # Since we provide the request_id when subscribing, we can just loop over them here.
#         for request_id in subscribing_request_ids:
#             message_body = dict(request_id=request_id)
#             message_body.update(message)
#             await self.send_json(message_body)
#
#     @message_activity.groups_for_signal
#     def message_activity(self, instance: Message, **kwargs):
#         yield f'room__{instance.room_id}'
#
#     @message_activity.groups_for_consumer
#     def message_activity(self, room=None, **kwargs):
#         if room is not None:
#             yield f'room__{room}'
#
#     @message_activity.serializer
#     def message_activity(self, instance: Message, action, **kwargs):
#         """
#         This is evaluated before the update is sent
#         out to all the subscribing consumers.
#         """
#         return dict(
#             data=MessageSerializer(instance).data,
#             action=action.value,
#             pk=instance.pk
#         )
#
#     @action()
#     async def join_room(self, pk, request_id, **kwargs):
#         room = await database_sync_to_async(self.get_object)(pk=pk)
#         await self.subscribe_instance(request_id=request_id, pk=room.pk)
#         await self.message_activity.subscribe(room=pk, request_id=request_id)
#         await self.add_user_to_room(room)
#
#     @action()
#     async def leave_room(self, pk, **kwargs):
#         room = await database_sync_to_async(self.get_object)(pk=pk)
#         await self.unsubscribe_instance(pk=room.pk)
#         await self.message_activity.unsubscribe(room=room.pk)
#         await self.remove_user_from_room(room)


# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TerminalEchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            "message": "✅ Connection established"
        }))

    async def disconnect(self, close_code):
        print("Disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        response = f"Echo: {data.get('message', '')}"
        await self.send(text_data=json.dumps({
            "message": response
        }))
