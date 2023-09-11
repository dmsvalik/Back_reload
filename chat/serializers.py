# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from chat.models import MessageModel
# from rest_framework.serializers import ModelSerializer, CharField
# from main_page.models import UserAccount

# class MessageModelSerializer(ModelSerializer):
#     user = CharField(source='user.name', read_only=True)
#     recipient = CharField(source='recipient.name')

#     # при создании письма и отправке в чате приходит сюда пост запрос из JS функции function sendMessage(recipient, body)
#     def create(self, validated_data):
#         for item in validated_data:
#             print(item)
#         print(validated_data['recipient'])

#         user = self.context['request'].user

#         recipient = get_object_or_404(
#             UserAccount, name=validated_data['recipient']['name'])
#         msg = MessageModel(recipient=recipient,
#                            body=validated_data['body'],
#                            user=user)
#         msg.save()
#         return msg

#     class Meta:
#         model = MessageModel
#         fields = ('id', 'user', 'recipient', 'timestamp', 'body')


# class UserModelSerializer(ModelSerializer):
#     class Meta:
#         model = UserAccount
#         fields = ('name', 'email',)
