from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from  django.urls import reverse

# Create your models here.
class PublishedManager(models.Manager):
    """
        `objects` is the default manager of every model that retrieves all
        objects in the database. However, we can also define custom managers
        for our models. `PublishedManager` is a custom manager that retrieves all posts
        with the `published` status.

        There are two ways to add a manager to your models: 
            1. You can add extra manager methods 
            2. Or modify initial manager QuerySets.
        The first method provides you with a QuerySet API such as `Post.objects.my_manager()`, and
        the later provides you with `Post.my_manager.all()`. The manager will allow us to 
        retrieve posts using `Post.published.all()`.

        The `get_queryset()` method of a manager returns the QuerySet that will be executed. We
        override this method to include our custom filter in the final QuerySet.  

        Usage `Post.published.filter(title__startswith='Who')` to retrieve all published posts whose title starts with `who`.
    """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    """
    We have added the unique_for_date parameter to this field so that we can build URLs for posts using their publish date and slug. Django will prevent multiple posts from having the same slug for a given date.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
            For this method, we will use the `reverse()` method that allows you to build
            URLs by their name and passing optional parameters.

            We can use the `get_absolute_url()` method to link to specific posts.
        """
        return reverse('blog:post_detail', args=[self.publish.year,self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)