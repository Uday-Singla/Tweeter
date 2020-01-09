from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm, PostForm, CommentForm
from .models import Post, Comment, Profile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.models import User
import sendgrid
from sendgrid.helpers.mail import *
from django.core.mail import send_mail
import os 
from Tweeter import config

def register(request):

    if request.method == "POST":
        register_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if register_form.is_valid() and profile_form.is_valid():
            user = register_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
           # username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created! You are now able to login.')
            return redirect('login')

    else:
        register_form = UserRegistrationForm()
        profile_form = ProfileForm()

    context = {
        'register_form': register_form,
        'profile_form': profile_form,
    }
    return render(request, 'codebase/register.html', context)


@login_required
def feed(request):
    context = {
        'posts': Post.objects.filter(user__in=[following.user for following in Profile.objects.get(user=request.user).following.all()]).order_by('-date') | Post.objects.filter(user=request.user)
    }
    return render(request, 'codebase/feed.html', context)


@login_required
def profile(request, username):
    context = {
        'title': 'Profile',
        'profile': Profile.objects.get(user__username = username),
        'user_view': User.objects.get(username = username),
        'posts': Post.objects.filter(user__username=username).order_by('-date'),
        'following': [follows for follows in User.objects.filter(username__in=[following.user.username for following in Profile.objects.get(user=request.user).following.all()])],
        'subscribers': [subscriber for subscriber in User.objects.filter(username__in=[subscribed.user.username for subscribed in Profile.objects.get(user=request.user).subscribed.all()])]
    }
    return render(request, 'codebase/profile.html', context)


@login_required
def explore(request):
    context = {
        'profiles': Profile.objects.all(),
        'following': [follows for follows in User.objects.filter(username__in=[following.user.username for following in Profile.objects.get(user=request.user).following.all()])],
        'subscribers': [subscriber for subscriber in User.objects.filter(username__in=[subscribed.user.username for subscribed in Profile.objects.get(user=request.user).subscribed.all()])] 
    }
    return render(request, 'codebase/explore.html', context)


@login_required
def profile_new(request):
    
    if Profile.objects.filter(user=request.user) is None:
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('profile', username=request.user.username)
        
        else:
            form = ProfileForm()
            profile = form.save(commit=False)
            profile.user = request.user
            profile.user_id = request.user.id
            profile.save()
    
        return render(request, 'codebase/profile_edit.html', {'form': form})

    else:

        context = {
        'profiles': Profile.objects.all(),
        'following': [follows for follows in User.objects.filter(username__in=[following.user.username for following in Profile.objects.get(user=request.user).following.all()])],
        'subscribers': [subscriber for subscriber in User.objects.filter(username__in=[subscribed.user.username for subscribed in Profile.objects.get(user=request.user).subscribed.all()])]

        }
        
        return render(request, 'codebase/explore.html', context)

@login_required
def profile_edit(request):
    user = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES or None, instance=user)
        # Saving images can be a pain, don't forget to add
        # <form method="POST" enctype="multipart/form-data"> in the edit template
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
                       
            profile.save()
            return redirect('profile', username=profile.user.username)
    else:
        form = ProfileForm(instance=user)
    
    return render(request, 'codebase/profile_edit.html', {'form': form})


@login_required
def post_detail(request, pk):
    if pk in [post.pk for post in Post.objects.filter(user__in=[following.user for following in Profile.objects.get(user=request.user).following.all()])]:
        post = get_object_or_404(Post, pk=pk)
	
    if pk in [post.pk for post in Post.objects.filter(user=request.user)]:
        post = get_object_or_404(Post, pk=pk)
    
    context = {
        'post': post,
        'comments': Comment.objects.filter(post=post)
    }
    
    return render(request, 'codebase/post_detail.html', context)


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        # Saving images can be a pain, don't forget to add
        # <form method="POST" enctype="multipart/form-data"> in the edit template
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.date = timezone.now()
            post.save()

            to_email = []
            for subscriber in request.user.profile.subscribers.all():
                to_email.append(subscriber.user.email)
            
            sg = sendgrid.SendGridAPIClient(config.SENDGRID_API_KEY)
            from_email = Email("singla.uday2000@gmail.com")
            subject = "Tweeter - New Post by " + request.user.username
            content = Content("text/plain", "Visit Tweeter to check - " + "127.0.0.1:8000/post/" + str(post.pk))
            mail = Mail(from_email, to_email, subject, content)
            response = sg.send(mail)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            print(to_email)

            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()
    
    return render(request, 'codebase/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):

    if pk in [post.pk for post in Post.objects.filter(user=request.user)]:
        post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=post)
        # Saving images can be a pain, don't forget to add
        # <form method="POST" enctype="multipart/form-data"> in the edit template
        if form.is_valid():
            post_edit = form.save(commit=False)
            post_edit.user = request.user
            post.save()

            return redirect('post_detail', pk=post_edit.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'codebase/post_edit.html', {'form':form})


