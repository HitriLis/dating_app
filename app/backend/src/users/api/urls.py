from rest_framework import routers
from django.urls import path
from users.api.views import UserViewSet, UserListViewSet, UserViewMatch

router = routers.DefaultRouter()
router.register('clients/create', UserViewSet, basename='user-view')
router.register('list', UserListViewSet, basename='user-list')

urlpatterns = [
    path('clients/<int:pk>/match', UserViewMatch.as_view(), name='user-match')
] + router.urls