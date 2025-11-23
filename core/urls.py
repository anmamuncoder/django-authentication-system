from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static 

# GraphQL imports 
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from apps.schema import schema

from drf_spectacular.views import ( 
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView,
)

drf_spectacular_urls = [ 
    # OpenAPI schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI (optional)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

apps_urls = [
    path('auth/',include('apps.users.urls'),name='user'),
    path('auth/',include('apps.verification.urls'),name='verification'),
    path('',include('apps.inventory.urls'),name='inventory'), 
    path('',include('apps.stockshare.urls'),name='stockshare'),
    path('',include('apps.subscription.urls'),name='subscription'),
    
]

# GraphQL URL patterns
graphql_urlpatterns = [ 
    # csrf_exempt =  Disable CSRF for this view so that POST requests from Postman or frontend work easily
    path('api/graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    
]

urlpatterns = (
    [
        path('admin/', admin.site.urls),
    ] 
    + drf_spectacular_urls
    + apps_urls
    + graphql_urlpatterns
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

 