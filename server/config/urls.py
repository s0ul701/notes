import json
import yaml

from django.conf import settings
from django.shortcuts import render
from django.urls import include, path

from apps import api


def render_yaml_to_swagger(request):
    with open(settings.SWAGGER_YAML_FILE) as swagger_doc:
        doc = yaml.load(swagger_doc.read())
    return render(
        request, template_name='swagger_base.html',
        context={'data': json.dumps(doc)},
    )


urlpatterns = [
    path('api/', include(api.urls, namespace='api')),
    path('docs/', render_yaml_to_swagger, name='api-doc'),
]

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
