from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('MIaC.urls'), name='user-list'),
    path('silk/', include('silk.urls', namespace='silk')),
]
