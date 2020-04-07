"""
    Django has a built-in syndication feed framework that you can use to dynamically generate RSS or Atom feeds in a similar manner to creating sitemaps using the site's framework. A web feed is a data format (usually XML) that provides users with frequently updated content. Users will be able to subscribe to your feed using a feed aggregator, a software that is used to read feeds and get new content notifications.
"""

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from . import models

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    def items(self):
        return models.Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)