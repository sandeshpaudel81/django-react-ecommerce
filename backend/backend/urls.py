"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# base url configuration

urlpatterns = [
    # all routes related to admin:
    path('admin/', admin.site.urls),
    # all routes related to product:
    path('api/products/', include('base.urls.product_urls')),
    # all routes related to orders:
    path('api/orders/', include('base.urls.order_urls')),
    # all routes related to users
    path('api/users/', include('base.urls.user_urls')),
]

# url routes for media files (user uploaded images, files, etc.)
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
