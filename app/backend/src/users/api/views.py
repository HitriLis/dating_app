from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import get_user_model
from users.api.serializers import UserSerializer
from rest_framework import mixins

User = get_user_model()



class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Работа с пользователями системы
    """
    parser_classes = (MultiPartParser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)




    # @permission_required('permissions.users.edit')
    # @action(methods=['PUT'], detail=True)
    # def avatar_set(self, request, pk=None):
    #     user = get_object_or_404(User, pk=pk)
    #     serializer = UserUpdateAvatarSerializer(user, data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return self.retrieve(request, pk)
