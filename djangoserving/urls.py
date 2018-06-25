
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('linear_regression/', include('linear_regression.urls')),
    path('admin/', admin.site.urls),
]
