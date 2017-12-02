from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from social_django.models import UserSocialAuth

from social_app.models import Post


@login_required
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
def post_editing(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.title = request.POST["title"]
        post.short_description = request.POST["short_description"]
        post.story = request.POST["story"]
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

    if search_query is None:
        trending_post_list = Post.objects.order_by('-pub_date')[:5]
    else:
        trending_post_list = Post.objects.order_by('-pub_date')[:5]

    context = {'trending_post_list': trending_post_list}
    return render(request, 'core/home.html', context)