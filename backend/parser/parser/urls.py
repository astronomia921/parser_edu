from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('parser_ozon.urls', namespace='parser_ozon'))
]
