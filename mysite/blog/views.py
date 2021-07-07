from django.core.paginator import (
    Paginator, EmptyPage, PageNotAnInteger
)
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.


def post_list(request):
    """
    View that returns all published posts
    """
    object_list = Post.published.all() # all published posts
    paginator = Paginator(object_list, 3) # 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page not an int then return first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range then return last page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    """
    View that shows individual post
    """
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, 'blog/post/detail.html', {'post': post})
