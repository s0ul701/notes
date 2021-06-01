from django.conf import settings
from django.urls import include, path

from apps import api

urlpatterns = [path('api/', include(api.urls, namespace='api'))]

if settings.DEBUG:
    from debug_toolbar import urls
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

    urlpatterns += [path('__debug__/', include(urls))]
