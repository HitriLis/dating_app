from users.api.serializers import UserSerializer, UserSerializerSimple
from users.models import UserProfile, UserFollowing
from rest_framework import viewsets, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from common import mail_sender
import django_filters
from django.db.models.expressions import RawSQL
from django.db.models.functions import Round
from rest_framework.views import APIView


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
       Работа с пользователями системы
    """
    parser_classes = (MultiPartParser,)
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"msg": UserSerializerSimple(serializer.data)}, status=status.HTTP_200_OK)
        else:
            return Response(data={"msg": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserFilter(django_filters.FilterSet):
    distance = django_filters.NumberFilter(field_name='distance', lookup_expr='lte')

    class Meta:
        model = UserProfile
        fields = ['gender', 'distance']


class UserListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
      Списка участников
    """
    serializer_class = UserSerializerSimple
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name']
    filter_class = UserFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        latitude = self.request.user.latitude
        longitude = self.request.user.longitude

        gcd_formula = "6371 * acos(least(greatest(\
            cos(radians(%s)) * cos(radians(latitude)) \
            * cos(radians(longitude) - radians(%s)) + \
            sin(radians(%s)) * sin(radians(latitude)) \
            , -1), 1)) * 1000"
        distance_raw_sql = RawSQL(
            gcd_formula,
            (latitude, longitude, latitude)
        )
        return UserProfile.objects.exclude(id=self.request.user.id) \
            .exclude(latitude__isnull=True) \
            .exclude(longitude__isnull=True).all() \
            .annotate(distance=Round(distance_raw_sql)) \
            .order_by('distance')


class UserViewMatch(APIView):
    """
       Оценка пользователя
    """

    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
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