@login_required
def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.date = timezone.now()
            comment.post = post
            comment.save()

            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()
    
    return render(request, 'codebase/comment_add.html', {'form': form})


@login_required
def follow(request, username):
    
    Profile.objects.get(user=request.user).following.add(Profile.objects.get(user__username=username))
    Profile.objects.get(user__username=username).followers.add(Profile.objects.get(user=request.user))

    context = {
        'title': 'Profile',
        'profile': Profile.objects.get(user__username = username),
        'user_view': User.objects.get(username = username),
        'posts': Post.objects.filter(user__username=username),
        'following': [follows for follows in User.objects.filter(username__in=[following.user.username for following in Profile.objects.get(user=request.user).following.all()])],
        'subscribers': [subscriber for subscriber in User.objects.filter(username__in=[subscribed.user.username for subscribed in Profile.objects.get(user=request.user).subscribed.all()])]
}

    return render(request, 'codebase/profile.html', context)


@login_required
def unfollow(request, username):
    
    Profile.objects.get(user=request.user).following.remove(Profile.objects.get(user__username=username))
    Profile.objects.get(user__username=username).followers.remove(Profile.objects.get(user=request.user))
    Profile.objects.get(user=request.user).subscribed.remove(Profile.objects.get(user__username=username))
    Profile.objects.get(user__username=username).subscribers.remove(Profile.objects.get(user=request.user))
    
    context = {
        'title': 'Profile',
        'profile': Profile.objects.get(user__username = username),
        'user_view': User.objects.get(username = username),
        'posts': Post.objects.filter(user__username=username),
        'following': [follows for follows in User.objects.filter(username__in=[following.user.username for following in Profile.objects.get(user=request.user).following.all()])],
        'subscribers': [subscriber for subscriber in User.objects.filter(username__in=[subscribed.user.username for subscribed in Profile.objects.get(user=request.user).subscribed.all()])]
    }

    return render(request, 'codebase/profile.html', context)

@login_required
def subscribe(request, username):

    if User.objects.get(username=username) in [follower.user for follower in request.user.profile.following.all()]:
    
        Profile.objects.get(user=request.user).subscribed.add(Profile.objects.get(user__username=username))
        Profile.objects.get(user__username=username).subscribers.add(Profile.objects.get(user=request.user))

        context = {
            'title': 'Profile',
            'profile': Profile.objects.get(user__username = username),
            'user_view': User.objects.get(username = username),
            'posts': Post.objects.filter(user__username=username),
            'following': [follows for follows in User.objects.filter(username__in=[following.user.username for following in Profile.objects.get(user=request.user).following.all()])],
            'subscribers': [subscriber for subscriber in User.objects.filter(username__in=[subscribed.user.username for subscribed in Profile.objects.get(user=request.user).subscribed.all()])]
        }

        return render(request, 'codebase/profile.html', context)
    else:
        context = {
            'title': 'Profile',
            'profile': Profile.objects.get(user__username = username),
            'user_view': User.objects.get(username = username),
            'posts': Post.objects.filter(user__username=username),
            'following': [follows for follows in User.objects.filter(username__in=[following.user.username for following in Profile.objects.get(user=request.user).following.all()])],
            'subscribers': [subscriber for subscriber in User.objects.filter(username__in=[subscribed.user.username for subscribed in Profile.objects.get(user=request.user).subscribed.all()])]
        }

        return render(request, 'codebase/profile.html', context)


@login_required
def unsubscribe(request, username):
    
    Profile.objects.get(user=request.user).subscribed.remove(Profile.objects.get(user__username=username))
    Profile.objects.get(user__username=username).subscribers.remove(Profile.objects.get(user=request.user))

    context = {
        'title': 'Profile',
        'profile': Profile.objects.get(user__username = username),
        'user_view': User.objects.get(username = username),
        'posts': Post.objects.filter(user__username=username),
        'following': [follows for follows in User.objects.filter(username__in=[following.user.username for following in Profile.objects.get(user=request.user).following.all()])],
        'subscribers': [subscriber for subscriber in User.objects.filter(username__in=[subscribed.user.username for subscribed in Profile.objects.get(user=request.user).subscribed.all()])]
    }

    return render(request, 'codebase/profile.html', context)


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'codebase/logout.html')