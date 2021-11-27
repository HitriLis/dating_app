from rest_framework import routers

from users.api.views import UserViewSet

router = routers.DefaultRouter()
router.register('create', UserViewSet)
# router.register('create', UserViewSet)
urlpatterns = router.urls

