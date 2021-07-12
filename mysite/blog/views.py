from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.urls import reverse
from .models import Post
from .forms import NewPostForm

# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name= 'blog/post/list.html'

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
