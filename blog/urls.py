from django.urls import path
from . import views, sitemaps, feeds
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

app_name = 'blog'

sitemaps = {
    'posts': sitemaps.PostSitemap,
}

"""
        We use angle brackets to capture the values from the URL.
        Any value specified in the URL pattern as `<parameter>` is captured as a string.
        We use path converters, such as `<int:year>` to specifically match and return
        an integer and `<slug:post>` to specifically match a slug (a string consisting of ASCII letters or numbers, plus the hyphen and underscore characters))
        
        You can see all path converters provided by Django at https://docs.djangoproject.com/en/2.0/topics/http/urls/#path-converters.

        If using `path()` and converters isn't sufficient for you, you can use `re_path()` instead to define complex URL patterns with Python regular expressions. You can learn more about defining URL patterns with regular expressions at https://docs.djangoproject.com/en/2.0/ref/urls/#django.urls.re_path.

    """
urlpatterns = [
    # path('', views.PostListView.as_view(), name='post_list'),
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', feeds.LatestPostsFeed(), name='post_feed'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)