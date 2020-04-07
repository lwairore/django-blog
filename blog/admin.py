from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """
        We are telling the Django admin site that our model is registered
        in the admin site using a custom class that inherits from `ModelAdmin`.

        In this class, we can include information about how to display the model in the admin site and how to interact with it. 

        The `list_display` attribute allows you to set the fields of your model that you want to display
        in the admin object list page.

        The `@admin.register()` decorator performs the same function as the 
        `admin.site.register()` function, registering the `ModelAdmin` class that it decorates.

        The `search_fields` attribute will allow a search bar to appear.
        Below the search bar, there will be navigation links to navigate through a date hierarchy:
        this has been defined by the `date_hierarchy` attribute.

        Posts will be ordered by Status and Publish columns by default. We have specified the default order using the `ordering` attribute.

        When Adding Post link as yo type the title of a new post, the `slug` field
        is filled in automatically. We have told Django to prepopulate the `slug` field with the input of the `titile`
        field using the `prepopulated_fields` attribute. 

        The `author` field is displayed with a lookup widget that can scale much better than a drop-down select input when you have 1000s of
        users.
    """

    list_filter = ('status', 'created', 'publish', 'author')    
    search_fields = ('title', 'body')    
    prepopulated_fields = {'slug': ('title',)}    
    raw_id_fields = ('author',)    
    date_hierarchy = 'publish'    
    ordering = ('status', 'publish')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')