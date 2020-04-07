from django.shortcuts import render, get_object_or_404
from . import models

# Create your views here.
def post_list(request):
    """
        The `post_list` view takes the `request` object as the only parameter.
        In this view, we are retrieving all the posts with the `published` status using the `published` manager
        we created earlier.

        Finally, we are using the `render()` shortccut provided by Django to render the list of
        posts with the given template. This function takes:
            1. the `request` object,
            2. the template path,
            3. and the context variables to render the given template.
        It returns an `HttpResponse` object wiht the rendered text.
    """
    posts = models.Post.published.all()
    return render(request, 'blog/post/list.html', { 'posts': posts })


def post_detail(request, year, month, day, post):
    """
        This view takes `year`, `month`, `day`, and `post` parameters to retrieve a published
        post with the given slug and date. 
    """
    post = get_object_or_404(models.Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', { 'post': post })