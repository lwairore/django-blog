from django.shortcuts import render, get_object_or_404
from . import models, forms
from django.core.paginator import Paginator, EmptyPage, \
        PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
class PostListView(ListView):
    queryset = models.Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# def post_list(request):
#     """
#         The `post_list` view takes the `request` object as the only parameter.
#         In this view, we are retrieving all the posts with the `published` status using the `published` manager
#         we created earlier.

#         Finally, we are using the `render()` shortccut provided by Django to render the list of
#         posts with the given template. This function takes:
#             1. the `request` object,
#             2. the template path,
#             3. and the context variables to render the given template.
#         It returns an `HttpResponse` object wiht the rendered text.
#     """
#     object_list = models.Post.published.all()
#     paginator = Paginator(object_list, 3) # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)

#     return render(request,
#                   'blog/post/list.html',
#                   {'page': page,
#                    'posts': posts})


def post_detail(request, year, month, day, post):
    """
        This view takes `year`, `month`, `day`, and `post` parameters to retrieve a published
        post with the given slug and date. 
    """
    post = get_object_or_404(models.Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None:
    
    if request.method == 'POST':
        # A comment was posted
        comment_from = forms.CommentForm(data=request.POST)
        if comment_from.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_from.save(commit=False)
            # Assign the current post to the comment
            new_comment.save()
    else:
        comment_from = forms.CommentForm()
    return render(request, 'blog/post/detail.html', { 'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_from': comment_from })


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(models.Post, id=post_id, status='published')
    sent = False 
 
    if request.method == 'POST':
        # Form was submitted
        form = forms.EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                          post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = forms.EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})