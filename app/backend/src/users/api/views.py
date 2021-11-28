from users.api.serializers import UserSerializer
from users.models import UserProfile
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

class UserViewSet(viewsets.ModelViewSet):
    """
       Работа с пользователями системы
    """
    parser_classes = (MultiPartParser,)
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"msg": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"msg": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

    http_method_names = ['post']