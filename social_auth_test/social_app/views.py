from functools import reduce

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from social_django.models import UserSocialAuth
import operator
from social_app.models import Post, LikeTable
from django.db.models import Q


def home(request):
    return post_listing(request)


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'google_login': google_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect,
        'user': user
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})


@login_required()
def post_new(request):
    if request.method == 'POST':
        title = request.POST.get("title", "Project Title")
        short_description = request.POST.get("description", "Project Description")
        story = request.POST.get("story", "Project Story")
        members = request.POST.get("member", "Utsav, Khang, Emma, Diego")
        creator = request.user.creator
        Post.objects.get_or_create(title=title, short_description=short_description, story=story,
                                          creator=creator, members=members)
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'core/post_new.html', {'post': None})


@login_required()
def post_editing(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.title = request.POST.get("title", "Project Title")
        post.short_description = request.POST.get("short_description", "Project Description")
        post.story = request.POST.get("description", "Project Description")
        post.members = request.POST.get("member", "Utsav, Khang, Emma, Diego")
        post.save()
        return HttpResponseRedirect(reverse('social_app:post_details', args=(post.id,)))
    return render(request, 'core/post_editing.html', {'post': post})


def post_details(request, post_id):
    if hasattr(request.user, 'creator'):
        creator = request.user.creator
    else:
        creator = None

    post = get_object_or_404(Post, pk=post_id)
    is_author = False
    if creator is not None and post.creator.id == creator.id:
        is_author = True

    return render(request, 'core/post_details.html', {'post': post, 'is_author': is_author})


def post_listing(request):
    search_query = None
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)

    if not search_query:
        trending_post_list = Post.objects.order_by('-pub_date')
    else:

        query_list = search_query.split()
        trending_post_list = Post.objects.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(short_description__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(story__icontains=q) for q in query_list))
        )

    context = {'trending_post_list': trending_post_list}
    return render(request, 'core/home.html', context)


def like_count(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        post = Post.objects.get(id=int(post_id))

        liked = post in request.user.creator.liketable_set

        if liked:
            print("unlike")
        else:
            print("like")
            LikeTable.objects.get_or_create(created=request.user.creator, post=post)

    return HttpResponse()


def favorite(request):
    trending_post_list = Post.objects.order_by('-title')[:4]
    context = {'trending_post_list': trending_post_list}
    return render(request, 'core/favorite.html', context)
