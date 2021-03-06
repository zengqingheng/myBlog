"""myBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from apps.blog import views as blog_views
from django.conf.urls.static import static

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'',blog_views.home,name='home'),
    path(r'home/',blog_views.home,name='home'),
    path(r'articles/<int:id>/',blog_views.detail,name='detail'),
    path(r'summernote/',include('django_summernote.urls')),
    path(r'jet/',include('jet.urls','jet')),
    path(r'jet/dashboard/',include('jet.dashboard.urls','jet-dashboard')),
    path(r'tag/<str:tag>/',blog_views.search_tag,name='search_tag'),
    path(r'category/<int:id>/',blog_views.search_category,name='category_menu'),
    path(r'archives/<str:year>/<str:month>',blog_views.archives,name='archives'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)