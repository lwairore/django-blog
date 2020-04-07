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
    """

    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
