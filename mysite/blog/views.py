from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.db.models import Count
from django.urls import reverse
from taggit.models import Tag
from .models import Post, Comment
from .forms import NewPostForm, CommentForm, SearchForm

# Create your views here.


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    """
    View that shows individual post
    """
    # fetch posts
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # fetch comments
    comments = post.comments.filter(active=True)
    # initiate new_comment variable for use when creating a new comment
    new_comment = None
    # posting new comment logic
    if request.method == 'POST':
        # ascertain form is valid
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment and assign post foreign key then save
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            # clear form for refresh
            comment_form = CommentForm()
    else:
        # GET request (page load)
        # instantiate blank comment form
        comment_form = CommentForm()
    # list of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
    })


def new_post(request):
    """
    Form to add a new post
    NOTE: This form is for dev use only
    TODO: productionise
    """
    # if post request then get form, validate and save
    if request.method == 'POST':
        # get form contents from posted page
        form = NewPostForm(request.POST)
        # ensure form is valid
        if form.is_valid():
            # gets form values from posted form
            form_cleaned = form.cleaned_data
            # gets user details from id provided in form
            user_obj = get_object_or_404(User, pk=int(form_cleaned['author']))
            # creates new post object
            Post.objects.create(
                title=form_cleaned['title'],
                slug=form_cleaned['slug'],
                author=user_obj,
                body=form_cleaned['body'],
                status='published',
            )
            return HttpResponseRedirect(reverse('blog:post_list'))
    else:
        form = NewPostForm()
    return render(request, 'blog/post/newpost.html', {'form': form})


def post_list(request, tag_slug=None):
    # all published objects
    object_list = Post.published.all()
    # instantiate tag variable
    tag = None
    # if tag slug provided in url then filter for it
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    # create pagination
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not int then return first page
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})