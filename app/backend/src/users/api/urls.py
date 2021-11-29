from rest_framework import routers

from users.api.views import UserViewSet, UserListViewSet

router = routers.DefaultRouter()
router.register('clients/create', UserViewSet)
router.register('list', UserListViewSet, basename='UserList')
urlpatterns = router.urls