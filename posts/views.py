from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
         request,
         'index.html',
         {'page': page, 'paginator': paginator}
     )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {
        "group": group,
        'page': page,
        'paginator': paginator
        })


@login_required
def new_post(request):
    form = PostForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()

        return redirect('index')

    return render(request, 'new.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.author_posts.all()
    count_posts = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'profile.html', {
        'page': page,
        'paginator': paginator,
        'count_posts': count_posts,
        'profile': author}
                  )


def post_view(request, username, post_id):
    selected_post = get_object_or_404(
        Post,
        pk=post_id,
        author__username=username
        )
    count_posts = selected_post.author.author_posts.count()
    return render(request, 'post.html', {
        'profile': selected_post.author,
        'selected_post': selected_post,
        'count_posts': count_posts}
                  )


@login_required
def post_edit(request, username, post_id):
    selected_post = get_object_or_404(
        Post,
        pk=post_id,
        author__username=username
        )
    if request.user != selected_post.author:
        return redirect('post_view', username=username, post_id=post_id)

    form = PostForm(request.POST or None, instance=selected_post)
    if not form.is_valid():
        return render(request, 'new.html', {
            'form': form,
            "selected_post": selected_post})
    form.save()
    return redirect('post_view', username=username, post_id=post_id)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию, 
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500) 
