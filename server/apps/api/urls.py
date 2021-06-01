from django.urls import include, path

from . import v1

app_name = 'api'

urlpatterns = [
    path('v1/', include(v1.urls, namespace='v1')),
]
