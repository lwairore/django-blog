from django.contrib.sitemaps import Sitemap
from . import models

"""
    Django comes with a sitemap framework, which allows you to generate sitemaps for your site dynamically. A sitemap is an XML file that tells search engines the pages of your website, their relevance, and how frequently they are updated. Using a sitemap, you will help crawlers that index your website's content.

    The Django sitemap framework depends on `django.contrib.sites`, which allows you to associate objects to particular websites that are running with your project. This comes handy when you want to run multiple sites using a single Django project. To install the sitemap framework, you will need to activate both the sites and the sitemap applications in our project. Edit the
    `settings.py` file of your project and add `django.contrib.sites` and django.contrib.sitemaps to the INSTALLED_APPS setting. Also, define a new setting for the site ID, as follows:
        `
            SITE_ID = 1

            # Application definition
            INSTALLED_APPS = [
                # ...
                'django.contrib.sites',
                'django.contrib.sitemaps',
            ]
        `
        

    Now, run the following command to create the tables of the Django site application in the database:
        `python manage.py migrate`

    The `sites` application is now synced witht the database. Now create a new file inside your `blog`
    application directory and name it `sitemaps.py`.
"""

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return models.Post.published.all()

    def lastmod(self, obj):
        return obj.updated

    """
        Above we create a custom sitemap by inheriting the `Sitemap` class of the 
        `sitemaps` module. The `changefreq` and `priority` attributes indicate the change frequency of your post pages and their relevance in your website (the maximum value is 1). The
        `items()` method returns the QuerySet of objects to include in this sitemap. By default, Django calls the
        `get_absolute_url()`  method on each object to retrieve its URL. If you want to specify the URL for each object, you can add a
        `location`  method to your sitemap class. The `lastmod` method receives each object returned by `items()` and returns the last time 
        the object was modified. Both `changefreq` and `priority` methods can also 
        be either methods or attributes. You can take a look at the complete sitemap reference in the official Django documentation located at https://docs.djangoproject.com/en/2.0/ref/contrib/sitemaps/.

        Finally, you will just need to add your sitemap URL. Edit the main urls.py file of your project and add the sitemap, as follows:
            `path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
                    name='django.contrib.sitemaps.views.sitemap')`
    """