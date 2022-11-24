"""ebr_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from frontend.sitemaps import StaticViewSitemap, ReviewCategorySitemap, ReviewBrandSitemap, ReviewSitemap, PagesSitemap

sitemaps = {
    'static': StaticViewSitemap, 'review_category': ReviewCategorySitemap,
    'review_brand': ReviewBrandSitemap, 'review': ReviewSitemap,
    'pages': PagesSitemap
}

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('customadmin/', include("core.urls")),
    path('', include("frontend.urls")),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'frontend/custom_sitemap.html'}),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'frontend.views.handler404'
