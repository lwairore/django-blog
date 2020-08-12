from django.shortcuts import render, get_object_or_404
from . import models, forms
from django.core.paginator import Paginator, EmptyPage, \
        PageNotAnInteger
from django.views.generic import ListView
from .email import mail_message
from django.conf import settings
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

# Create your views here.
class PostListView(ListView):
    queryset = models.Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    object_list = models.Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = forms.CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = models.Post.published.filter(tags__in=post_tags_ids)\
                                .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]
    """
        The preceding code is as follows:
            1. We retrieve a Python list of IDs for the tags of the current post. The  `values_list()` QuerySet returns tuples with the values for the given fields. We pass `flat=True` to it to get a flat list like `[1, 2, 3, ...]`.
            2. We get all posts that contain any of these tags, excluding the current post itself.
            3. We use the `Count` aggregation function to generate a calculated field—`same_tags`— that
                contains the number of tags shared with all the tags queried.
            4. We order the result by the number of shared tags (descending order) and by `publish` to 
                display recent posts first for the posts with the same number of shared tags. We slice the result
                only the first four posts.
    """

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


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
            mail_message(cd, post, post_url)
            sent = True
    else:
        form = forms.EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


def post_search(request):
    form = forms.SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = models.Post.objects.annotate(
                    similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gt=0.3).order_by('-similarity')
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})