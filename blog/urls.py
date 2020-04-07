from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    """
        We use angle brackets to capture the values from the URL.
        Any value specified in the URL pattern as `<parameter>` is captured as a string.
        We use path converters, such as `<int:year>` to specifically match and return
        an integer and `<slug:post>` to specifically match a slug (a string consisting of ASCII letters or numbers, plus the hyphen and underscore characters))
        
        You can see all path converters provided by Django at https://docs.djangoproject.com/en/2.0/topics/http/urls/#path-converters.

        If using `path()` and converters isn't sufficient for you, you can use `re_path()` instead to define complex URL patterns with Python regular expressions. You can learn more about defining URL patterns with regular expressions at https://docs.djangoproject.com/en/2.0/ref/urls/#django.urls.re_path.

    """
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)