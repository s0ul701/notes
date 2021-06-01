from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.viewsets import UserViewSet

app_name = 'api'

router = SimpleRouter()
router.register('users', UserViewSet, basename='subjects')

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]
