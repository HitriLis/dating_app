from users.api.serializers import UserSerializer
from users.models import UserProfile, UserFollowing
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from common import mail_sender

class UserViewSet(viewsets.ModelViewSet):
    """
       Работа с пользователями системы
    """
    parser_classes = (MultiPartParser,)
    queryset = UserProfile.objects.all()

    # def get_permissions(self):
    #     if not self.action == 'create':
    #         return [IsAuthenticated()]
    #     return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        return None

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"msg": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"msg": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['POST'], detail=True)
    def match(self, request, pk=None):
        subscriber = request.user
        user = get_object_or_404(UserProfile, pk=pk)
        if not subscriber == user:
            subscriber = request.user
            user = get_object_or_404(UserProfile, pk=pk)
            obj, created = UserFollowing.objects.get_or_create(
                defaults={
                    "user": user
                },
                user=user
            )
            obj.subscribers.add(subscriber)
            obj.save()
            signed = UserFollowing.objects.filter(user=subscriber, subscribers__pk=pk)
            if signed:
                mail_sender(user, subscriber)
                return Response(data={'email': user.email}, status=status.HTTP_200_OK)
            return Response(data={'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'You can not subscribe to yourself'}, status=status.HTTP_400_BAD_REQUEST)

    http_method_names = ['post']
